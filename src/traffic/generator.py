from __future__ import annotations

import math
from typing import Dict, Tuple

import numpy as np

from src.core.entities import UserRequest


class TrafficGenerator:
    def __init__(
        self,
        layout: Dict[int, Tuple[float, float]],
        base_arrival_rate: float,
        hotspot_amplitude: float,
        hotspot_period_s: float,
        mean_service_demand_mb: float,
        rng: np.random.Generator,
    ) -> None:
        self.layout = layout
        self.base_arrival_rate = base_arrival_rate
        self.hotspot_amplitude = hotspot_amplitude
        self.hotspot_period_s = hotspot_period_s
        self.mean_service_demand_mb = mean_service_demand_mb
        self.rng = rng
        self.request_counter = 0

    def hotspot_position(self, t: float) -> Tuple[float, float]:
        angle = 2.0 * math.pi * (t / self.hotspot_period_s)
        return 1.4 * math.cos(angle), 1.0 * math.sin(angle)

    def beam_load_factor(self, beam_xy: Tuple[float, float], hotspot_xy: Tuple[float, float]) -> float:
        dx = beam_xy[0] - hotspot_xy[0]
        dy = beam_xy[1] - hotspot_xy[1]
        d2 = dx * dx + dy * dy
        return 1.0 + self.hotspot_amplitude * math.exp(-d2 / 1.5)

    def generate(self, t: float, dt_s: float) -> Dict[int, list[UserRequest]]:
        arrivals: Dict[int, list[UserRequest]] = {beam_id: [] for beam_id in self.layout}
        hotspot = self.hotspot_position(t)
        for beam_id, xy in self.layout.items():
            lam = self.base_arrival_rate * self.beam_load_factor(xy, hotspot) * dt_s
            n_arrivals = self.rng.poisson(lam)
            for _ in range(n_arrivals):
                self.request_counter += 1
                demand_mb = max(1.0, self.rng.exponential(self.mean_service_demand_mb))
                arrivals[beam_id].append(
                    UserRequest(
                        request_id=self.request_counter,
                        beam_id=beam_id,
                        demand_mb=demand_mb,
                        remaining_mb=demand_mb,
                        created_at=t,
                    )
                )
        return arrivals
