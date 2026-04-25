from __future__ import annotations

from pathlib import Path

import pandas as pd


def main() -> None:
    heuristics_path = Path("results/experiments_sensitivity/comparison_table.csv")
    rl_path = Path("results/rl/evaluations/robustness/ppo_both_v4/rl_robustness_summary.csv")
    out_dir = Path("results/rl/comparisons/robustness/ppo_both_v4")
    out_dir.mkdir(parents=True, exist_ok=True)

    heur_df = pd.read_csv(heuristics_path)
    rl_df = pd.read_csv(rl_path)

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

    heur_sel = heur_df[selected_cols].copy()
    rl_sel = rl_df[selected_cols].copy()

    comparison_df = pd.concat([heur_sel, rl_sel], ignore_index=True)
    comparison_df.to_csv(out_dir / "robustness_rl_vs_heuristics.csv", index=False)

    print("\n--- COMPARAÇÃO ROBUSTEZ RL V4 VS HEURÍSTICAS ---")
    print(comparison_df.to_string(index=False))
    print(f"\nArquivo salvo em: {(out_dir / 'robustness_rl_vs_heuristics.csv').resolve()}")


if __name__ == "__main__":
    main()