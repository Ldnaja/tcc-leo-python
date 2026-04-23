from __future__ import annotations

from typing import Dict, List, Tuple


def beam_quality_db(
    beam_xy: Tuple[float, float],
    hotspot_xy: Tuple[float, float],
    base_snr_db: float,
    edge_loss_db: float,
) -> float:
    dx = beam_xy[0] - hotspot_xy[0]
    dy = beam_xy[1] - hotspot_xy[1]
    radius = (dx * dx + dy * dy) ** 0.5
    normalized = min(radius / 2.0, 1.0)
    return base_snr_db - edge_loss_db * normalized


def apply_interference_penalty(
    snr_db: float,
    allocated_channels: int,
    neighbor_allocations: List[int],
    interference_penalty_db: float,
) -> float:
    if allocated_channels == 0:
        return -100.0
    active_neighbors = sum(1 for x in neighbor_allocations if x > 0)
    return snr_db - interference_penalty_db * (active_neighbors / max(1, len(neighbor_allocations)))


def spectral_efficiency_bps_hz(sinr_db: float) -> float:
    # Shannon-like clipped approximation
    if sinr_db <= -20:
        return 0.0
    sinr_linear = 10 ** (sinr_db / 10.0)
    eff = max(0.0, min(7.5, __import__("math").log2(1.0 + sinr_linear)))
    return eff
