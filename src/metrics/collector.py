from __future__ import annotations

from dataclasses import dataclass, field
from typing import List


@dataclass
class MetricsCollector:
    total_requests: int = 0
    accepted_requests: int = 0
    blocked_requests: int = 0
    blocked_by_queue_cap: int = 0
    blocked_by_timeout: int = 0
    served_requests: int = 0

    total_served_mb: float = 0.0
    total_offered_mb: float = 0.0
    total_accepted_mb: float = 0.0

    served_delays_s: List[float] = field(default_factory=list)
    timeout_delays_s: List[float] = field(default_factory=list)

    def jain_fairness(self, xs: List[float]) -> float:
        if not xs or sum(xs) == 0:
            return 0.0
        return (sum(xs) ** 2) / (len(xs) * sum(x * x for x in xs))

    def mean_or_zero(self, xs: List[float]) -> float:
        return sum(xs) / len(xs) if xs else 0.0

    def percentile_or_zero(self, xs: List[float], q: float) -> float:
        if not xs:
            return 0.0
        xs_sorted = sorted(xs)
        idx = min(len(xs_sorted) - 1, max(0, int(round((q / 100.0) * (len(xs_sorted) - 1)))))
        return xs_sorted[idx]