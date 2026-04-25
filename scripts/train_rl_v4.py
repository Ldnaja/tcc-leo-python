from __future__ import annotations

import sys
from pathlib import Path

import yaml
from stable_baselines3 import PPO
from stable_baselines3.common.callbacks import CheckpointCallback
from stable_baselines3.common.env_checker import check_env
from stable_baselines3.common.monitor import Monitor

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.rl.envs.leo_env import LeoEnv


def main() -> None:
    config_path = Path("configs/rl/ppo_both_v4.yaml")

    with open(config_path, "r", encoding="utf-8") as f:
        cfg = yaml.safe_load(f)

    scenario_config = cfg["env"]["scenario_config"]
    queue_norm = float(cfg["rl"]["queue_norm"])
    goodput_norm = float(cfg["rl"]["goodput_norm"])
    throughput_norm = float(cfg["rl"]["throughput_norm"])

    env = LeoEnv(
        config_path=scenario_config,
        queue_norm=queue_norm,
        goodput_norm=goodput_norm,
        throughput_norm=throughput_norm,
    )
    check_env(env, warn=True)

    train_env = Monitor(
        LeoEnv(
            config_path=scenario_config,
            queue_norm=queue_norm,
            goodput_norm=goodput_norm,
            throughput_norm=throughput_norm,
        )
    )

    checkpoint_dir = Path(cfg["paths"]["checkpoint_dir"])
    checkpoint_dir.mkdir(parents=True, exist_ok=True)

    tensorboard_dir = Path(cfg["paths"]["tensorboard_log"])
    tensorboard_dir.mkdir(parents=True, exist_ok=True)

    checkpoint_callback = CheckpointCallback(
        save_freq=10000,
        save_path=str(checkpoint_dir),
        name_prefix="ppo_both_v4",
    )

    model = PPO.load(
        cfg["paths"]["bc_model_path"],
        env=train_env,
        device="cpu",
    )

    model.learn(
        total_timesteps=cfg["train"]["total_timesteps"],
        callback=checkpoint_callback,
        progress_bar=True,
    )

    model.save(cfg["paths"]["model_path"])
    print(f"Modelo final salvo em: {cfg['paths']['model_path']}")


if __name__ == "__main__":
    main()