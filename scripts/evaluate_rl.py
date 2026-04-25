from __future__ import annotations

import json
import sys
from pathlib import Path

import pandas as pd
import yaml
from stable_baselines3 import PPO

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.rl.envs.leo_env import LeoEnv


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
        "final_mean_served_delay_s": history["mean_served_delay_s"][-1] if history["mean_served_delay_s"] else 0.0,
        "final_p95_served_delay_s": history["p95_served_delay_s"][-1] if history["p95_served_delay_s"] else 0.0,
        "final_mean_timeout_delay_s": history["mean_timeout_delay_s"][-1] if history["mean_timeout_delay_s"] else 0.0,
    }


def flatten_columns(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df.columns = [
        "_".join(col).strip("_") if isinstance(col, tuple) else col
        for col in df.columns.to_flat_index()
    ]
    return df


def main() -> None:
    rl_config_path = Path("configs/rl/ppo_both_v3.yaml") #Alterar se caso for testar outras versões
    with open(rl_config_path, "r", encoding="utf-8") as f:
        cfg = yaml.safe_load(f)

    scenario_config = cfg["env"]["scenario_config"]
    queue_norm = float(cfg["rl"]["queue_norm"])
    goodput_norm = float(cfg["rl"]["goodput_norm"])
    throughput_norm = float(cfg["rl"]["throughput_norm"])
    model_path = cfg["paths"]["model_path"]

    out_dir = Path("results/rl/evaluations/ppo_both_v3") #Alterar se caso for testar outras versões
    out_dir.mkdir(parents=True, exist_ok=True)

    model = PPO.load(model_path, device="cpu")

    rows = []

    for seed in DEFAULT_SEEDS:
        print(f"Avaliando seed={seed}")

        env = LeoEnv(
            config_path=scenario_config,
            queue_norm=queue_norm,
            goodput_norm=goodput_norm,
            throughput_norm=throughput_norm,
        )

        obs, info = env.reset(seed=seed)
        terminated = False
        truncated = False
        episode_reward = 0.0
        episode_steps = 0

        while not (terminated or truncated):
            action, _ = model.predict(obs, deterministic=True)
            obs, reward, terminated, truncated, step_info = env.step(action)
            episode_reward += float(reward)
            episode_steps += 1

        assert env.scenario is not None
        history = env.scenario.history
        summary = summarize_history(history)

        row = {
            "scenario": Path(scenario_config).stem,
            "strategy": "ppo",
            "seed": seed,
            "episode_reward": episode_reward,
            "episode_steps": episode_steps,
            **summary,
        }
        rows.append(row)

        seed_dir = out_dir / f"seed_{seed}"
        seed_dir.mkdir(parents=True, exist_ok=True)

        pd.DataFrame(history).to_csv(seed_dir / "history.csv", index=False)
        env.scenario.save_plots(seed_dir)

        with open(seed_dir / "summary.json", "w", encoding="utf-8") as f:
            json.dump(row, f, indent=2, ensure_ascii=False)

    runs_df = pd.DataFrame(rows)
    runs_df.to_csv(out_dir / "rl_eval_runs.csv", index=False)

    metrics = [
        "episode_reward",
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

    summary_df = runs_df.groupby(["scenario", "strategy"])[metrics].agg(["mean", "std"]).reset_index()
    summary_df = flatten_columns(summary_df)
    summary_df.to_csv(out_dir / "rl_eval_summary.csv", index=False)

    print("\n--- RESUMO RL ---")
    print(summary_df.to_string(index=False))
    print(f"\nResultados em: {out_dir.resolve()}")


if __name__ == "__main__":
    main()