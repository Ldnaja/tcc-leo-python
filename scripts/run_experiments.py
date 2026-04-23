from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.scenarios.baseline import BaselineScenario


DEFAULT_CONFIGS = [
    "configs/baseline.yaml",
    "configs/baseline_queue_cap.yaml",
    "configs/baseline_timeout.yaml",
    "configs/baseline_both.yaml",
]

DEFAULT_STRATEGIES = [
    "proportional_fair",
    "round_robin",
    "longest_queue_first",
    "greedy_backlog",
]

DEFAULT_SEEDS = [42, 43, 44, 45, 46, 47, 48, 49, 50, 51]


def summarize_history(history: dict) -> dict:
    avg_offered = sum(history["offered_load_mbps"]) / max(1, len(history["offered_load_mbps"]))
    avg_accepted = sum(history["accepted_load_mbps"]) / max(1, len(history["accepted_load_mbps"]))
    avg_capacity = sum(history["capacity_sum_mbps"]) / max(1, len(history["capacity_sum_mbps"]))
    avg_goodput = sum(history["goodput_sum_mbps"]) / max(1, len(history["goodput_sum_mbps"]))
    avg_queue = sum(history["queue_sum"]) / max(1, len(history["queue_sum"]))
    avg_utilization = sum(history["utilization"]) / max(1, len(history["utilization"]))
    avg_fairness = sum(history["fairness"]) / max(1, len(history["fairness"]))
    avg_acceptance_rate = sum(history["acceptance_rate"]) / max(1, len(history["acceptance_rate"]))
    avg_service_rate = sum(history["service_rate"]) / max(1, len(history["service_rate"]))
    final_mean_served_delay_s = history["mean_served_delay_s"][-1] if history["mean_served_delay_s"] else 0.0
    final_p95_served_delay_s = history["p95_served_delay_s"][-1] if history["p95_served_delay_s"] else 0.0
    final_mean_timeout_delay_s = history["mean_timeout_delay_s"][-1] if history["mean_timeout_delay_s"] else 0.0

    return {
        "samples": len(history["time"]),
        "avg_offered_load_mbps": avg_offered,
        "avg_accepted_load_mbps": avg_accepted,
        "avg_capacity_mbps": avg_capacity,
        "avg_goodput_mbps": avg_goodput,
        "avg_queue": avg_queue,
        "final_capacity_mbps": history["capacity_sum_mbps"][-1] if history["capacity_sum_mbps"] else 0.0,
        "final_goodput_mbps": history["goodput_sum_mbps"][-1] if history["goodput_sum_mbps"] else 0.0,
        "final_queue": history["queue_sum"][-1] if history["queue_sum"] else 0,
        "final_blocked_rate": history["blocked_rate"][-1] if history["blocked_rate"] else 0.0,
        "final_blocked_queue_cap_rate": history["blocked_queue_cap_rate"][-1] if history["blocked_queue_cap_rate"] else 0.0,
        "final_blocked_timeout_rate": history["blocked_timeout_rate"][-1] if history["blocked_timeout_rate"] else 0.0,
        "final_utilization": history["utilization"][-1] if history["utilization"] else 0.0,
        "final_fairness": history["fairness"][-1] if history["fairness"] else 0.0,
        "avg_utilization": avg_utilization,
        "avg_fairness": avg_fairness,
        "avg_acceptance_rate": avg_acceptance_rate,
        "avg_service_rate": avg_service_rate,
        "final_mean_served_delay_s": final_mean_served_delay_s,
        "final_p95_served_delay_s": final_p95_served_delay_s,
        "final_mean_timeout_delay_s": final_mean_timeout_delay_s,
    }


def flatten_columns(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df.columns = [
        "_".join(col).strip("_") if isinstance(col, tuple) else col
        for col in df.columns.to_flat_index()
    ]
    return df


def main() -> None:
    parser = argparse.ArgumentParser(description="Roda experimentos com múltiplas seeds, cenários e heurísticas.")
    parser.add_argument("--configs", nargs="+", default=DEFAULT_CONFIGS, help="Lista de arquivos YAML.")
    parser.add_argument("--strategies", nargs="+", default=DEFAULT_STRATEGIES, help="Lista de heurísticas.")
    parser.add_argument("--seeds", nargs="+", type=int, default=DEFAULT_SEEDS, help="Lista de seeds.")
    parser.add_argument("--outdir", type=str, default="results/experiments", help="Diretório base de saída.")
    parser.add_argument(
        "--save-histories",
        action="store_true",
        help="Se ativo, salva history.csv e gráficos de cada execução individual.",
    )
    args = parser.parse_args()

    out_dir = Path(args.outdir)
    out_dir.mkdir(parents=True, exist_ok=True)

    rows = []

    total_runs = len(args.configs) * len(args.strategies) * len(args.seeds)
    current_run = 0

    for config in args.configs:
        config_path = Path(config)
        scenario_name = config_path.stem

        for strategy in args.strategies:
            for seed in args.seeds:
                current_run += 1
                print(f"[{current_run}/{total_runs}] cenário={scenario_name} estratégia={strategy} seed={seed}")

                scenario = BaselineScenario(
                    config_path=config_path,
                    seed_override=seed,
                    strategy_override=strategy,
                )
                history = scenario.run()
                summary = summarize_history(history)

                row = {
                    "scenario": scenario_name,
                    "strategy": strategy,
                    "seed": seed,
                    **summary,
                }
                rows.append(row)

                if args.save_histories:
                    run_dir = out_dir / "runs" / scenario_name / strategy / f"seed_{seed}"
                    run_dir.mkdir(parents=True, exist_ok=True)
                    pd.DataFrame(history).to_csv(run_dir / "history.csv", index=False)
                    scenario.save_plots(run_dir)
                    with open(run_dir / "summary.json", "w", encoding="utf-8") as f:
                        json.dump(row, f, indent=2, ensure_ascii=False)

    runs_df = pd.DataFrame(rows)
    runs_df.to_csv(out_dir / "all_runs.csv", index=False)

    metrics = [
        "avg_offered_load_mbps",
        "avg_accepted_load_mbps",
        "avg_capacity_mbps",
        "avg_goodput_mbps",
        "avg_queue",
        "final_queue",
        "final_blocked_rate",
        "final_blocked_queue_cap_rate",
        "final_blocked_timeout_rate",
        "final_utilization",
        "final_fairness",
        "avg_acceptance_rate",
        "avg_service_rate",
        "final_mean_served_delay_s",
        "final_p95_served_delay_s",
        "final_mean_timeout_delay_s",
    ]

    table_df = runs_df.groupby(["scenario", "strategy"])[metrics].agg(["mean", "std"]).reset_index()
    table_df = flatten_columns(table_df)
    table_df.to_csv(out_dir / "comparison_table.csv", index=False)

    print("\n--- TABELA FINAL (médias e desvios) ---")
    print(table_df.to_string(index=False))
    print(f"\nResultados consolidados em: {out_dir.resolve()}")


if __name__ == "__main__":
    main()