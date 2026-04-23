from __future__ import annotations

from typing import Dict, List, Tuple


def hex_layout(n_beams: int) -> Dict[int, Tuple[float, float]]:
    """Returns a small fixed hex-like footprint for 19 beams.
    Coordinates are normalized and only used to create spatial demand dynamics.
    """
    if n_beams != 19:
        raise ValueError("This starter version supports 19 beams.")

    coords = [
        (0.0, 0.0),
        (1.0, 0.0), (0.5, 0.866), (-0.5, 0.866), (-1.0, 0.0), (-0.5, -0.866), (0.5, -0.866),
        (2.0, 0.0), (1.5, 0.866), (1.0, 1.732), (0.0, 1.732), (-1.0, 1.732),
        (-1.5, 0.866), (-2.0, 0.0), (-1.5, -0.866), (-1.0, -1.732), (0.0, -1.732),
        (1.0, -1.732), (1.5, -0.866),
    ]
    return {i: coords[i] for i in range(n_beams)}


def adjacency_from_distance(layout: Dict[int, Tuple[float, float]], threshold: float = 1.05) -> Dict[int, List[int]]:
    adj: Dict[int, List[int]] = {beam_id: [] for beam_id in layout}
    items = list(layout.items())
    for i, (beam_i, (xi, yi)) in enumerate(items):
        for beam_j, (xj, yj) in items[i + 1 :]:
            d = ((xi - xj) ** 2 + (yi - yj) ** 2) ** 0.5
            if d <= threshold:
                adj[beam_i].append(beam_j)
                adj[beam_j].append(beam_i)
    return adj
