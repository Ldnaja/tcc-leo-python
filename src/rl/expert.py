from __future__ import annotations

import copy
from typing import Dict

import numpy as np

from src.allocation.heuristics import allocate_resources
from src.core.entities import BeamState


def expert_action_greedy_backlog(
    beams: Dict[int, BeamState],
    total_channels: int,
    total_power_w: float,
    max_channels_per_beam: int,
) -> np.ndarray:
    beam_ids = sorted(beams.keys())
    beams_copy = copy.deepcopy(beams)

    allocate_resources(
        strategy="greedy_backlog",
        beams=beams_copy,
        total_channels=total_channels,
        total_power_w=total_power_w,
        max_channels_per_beam=max_channels_per_beam,
        step_idx=0,
    )

    alloc = np.array([beams_copy[b].allocated_channels for b in beam_ids], dtype=np.float32)

    if alloc.sum() <= 0:
        return np.zeros(len(beam_ids), dtype=np.float32)

    logits = np.where(alloc > 0, np.log1p(alloc), -4.0).astype(np.float32)
    logits = logits - logits.mean()

    max_abs = np.max(np.abs(logits))
    if max_abs > 0:
        logits = logits / max_abs

    logits = np.clip(logits, -1.0, 1.0)
    return logits.astype(np.float32)