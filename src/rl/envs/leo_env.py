from __future__ import annotations

from pathlib import Path

import gymnasium as gym
import numpy as np
import yaml
from gymnasium import spaces

from src.rl.rewards import compute_reward
from src.scenarios.baseline import BaselineScenario


class LeoEnv(gym.Env):
    metadata = {"render_modes": []}

    def __init__(
        self,
        config_path: str | Path,
        queue_norm: float = 100.0,
        goodput_norm: float = 250.0,
        throughput_norm: float = 50.0,
    ):
        super().__init__()

        self.config_path = Path(config_path)
        with open(self.config_path, "r", encoding="utf-8") as f:
            self.cfg = yaml.safe_load(f)

        self.n_beams = int(self.cfg["satellite"]["n_beams"])
        self.dt_s = float(self.cfg["simulation"]["dt_s"])
        self.duration_s = float(self.cfg["simulation"]["duration_s"])
        self.max_steps = int(self.duration_s / self.dt_s)

        self.max_channels_per_beam = int(self.cfg["allocation"]["max_channels_per_beam"])

        self.queue_norm = float(queue_norm)
        self.goodput_norm = float(goodput_norm)
        self.throughput_norm = float(throughput_norm)

        obs_dim = self.n_beams * 4 + 4

        self.observation_space = spaces.Box(
            low=0.0,
            high=1.0,
            shape=(obs_dim,),
            dtype=np.float32,
        )

        self.action_space = spaces.Box(
            low=-1.0,
            high=1.0,
            shape=(self.n_beams,),
            dtype=np.float32,
        )

        self.scenario: BaselineScenario | None = None
        self.current_step = 0
        self.current_time = 0.0
        self.last_step_info: dict = {}

    def _norm_db(self, value: float, min_db: float = -10.0, max_db: float = 30.0) -> float:
        value = max(min(value, max_db), min_db)
        return (value - min_db) / (max_db - min_db)

    def _get_obs(self) -> np.ndarray:
        assert self.scenario is not None

        beam_ids = sorted(self.scenario.beams.keys())

        queue_feats = []
        alloc_feats = []
        sinr_feats = []
        thr_feats = []

        for beam_id in beam_ids:
            beam = self.scenario.beams[beam_id]
            queue_feats.append(min(beam.queue_len / self.queue_norm, 1.0))
            alloc_feats.append(min(beam.allocated_channels / max(1, self.max_channels_per_beam), 1.0))
            sinr_feats.append(self._norm_db(getattr(beam, "sinr_db", 0.0)))
            thr_feats.append(min(getattr(beam, "throughput_mbps", 0.0) / self.throughput_norm, 1.0))

        global_feats = [
            min(sum(beam.queue_len for beam in self.scenario.beams.values()) / (self.n_beams * self.queue_norm), 1.0),
            min(self.last_step_info.get("goodput_sum_mbps", 0.0) / self.goodput_norm, 1.0),
            min(self.last_step_info.get("blocked_step_ratio", 0.0), 1.0),
            min(self.last_step_info.get("utilization", 0.0), 1.0),
        ]

        obs = np.array(queue_feats + alloc_feats + sinr_feats + thr_feats + global_feats, dtype=np.float32)
        return obs

    def reset(self, *, seed: int | None = None, options: dict | None = None):
        super().reset(seed=seed)

        if seed is not None:
            chosen_seed = int(seed)
        else:
            chosen_seed = int(self.np_random.integers(0, 1_000_000))

        self.scenario = BaselineScenario(
            config_path=self.config_path,
            seed_override=chosen_seed,
            strategy_override=None,
        )
        self.current_step = 0
        self.current_time = 0.0
        self.last_step_info = {}

        obs = self._get_obs()
        info = {"seed": chosen_seed}
        return obs, info

    def step(self, action: np.ndarray):
        assert self.scenario is not None

        step_info = self.scenario.step(
            t=self.current_time,
            dt_s=self.dt_s,
            external_action=action,
        )

        reward, reward_terms = compute_reward(
            step_info=step_info,
            queue_norm=self.queue_norm,
            goodput_norm=self.goodput_norm,
        )

        self.last_step_info = step_info
        self.current_step += 1
        self.current_time += self.dt_s

        terminated = False
        truncated = self.current_step >= self.max_steps

        obs = self._get_obs()
        info = {**step_info, **reward_terms}

        return obs, reward, terminated, truncated, info