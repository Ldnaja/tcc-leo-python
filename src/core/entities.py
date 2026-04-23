from __future__ import annotations

from dataclasses import dataclass, field
from typing import List


@dataclass
class UserRequest:
    request_id: int
    beam_id: int
    demand_mb: float
    created_at: float
    remaining_mb: float
    served: bool = False
    blocked: bool = False


@dataclass
class BeamState:
    beam_id: int
    backlog: List[UserRequest] = field(default_factory=list)
    allocated_channels: int = 0
    allocated_power_w: float = 0.0
    snr_db: float = 0.0
    sinr_db: float = 0.0
    throughput_mbps: float = 0.0

    @property
    def queue_len(self) -> int:
        return len(self.backlog)
