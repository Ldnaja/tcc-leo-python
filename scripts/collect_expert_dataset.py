from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import yaml

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.rl.envs.leo_env import LeoEnv
from src.rl.expert import expert_action_greedy_backlog


DEFAULT_SEEDS = [42, 43, 44, 45, 46, 47, 48, 49, 50, 51]


def main() -> None:
    config_path = Path("configs/rl/ppo_both_v4.yaml")
    with open(config_path, "r", encoding="utf-8") as f:
        cfg = yaml.safe_load(f)

    scenario_config = cfg["env"]["scenario_config"]
    queue_norm = float(cfg["rl"]["queue_norm"])
    goodput_norm = float(cfg["rl"]["goodput_norm"])
    throughput_norm = float(cfg["rl"]["throughput_norm"])

    total_channels = int(cfg["expert"]["total_channels"])
    total_power_w = float(cfg["expert"]["total_power_w"])
    max_channels_per_beam = int(cfg["expert"]["max_channels_per_beam"])

    out_path = Path(cfg["expert"]["dataset_path"])
    out_path.parent.mkdir(parents=True, exist_ok=True)

    all_obs = []
    all_actions = []

    for seed in DEFAULT_SEEDS:
        print(f"Coletando expert seed={seed}")

        env = LeoEnv(
            config_path=scenario_config,
            queue_norm=queue_norm,
            goodput_norm=goodput_norm,
            throughput_norm=throughput_norm,
        )

        obs, _ = env.reset(seed=seed)
        terminated = False
        truncated = False

        while not (terminated or truncated):
            assert env.scenario is not None

            action = expert_action_greedy_backlog(
                beams=env.scenario.beams,
                total_channels=total_channels,
                total_power_w=total_power_w,
                max_channels_per_beam=max_channels_per_beam,
            )

            all_obs.append(obs.astype(np.float32))
            all_actions.append(action.astype(np.float32))

            obs, reward, terminated, truncated, info = env.step(action)

    obs_arr = np.stack(all_obs)
    act_arr = np.stack(all_actions)

    np.savez_compressed(out_path, observations=obs_arr, actions=act_arr)

    print(f"Dataset salvo em: {out_path}")
    print(f"Observations shape: {obs_arr.shape}")
    print(f"Actions shape: {act_arr.shape}")


if __name__ == "__main__":
    main()