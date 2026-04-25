from __future__ import annotations

from pathlib import Path

import pandas as pd


def main() -> None:
    heuristics_path = Path("results/experiments_main/comparison_table.csv")
    rl_path = Path("results/rl/evaluations/ppo_both_v3/rl_eval_summary.csv")  # Alterar se caso for testar outras versões
    out_dir = Path("results/rl/comparisons/ppo_both_v3")  # Alterar se caso for testar outras versões
    out_dir.mkdir(parents=True, exist_ok=True)

    heur_df = pd.read_csv(heuristics_path)
    rl_df = pd.read_csv(rl_path)

    heur_both = heur_df[heur_df["scenario"] == "baseline_both"].copy()

    selected_cols = [
        "scenario",
        "strategy",
        "avg_goodput_mbps_mean",
        "avg_goodput_mbps_std",
        "final_blocked_rate_mean",
        "final_blocked_rate_std",
        "avg_acceptance_rate_mean",
        "avg_acceptance_rate_std",
        "avg_service_rate_mean",
        "avg_service_rate_std",
        "final_mean_served_delay_s_mean",
        "final_mean_served_delay_s_std",
        "final_p95_served_delay_s_mean",
        "final_p95_served_delay_s_std",
        "final_fairness_mean",
        "final_fairness_std",
        "final_queue_mean",
        "final_queue_std",
    ]
    heur_both = heur_both[selected_cols]

    rl_both = rl_df[
        [
            "scenario",
            "strategy",
            "avg_goodput_mbps_mean",
            "avg_goodput_mbps_std",
            "final_blocked_rate_mean",
            "final_blocked_rate_std",
            "avg_acceptance_rate_mean",
            "avg_acceptance_rate_std",
            "avg_service_rate_mean",
            "avg_service_rate_std",
            "final_mean_served_delay_s_mean",
            "final_mean_served_delay_s_std",
            "final_p95_served_delay_s_mean",
            "final_p95_served_delay_s_std",
            "final_fairness_mean",
            "final_fairness_std",
            "final_queue_mean",
            "final_queue_std",
        ]
    ].copy()

    comparison_df = pd.concat([heur_both, rl_both], ignore_index=True)
    comparison_df.to_csv(out_dir / "baseline_both_rl_vs_heuristics.csv", index=False)

    print("\n--- COMPARAÇÃO RL VS HEURÍSTICAS (baseline_both) ---")
    print(comparison_df.to_string(index=False))
    print(f"\nArquivo salvo em: {(out_dir / 'baseline_both_rl_vs_heuristics.csv').resolve()}")


if __name__ == "__main__":
    main()