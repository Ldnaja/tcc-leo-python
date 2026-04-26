
from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


def find_first_existing(base_dir: Path, candidates: list[str]) -> Path:
    for candidate in candidates:
        path = base_dir / candidate
        if path.exists():
            return path
    raise FileNotFoundError(
        "Nenhum dos caminhos foi encontrado:\n- " + "\n- ".join(str(base_dir / c) for c in candidates)
    )


def ensure_dirs(out_dir: Path) -> tuple[Path, Path]:
    figures_dir = out_dir / "figures"
    tables_dir = out_dir / "tables"
    figures_dir.mkdir(parents=True, exist_ok=True)
    tables_dir.mkdir(parents=True, exist_ok=True)
    return figures_dir, tables_dir


def save_table(df: pd.DataFrame, path: Path) -> None:
    df.to_csv(path, index=False)


def sort_by_order(df: pd.DataFrame, column: str, order: list[str]) -> pd.DataFrame:
    tmp = df.copy()
    tmp[column] = pd.Categorical(tmp[column], categories=order, ordered=True)
    return tmp.sort_values(column).reset_index(drop=True)


def normalize_strategy_name(value: str) -> str:
    if value == "ppo":
        return "ppo_v4"
    return value


def plot_bar_with_error(
    df: pd.DataFrame,
    x_col: str,
    y_col: str,
    err_col: str,
    title: str,
    ylabel: str,
    out_path: Path,
    rotate_xticks: bool = False,
) -> None:
    plt.figure(figsize=(10, 5))
    plt.bar(df[x_col], df[y_col], yerr=df[err_col], capsize=4)
    plt.title(title)
    plt.ylabel(ylabel)
    plt.grid(axis="y", alpha=0.3)
    if rotate_xticks:
        plt.xticks(rotation=25, ha="right")
    plt.tight_layout()
    plt.savefig(out_path, dpi=200)
    plt.close()


def plot_grouped_metric_figure(
    df: pd.DataFrame,
    x_col: str,
    metrics: list[tuple[str, str, str]],
    base_name: str,
    figures_dir: Path,
    rotate_xticks: bool = False,
) -> None:
    for y_col, err_col, ylabel in metrics:
        title = f"{ylabel}"
        out_path = figures_dir / f"{base_name}_{y_col}.png"
        plot_bar_with_error(
            df=df,
            x_col=x_col,
            y_col=y_col,
            err_col=err_col,
            title=title,
            ylabel=ylabel,
            out_path=out_path,
            rotate_xticks=rotate_xticks,
        )


def plot_boxplot(
    dataframes: list[pd.DataFrame],
    labels: list[str],
    value_col: str,
    title: str,
    ylabel: str,
    out_path: Path,
) -> None:
    values = [df[value_col].dropna().tolist() for df in dataframes]
    plt.figure(figsize=(10, 5))
    plt.boxplot(values, labels=labels, patch_artist=False)
    plt.title(title)
    plt.ylabel(ylabel)
    plt.grid(axis="y", alpha=0.3)
    plt.tight_layout()
    plt.savefig(out_path, dpi=200)
    plt.close()


def build_inputs(base_dir: Path) -> dict[str, Path]:
    return {
        "compare_main": find_first_existing(
            base_dir,
            [
                "results/experiments_main/comparison_table_experiments_main.csv",
                "results/experiments_main/comparison_table.csv",
                "comparison_table_experiments_main.csv",
                "comparison_table.csv",
            ],
        ),
        "compare_sensitivity": find_first_existing(
            base_dir,
            [
                "results/experiments_sensitivity/comparison_table_experiments_sensitivity.csv",
                "results/experiments_sensitivity/comparison_table.csv",
                "comparison_table_experiments_sensitivity.csv",
            ],
        ),
        "rl_summary_v1": find_first_existing(
            base_dir,
            [
                "results/rl/evaluations/ppo_both_v1/rl_eval_summary_ppo_both_v1.csv",
                "results/rl/evaluations/ppo_both_v1/rl_eval_summary.csv",
                "rl_eval_summary_ppo_both_v1.csv",
            ],
        ),
        "rl_summary_v2": find_first_existing(
            base_dir,
            [
                "results/rl/evaluations/ppo_both_v2/rl_eval_summary_ppo_v2_both.csv",
                "results/rl/evaluations/ppo_both_v2/rl_eval_summary.csv",
                "rl_eval_summary_ppo_v2_both.csv",
            ],
        ),
        "rl_summary_v3": find_first_existing(
            base_dir,
            [
                "results/rl/evaluations/ppo_both_v3/rl_eval_summary_ppo_v3_both.csv",
                "results/rl/evaluations/ppo_both_v3/rl_eval_summary.csv",
                "rl_eval_summary_ppo_v3_both.csv",
            ],
        ),
        "rl_summary_v4": find_first_existing(
            base_dir,
            [
                "results/rl/evaluations/ppo_both_v4/rl_eval_summary_ppo_v4_both.csv",
                "results/rl/evaluations/ppo_both_v4/rl_eval_summary.csv",
                "rl_eval_summary_ppo_v4_both.csv",
            ],
        ),
        "final_compare_v4": find_first_existing(
            base_dir,
            [
                "results/rl/comparisons/ppo_both_v4/baseline_both_rl_vs_heuristics_ppo_v4_both.csv",
                "results/rl/comparisons/ppo_both_v4/baseline_both_rl_vs_heuristics.csv",
                "baseline_both_rl_vs_heuristics_ppo_v4_both.csv",
            ],
        ),
        "robust_summary_v4": find_first_existing(
            base_dir,
            [
                "results/rl/robustness/ppo_both_v4/rl_robustness_summary_ppo_v4_both.csv",
                "results/rl/robustness/ppo_both_v4/rl_robustness_summary.csv",
                "results/rl/evaluations/robustness/ppo_both_v4/rl_robustness_summary_ppo_v4_both.csv",
                "rl_robustness_summary_ppo_v4_both.csv",
            ],
        ),
        "robust_compare_v4": find_first_existing(
            base_dir,
            [
                "results/rl/comparisons/robustness/ppo_both_v4/robustness_rl_vs_heuristics_robustness_ppo_v4.csv",
                "results/rl/comparisons/robustness/ppo_both_v4/robustness_rl_vs_heuristics.csv",
                "robustness_rl_vs_heuristics_robustness_ppo_v4.csv",
            ],
        ),
        "rl_runs_v1": find_first_existing(
            base_dir,
            [
                "results/rl/evaluations/ppo_both_v1/rl_eval_runs_ppo_v1_both.csv",
                "results/rl/evaluations/ppo_both_v1/rl_eval_runs.csv",
                "rl_eval_runs_ppo_v1_both.csv",
            ],
        ),
        "rl_runs_v2": find_first_existing(
            base_dir,
            [
                "results/rl/evaluations/ppo_both_v2/rl_eval_runs_ppo_v2_both.csv",
                "results/rl/evaluations/ppo_both_v2/rl_eval_runs.csv",
                "rl_eval_runs_ppo_v2_both.csv",
            ],
        ),
        "rl_runs_v3": find_first_existing(
            base_dir,
            [
                "results/rl/evaluations/ppo_both_v3/rl_eval_runs_ppo_v3_both.csv",
                "results/rl/evaluations/ppo_both_v3/rl_eval_runs.csv",
                "rl_eval_runs_ppo_v3_both.csv",
            ],
        ),
        "rl_runs_v4": find_first_existing(
            base_dir,
            [
                "results/rl/evaluations/ppo_both_v4/rl_eval_runs_ppo_v4_both.csv",
                "results/rl/evaluations/ppo_both_v4/rl_eval_runs.csv",
                "rl_eval_runs_ppo_v4_both.csv",
            ],
        ),
        "robust_runs_v4": find_first_existing(
            base_dir,
            [
                "results/rl/robustness/ppo_both_v4/rl_robustness_runs.csv",
                "results/rl/evaluations/robustness/ppo_both_v4/rl_robustness_runs.csv",
                "rl_robustness_runs.csv",
            ],
        ),
    }

def main() -> None:
    parser = argparse.ArgumentParser(description="Compila tabelas e gráficos principais do TCC NTN/LEO.")
    parser.add_argument(
        "--base-dir",
        type=str,
        default=".",
        help="Diretório base onde estão os CSVs.",
    )
    parser.add_argument(
        "--out-dir",
        type=str,
        default="results/tcc_compilation",
        help="Diretório de saída.",
    )
    args = parser.parse_args()

    base_dir = Path(args.base_dir).resolve()
    out_dir = Path(args.out_dir).resolve()
    figures_dir, tables_dir = ensure_dirs(out_dir)
    inputs = build_inputs(base_dir)

    compare_main = pd.read_csv(inputs["compare_main"])
    compare_sensitivity = pd.read_csv(inputs["compare_sensitivity"])
    rl_summary_v1 = pd.read_csv(inputs["rl_summary_v1"])
    rl_summary_v2 = pd.read_csv(inputs["rl_summary_v2"])
    rl_summary_v3 = pd.read_csv(inputs["rl_summary_v3"])
    rl_summary_v4 = pd.read_csv(inputs["rl_summary_v4"])
    final_compare_v4 = pd.read_csv(inputs["final_compare_v4"])
    robust_summary_v4 = pd.read_csv(inputs["robust_summary_v4"])
    robust_compare_v4 = pd.read_csv(inputs["robust_compare_v4"])
    rl_runs_v1 = pd.read_csv(inputs["rl_runs_v1"])
    rl_runs_v2 = pd.read_csv(inputs["rl_runs_v2"])
    rl_runs_v3 = pd.read_csv(inputs["rl_runs_v3"])
    rl_runs_v4 = pd.read_csv(inputs["rl_runs_v4"])
    robust_runs_v4 = pd.read_csv(inputs["robust_runs_v4"])

    strategy_order = ["proportional_fair", "round_robin", "longest_queue_first", "greedy_backlog", "ppo_v4"]
    rl_version_order = ["ppo_v1", "ppo_v2", "ppo_v3", "ppo_v4"]
    sensitivity_order = [
        "both_ch32",
        "both_ch64",
        "both_int3",
        "both_int6",
        "both_q5_t10",
        "both_q5_t40",
        "both_q10_t20",
        "both_q15_t20",
    ]

    # TABELA 1: cenário principal baseline_both com heurísticas
    table_main_baseline_both = compare_main[compare_main["scenario"] == "baseline_both"].copy()
    table_main_baseline_both = sort_by_order(table_main_baseline_both, "strategy", strategy_order[:-1])
    save_table(table_main_baseline_both, tables_dir / "table_01_main_baseline_both_heuristics.csv")

    # TABELA 2: sensibilidade com proportional_fair
    table_sensitivity_pf = compare_sensitivity[compare_sensitivity["strategy"] == "proportional_fair"].copy()
    table_sensitivity_pf = sort_by_order(table_sensitivity_pf, "scenario", sensitivity_order)
    save_table(table_sensitivity_pf, tables_dir / "table_02_sensitivity_proportional_fair.csv")

    # TABELA 3: evolução RL v1-v4
    versions = [
        ("ppo_v1", rl_summary_v1),
        ("ppo_v2", rl_summary_v2),
        ("ppo_v3", rl_summary_v3),
        ("ppo_v4", rl_summary_v4),
    ]
    rl_version_rows = []
    for version_name, df in versions:
        row = df.iloc[0].copy()
        row["strategy"] = version_name
        rl_version_rows.append(row)
    table_rl_versions = pd.DataFrame(rl_version_rows)
    table_rl_versions = sort_by_order(table_rl_versions, "strategy", rl_version_order)
    save_table(table_rl_versions, tables_dir / "table_03_rl_versions_summary.csv")

    # TABELA 4: comparação final RL v4 vs heurísticas
    final_compare_v4 = final_compare_v4.copy()
    final_compare_v4["strategy"] = final_compare_v4["strategy"].apply(normalize_strategy_name)
    final_compare_v4 = sort_by_order(final_compare_v4, "strategy", strategy_order)
    save_table(final_compare_v4, tables_dir / "table_04_final_rl_v4_vs_heuristics.csv")

    # TABELA 5: robustez RL v4
    robust_summary_v4 = robust_summary_v4.copy()
    robust_summary_v4["strategy"] = robust_summary_v4["strategy"].apply(normalize_strategy_name)
    robust_summary_v4 = sort_by_order(robust_summary_v4, "scenario", sensitivity_order)
    save_table(robust_summary_v4, tables_dir / "table_05_rl_v4_robustness_summary.csv")

    # TABELA 6: robustez RL v4 vs heurísticas
    robust_compare_v4 = robust_compare_v4.copy()
    robust_compare_v4["strategy"] = robust_compare_v4["strategy"].apply(normalize_strategy_name)
    robust_compare_v4 = sort_by_order(robust_compare_v4, "scenario", sensitivity_order)
    save_table(robust_compare_v4, tables_dir / "table_06_rl_v4_robustness_vs_heuristics.csv")

    # FIGURA 1: baseline_both - goodput
    plot_bar_with_error(
        df=final_compare_v4,
        x_col="strategy",
        y_col="avg_goodput_mbps_mean",
        err_col="avg_goodput_mbps_std",
        title="Cenário baseline_both - Goodput médio",
        ylabel="Goodput médio (Mbps)",
        out_path=figures_dir / "fig_01_baseline_both_goodput.png",
    )

    # FIGURA 2: baseline_both - bloqueio final
    plot_bar_with_error(
        df=final_compare_v4,
        x_col="strategy",
        y_col="final_blocked_rate_mean",
        err_col="final_blocked_rate_std",
        title="Cenário baseline_both - Taxa final de bloqueio",
        ylabel="Taxa final de bloqueio",
        out_path=figures_dir / "fig_02_baseline_both_blocking.png",
    )

    # FIGURA 3: baseline_both - atraso médio servido final
    plot_bar_with_error(
        df=final_compare_v4,
        x_col="strategy",
        y_col="final_mean_served_delay_s_mean",
        err_col="final_mean_served_delay_s_std",
        title="Cenário baseline_both - Atraso médio servido final",
        ylabel="Atraso médio servido final (s)",
        out_path=figures_dir / "fig_03_baseline_both_delay.png",
    )

    # FIGURA 4: evolução RL v1-v4 - goodput
    plot_bar_with_error(
        df=table_rl_versions,
        x_col="strategy",
        y_col="avg_goodput_mbps_mean",
        err_col="avg_goodput_mbps_std",
        title="Evolução do PPO entre versões - Goodput médio",
        ylabel="Goodput médio (Mbps)",
        out_path=figures_dir / "fig_04_rl_versions_goodput.png",
    )

    # FIGURA 5: evolução RL v1-v4 - recompensa
    plot_bar_with_error(
        df=table_rl_versions,
        x_col="strategy",
        y_col="episode_reward_mean",
        err_col="episode_reward_std",
        title="Evolução do PPO entre versões - Recompensa por episódio",
        ylabel="Recompensa média",
        out_path=figures_dir / "fig_05_rl_versions_reward.png",
    )

    # FIGURA 6: sensibilidade (proportional_fair) - goodput
    plot_bar_with_error(
        df=table_sensitivity_pf,
        x_col="scenario",
        y_col="avg_goodput_mbps_mean",
        err_col="avg_goodput_mbps_std",
        title="Sensibilidade com proportional_fair - Goodput médio",
        ylabel="Goodput médio (Mbps)",
        out_path=figures_dir / "fig_06_sensitivity_pf_goodput.png",
        rotate_xticks=True,
    )

    # FIGURA 7: sensibilidade (proportional_fair) - bloqueio final
    plot_bar_with_error(
        df=table_sensitivity_pf,
        x_col="scenario",
        y_col="final_blocked_rate_mean",
        err_col="final_blocked_rate_std",
        title="Sensibilidade com proportional_fair - Taxa final de bloqueio",
        ylabel="Taxa final de bloqueio",
        out_path=figures_dir / "fig_07_sensitivity_pf_blocking.png",
        rotate_xticks=True,
    )

    # FIGURA 8: robustez RL v4 - goodput por cenário
    plot_bar_with_error(
        df=robust_summary_v4,
        x_col="scenario",
        y_col="avg_goodput_mbps_mean",
        err_col="avg_goodput_mbps_std",
        title="Robustez do PPO v4 - Goodput médio por cenário",
        ylabel="Goodput médio (Mbps)",
        out_path=figures_dir / "fig_08_rl_v4_robustness_goodput.png",
        rotate_xticks=True,
    )

    # FIGURA 9: robustez RL v4 - bloqueio por cenário
    plot_bar_with_error(
        df=robust_summary_v4,
        x_col="scenario",
        y_col="final_blocked_rate_mean",
        err_col="final_blocked_rate_std",
        title="Robustez do PPO v4 - Taxa final de bloqueio por cenário",
        ylabel="Taxa final de bloqueio",
        out_path=figures_dir / "fig_09_rl_v4_robustness_blocking.png",
        rotate_xticks=True,
    )

    # FIGURA 10: boxplot goodput por versão RL
    rl_runs_v1["version"] = "ppo_v1"
    rl_runs_v2["version"] = "ppo_v2"
    rl_runs_v3["version"] = "ppo_v3"
    rl_runs_v4["version"] = "ppo_v4"
    plot_boxplot(
        dataframes=[rl_runs_v1, rl_runs_v2, rl_runs_v3, rl_runs_v4],
        labels=rl_version_order,
        value_col="avg_goodput_mbps",
        title="Dispersão do goodput por seed nas versões PPO",
        ylabel="Goodput médio por seed (Mbps)",
        out_path=figures_dir / "fig_10_boxplot_rl_versions_goodput.png",
    )

    # FIGURA 11: boxplot recompensa por versão RL
    plot_boxplot(
        dataframes=[rl_runs_v1, rl_runs_v2, rl_runs_v3, rl_runs_v4],
        labels=rl_version_order,
        value_col="episode_reward",
        title="Dispersão da recompensa por seed nas versões PPO",
        ylabel="Recompensa por episódio",
        out_path=figures_dir / "fig_11_boxplot_rl_versions_reward.png",
    )

    # FIGURA 12: boxplot robustez RL v4 por cenário
    robust_runs_grouped = [group for _, group in robust_runs_v4.groupby("scenario", sort=False)]
    robust_labels = [name for name, _ in robust_runs_v4.groupby("scenario", sort=False)]
    plot_boxplot(
        dataframes=robust_runs_grouped,
        labels=robust_labels,
        value_col="avg_goodput_mbps",
        title="Dispersão do goodput por seed nos cenários de robustez (PPO v4)",
        ylabel="Goodput médio por seed (Mbps)",
        out_path=figures_dir / "fig_12_boxplot_rl_v4_robustness_goodput.png",
    )

    print("\nArquivos de entrada encontrados:")
    for key, value in inputs.items():
        print(f"- {key}: {value}")

    print(f"\nTabelas salvas em: {tables_dir}")
    print(f"Figuras salvas em: {figures_dir}")
    print("\nSugestão para o corpo do TCC:")
    print("1) fig_01_baseline_both_goodput.png")
    print("2) fig_02_baseline_both_blocking.png")
    print("3) fig_04_rl_versions_goodput.png")
    print("4) fig_06_sensitivity_pf_goodput.png")
    print("5) fig_08_rl_v4_robustness_goodput.png")
    print("6) fig_09_rl_v4_robustness_blocking.png")
    print("\nSugestão para apêndice:")
    print("7) fig_03_baseline_both_delay.png")
    print("8) fig_05_rl_versions_reward.png")
    print("9) fig_07_sensitivity_pf_blocking.png")
    print("10) fig_10_boxplot_rl_versions_goodput.png")
    print("11) fig_11_boxplot_rl_versions_reward.png")
    print("12) fig_12_boxplot_rl_v4_robustness_goodput.png")


if __name__ == "__main__":
    main()
