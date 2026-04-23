from __future__ import annotations

from typing import Dict

from src.core.entities import BeamState


def _reset_allocations(beams: Dict[int, BeamState]) -> None:
    for beam in beams.values():
        beam.allocated_channels = 0
        beam.allocated_power_w = 0.0


def _active_beam_ids(beams: Dict[int, BeamState]) -> list[int]:
    return [beam_id for beam_id, beam in beams.items() if beam.queue_len > 0]


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


def proportional_fair_allocate(
    beams: Dict[int, BeamState],
    total_channels: int,
    total_power_w: float,
    max_channels_per_beam: int,
) -> None:
    _reset_allocations(beams)
    active = _active_beam_ids(beams)

    if not active or total_channels <= 0:
        return

    channels_left = total_channels

    while channels_left > 0:
        candidates = [
            beam_id
            for beam_id in active
            if beams[beam_id].allocated_channels < max_channels_per_beam
        ]
        if not candidates:
            break

        best_beam = max(
            candidates,
            key=lambda b: beams[b].queue_len / (1.0 + beams[b].allocated_channels),
        )
        beams[best_beam].allocated_channels += 1
        channels_left -= 1

    _distribute_power(beams, total_power_w)


def round_robin_allocate(
    beams: Dict[int, BeamState],
    total_channels: int,
    total_power_w: float,
    max_channels_per_beam: int,
    step_idx: int = 0,
) -> None:
    _reset_allocations(beams)
    active = sorted(_active_beam_ids(beams))

    if not active or total_channels <= 0:
        return

    shift = step_idx % len(active)
    order = active[shift:] + active[:shift]

    channels_left = total_channels
    while channels_left > 0:
        progress = False
        for beam_id in order:
            if beams[beam_id].allocated_channels < max_channels_per_beam:
                beams[beam_id].allocated_channels += 1
                channels_left -= 1
                progress = True
                if channels_left == 0:
                    break
        if not progress:
            break

    _distribute_power(beams, total_power_w)


def longest_queue_first_allocate(
    beams: Dict[int, BeamState],
    total_channels: int,
    total_power_w: float,
    max_channels_per_beam: int,
) -> None:
    _reset_allocations(beams)
    active = _active_beam_ids(beams)

    if not active or total_channels <= 0:
        return

    order = sorted(active, key=lambda b: beams[b].queue_len, reverse=True)

    channels_left = total_channels
    while channels_left > 0:
        progress = False
        for beam_id in order:
            if beams[beam_id].allocated_channels < max_channels_per_beam:
                beams[beam_id].allocated_channels += 1
                channels_left -= 1
                progress = True
                if channels_left == 0:
                    break
        if not progress:
            break

    _distribute_power(beams, total_power_w)


def greedy_backlog_allocate(
    beams: Dict[int, BeamState],
    total_channels: int,
    total_power_w: float,
    max_channels_per_beam: int,
) -> None:
    _reset_allocations(beams)
    active = _active_beam_ids(beams)

    if not active or total_channels <= 0:
        return

    order = sorted(active, key=lambda b: beams[b].queue_len, reverse=True)

    channels_left = total_channels
    for beam_id in order:
        if channels_left <= 0:
            break

        alloc = min(max_channels_per_beam, channels_left)
        beams[beam_id].allocated_channels = alloc
        channels_left -= alloc

    _distribute_power(beams, total_power_w)


def allocate_resources(
    strategy: str,
    beams: Dict[int, BeamState],
    total_channels: int,
    total_power_w: float,
    max_channels_per_beam: int,
    step_idx: int = 0,
) -> None:
    if strategy == "proportional_fair":
        proportional_fair_allocate(
            beams=beams,
            total_channels=total_channels,
            total_power_w=total_power_w,
            max_channels_per_beam=max_channels_per_beam,
        )
        return

    if strategy == "round_robin":
        round_robin_allocate(
            beams=beams,
            total_channels=total_channels,
            total_power_w=total_power_w,
            max_channels_per_beam=max_channels_per_beam,
            step_idx=step_idx,
        )
        return

    if strategy == "longest_queue_first":
        longest_queue_first_allocate(
            beams=beams,
            total_channels=total_channels,
            total_power_w=total_power_w,
            max_channels_per_beam=max_channels_per_beam,
        )
        return

    if strategy == "greedy_backlog":
        greedy_backlog_allocate(
            beams=beams,
            total_channels=total_channels,
            total_power_w=total_power_w,
            max_channels_per_beam=max_channels_per_beam,
        )
        return

    raise ValueError(f"Estratégia de alocação desconhecida: {strategy}")