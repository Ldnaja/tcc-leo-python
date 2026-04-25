from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import torch
import torch.nn.functional as F
import yaml
from torch.utils.data import DataLoader, TensorDataset
from stable_baselines3 import PPO
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

    dataset = np.load(cfg["expert"]["dataset_path"])
    obs = dataset["observations"]
    actions = dataset["actions"]

    train_env = Monitor(
        LeoEnv(
            config_path=scenario_config,
            queue_norm=queue_norm,
            goodput_norm=goodput_norm,
            throughput_norm=throughput_norm,
        )
    )

    device = "cpu"

    model = PPO(
        policy="MlpPolicy",
        env=train_env,
        learning_rate=cfg["train"]["learning_rate"],
        n_steps=cfg["train"]["n_steps"],
        batch_size=cfg["train"]["batch_size"],
        gamma=cfg["train"]["gamma"],
        gae_lambda=cfg["train"]["gae_lambda"],
        ent_coef=cfg["train"]["ent_coef"],
        vf_coef=cfg["train"]["vf_coef"],
        verbose=1,
        tensorboard_log=str(cfg["paths"]["tensorboard_log"]),
        device=device,
        seed=cfg["train"]["seed"],
    )

    model.policy.train()

    x = torch.tensor(obs, dtype=torch.float32)
    y = torch.tensor(actions, dtype=torch.float32)

    loader = DataLoader(
        TensorDataset(x, y),
        batch_size=cfg["bc"]["batch_size"],
        shuffle=True,
    )

    optimizer = torch.optim.Adam(model.policy.parameters(), lr=cfg["bc"]["learning_rate"])

    for epoch in range(cfg["bc"]["epochs"]):
        losses = []

        for batch_obs, batch_actions in loader:
            batch_obs = batch_obs.to(device)
            batch_actions = batch_actions.to(device)

            dist = model.policy.get_distribution(batch_obs)
            pred_actions = dist.distribution.mean

            loss = F.mse_loss(pred_actions, batch_actions)

            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

            losses.append(loss.item())

        mean_loss = float(np.mean(losses)) if losses else 0.0
        print(f"Epoch {epoch + 1}/{cfg['bc']['epochs']} - bc_loss={mean_loss:.6f}")

    bc_model_path = Path(cfg["paths"]["bc_model_path"])
    bc_model_path.parent.mkdir(parents=True, exist_ok=True)
    model.save(str(bc_model_path))
    print(f"Modelo BC salvo em: {bc_model_path}")


if __name__ == "__main__":
    main()