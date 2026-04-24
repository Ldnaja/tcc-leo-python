from __future__ import annotations

from typing import Dict

import numpy as np

from src.core.entities import BeamState


def _reset_allocations(beams: Dict[int, BeamState]) -> None:
    for beam in beams.values():
        beam.allocated_channels = 0
        beam.allocated_power_w = 0.0


def _distribute_power(beams: Dict[int, BeamState], total_power_w: float) -> None:
    total_alloc = sum(beam.allocated_channels for beam in beams.values())
    if total_alloc <= 0:
        for beam in beams.values():
            beam.allocated_power_w = 0.0
        return

    for beam in beams.values():
        if beam.allocated_channels > 0:
            beam.allocated_power_w = total_power_w * (beam.allocated_channels / total_alloc)
        else:
            beam.allocated_power_w = 0.0


def allocate_by_priority(
    beams: Dict[int, BeamState],
    priorities: np.ndarray,
    total_channels: int,
    total_power_w: float,
    max_channels_per_beam: int,
) -> None:
    _reset_allocations(beams)

    beam_ids = sorted(beams.keys())
    priorities = np.asarray(priorities, dtype=np.float32).reshape(-1)

    if priorities.size != len(beam_ids):
        raise ValueError(
            f"Ação inválida: esperado vetor de tamanho {len(beam_ids)}, recebido {priorities.size}."
        )

    active_mask = np.array([1.0 if beams[b].queue_len > 0 else 0.0 for b in beam_ids], dtype=np.float32)

    if active_mask.sum() == 0 or total_channels <= 0:
        return

    logits = np.clip(priorities, -10.0, 10.0)
    weights = np.exp(logits - np.max(logits))
    weights *= active_mask

    if weights.sum() <= 0:
        weights = np.array([max(float(beams[b].queue_len), 0.0) for b in beam_ids], dtype=np.float32)
        weights *= active_mask

    if weights.sum() <= 0:
        return

    weights = weights / weights.sum()
    quotas = weights * total_channels

    alloc = np.floor(quotas).astype(int)
    alloc = np.minimum(alloc, max_channels_per_beam)

    channels_used = int(alloc.sum())
    channels_left = total_channels - channels_used

    residual = quotas - alloc

    while channels_left > 0:
        candidates = [
            i for i, beam_id in enumerate(beam_ids)
            if beams[beam_id].queue_len > 0 and alloc[i] < max_channels_per_beam
        ]
        if not candidates:
            break

        best_idx = max(candidates, key=lambda i: residual[i])
        alloc[best_idx] += 1
        residual[best_idx] = 0.0
        channels_left -= 1

    for i, beam_id in enumerate(beam_ids):
        beams[beam_id].allocated_channels = int(alloc[i])

    _distribute_power(beams, total_power_w)