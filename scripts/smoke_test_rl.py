from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
from stable_baselines3.common.env_checker import check_env

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.rl.envs.leo_env import LeoEnv


def main() -> None:
    env = LeoEnv("configs/baseline_both.yaml")

    print("Verificando ambiente com check_env...")
    check_env(env, warn=True)
    print("Ambiente OK.")

    obs, info = env.reset(seed=42)
    print("Obs shape:", obs.shape)
    print("Reset info:", info)

    total_reward = 0.0
    for step in range(10):
        action = env.action_space.sample()
        obs, reward, terminated, truncated, info = env.step(action)
        total_reward += reward
        print(
            f"step={step} reward={reward:.4f} "
            f"goodput={info['goodput_sum_mbps']:.2f} "
            f"queue={info['queue_sum']} blocked_step_ratio={info['blocked_step_ratio']:.4f}"
        )
        if terminated or truncated:
            break

    print("Total reward:", total_reward)


if __name__ == "__main__":
    main()