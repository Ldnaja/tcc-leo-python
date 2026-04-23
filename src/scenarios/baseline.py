from __future__ import annotations

from pathlib import Path
from typing import Dict

import matplotlib.pyplot as plt
import numpy as np
import yaml

from src.allocation.heuristics import allocate_resources
from src.channel.link_model import apply_interference_penalty, beam_quality_db, spectral_efficiency_bps_hz
from src.core.entities import BeamState, UserRequest
from src.core.topology import adjacency_from_distance, hex_layout
from src.metrics.collector import MetricsCollector
from src.traffic.generator import TrafficGenerator


class BaselineScenario:
    def __init__(
        self,
        config_path: str | Path,
        seed_override: int | None = None,
        strategy_override: str | None = None,
    ):
        with open(config_path, "r", encoding="utf-8") as f:
            self.cfg = yaml.safe_load(f)

        if seed_override is not None:
            self.cfg["simulation"]["seed"] = seed_override

        if strategy_override is not None:
            self.cfg["allocation"]["strategy"] = strategy_override

        self.seed = self.cfg["simulation"]["seed"]
        self.strategy = self.cfg["allocation"].get("strategy", "proportional_fair")
        self.step_idx = 0

        self.rng = np.random.default_rng(self.seed)
        self.layout = hex_layout(self.cfg["satellite"]["n_beams"])
        self.adj = adjacency_from_distance(self.layout)
        self.beams: Dict[int, BeamState] = {i: BeamState(beam_id=i) for i in self.layout}
        self.collector = MetricsCollector()

        congestion_cfg = self.cfg.get("congestion", {})
        self.enable_queue_cap = congestion_cfg.get("enable_queue_cap", False)
        self.max_queue_per_beam = congestion_cfg.get("max_queue_per_beam", 100)

        self.enable_timeout = congestion_cfg.get("enable_timeout", False)
        self.max_wait_s = congestion_cfg.get("max_wait_s", 20.0)

        self.history = {
            "time": [],
            "offered_load_mbps": [],
            "accepted_load_mbps": [],
            "capacity_sum_mbps": [],
            "goodput_sum_mbps": [],
            "served_step_mb": [],
            "queue_sum": [],
            "blocked_rate": [],
            "blocked_queue_cap_rate": [],
            "blocked_timeout_rate": [],
            "acceptance_rate": [],
            "service_rate": [],
            "mean_served_delay_s": [],
            "p95_served_delay_s": [],
            "mean_timeout_delay_s": [],
            "utilization": [],
            "fairness": [],
        }

        self.traffic = TrafficGenerator(
            layout=self.layout,
            base_arrival_rate=self.cfg["traffic"]["base_arrival_rate"],
            hotspot_amplitude=self.cfg["traffic"]["hotspot_amplitude"],
            hotspot_period_s=self.cfg["traffic"]["hotspot_period_s"],
            mean_service_demand_mb=self.cfg["traffic"]["mean_service_demand_mb"],
            rng=self.rng,
        )

    def _apply_timeout_drops(self, t: float) -> None:
        if not self.enable_timeout:
            return

        for beam in self.beams.values():
            remaining_backlog = []
            for req in beam.backlog:
                waited_s = t - req.created_at
                if waited_s >= self.max_wait_s:
                    req.blocked = True
                    self.collector.blocked_requests += 1
                    self.collector.blocked_by_timeout += 1
                    self.collector.timeout_delays_s.append(waited_s)
                else:
                    remaining_backlog.append(req)
            beam.backlog = remaining_backlog

    def _admit_arrivals(self, arrivals: Dict[int, list[UserRequest]]) -> tuple[float, float]:
        offered_mb = 0.0
        accepted_mb = 0.0

        for beam_id, new_reqs in arrivals.items():
            self.collector.total_requests += len(new_reqs)

            for req in new_reqs:
                offered_mb += req.demand_mb
                self.collector.total_offered_mb += req.demand_mb

                if self.enable_queue_cap and self.beams[beam_id].queue_len >= self.max_queue_per_beam:
                    req.blocked = True
                    self.collector.blocked_requests += 1
                    self.collector.blocked_by_queue_cap += 1
                    continue

                self.beams[beam_id].backlog.append(req)
                accepted_mb += req.demand_mb
                self.collector.total_accepted_mb += req.demand_mb
                self.collector.accepted_requests += 1

        return offered_mb, accepted_mb

    def step(self, t: float, dt_s: float) -> None:
        arrivals = self.traffic.generate(t, dt_s)
        hotspot_xy = self.traffic.hotspot_position(t)

        self._apply_timeout_drops(t)
        offered_mb, accepted_mb = self._admit_arrivals(arrivals)

        allocate_resources(
            strategy=self.strategy,
            beams=self.beams,
            total_channels=self.cfg["satellite"]["total_channels"],
            total_power_w=self.cfg["satellite"]["total_power_w"],
            max_channels_per_beam=self.cfg["allocation"]["max_channels_per_beam"],
            step_idx=self.step_idx,
        )

        channel_bw = self.cfg["channel"]["channel_bandwidth_hz"]
        min_sinr_db = self.cfg["traffic"]["min_sinr_db"]
        total_channels = self.cfg["satellite"]["total_channels"]

        throughputs = []
        used_channels = 0

        served_step_mb = 0.0

        for beam_id, beam in self.beams.items():
            beam.snr_db = beam_quality_db(
                beam_xy=self.layout[beam_id],
                hotspot_xy=hotspot_xy,
                base_snr_db=self.cfg["channel"]["base_snr_db"],
                edge_loss_db=self.cfg["channel"]["edge_loss_db"],
            )

            neighbor_allocs = [self.beams[n].allocated_channels for n in self.adj[beam_id]]
            beam.sinr_db = apply_interference_penalty(
                snr_db=beam.snr_db,
                allocated_channels=beam.allocated_channels,
                neighbor_allocations=neighbor_allocs,
                interference_penalty_db=self.cfg["channel"]["interference_penalty_db"],
            )

            se = spectral_efficiency_bps_hz(beam.sinr_db)
            beam.throughput_mbps = (se * channel_bw * beam.allocated_channels) / 1e6

            used_channels += beam.allocated_channels
            throughputs.append(beam.throughput_mbps)

            if beam.queue_len == 0 or beam.allocated_channels == 0:
                continue

            if beam.sinr_db < min_sinr_db:
                n_block = min(len(beam.backlog), max(1, beam.queue_len // 4))
                for _ in range(n_block):
                    req = beam.backlog.pop(0)
                    req.blocked = True
                    self.collector.blocked_requests += 1
                continue

            capacity_mb = beam.throughput_mbps * dt_s / 8.0

            while beam.backlog and capacity_mb > 0:
                req = beam.backlog[0]
                served_now = min(req.remaining_mb, capacity_mb)
                req.remaining_mb -= served_now
                capacity_mb -= served_now
                self.collector.total_served_mb += served_now
                served_step_mb += served_now

                if req.remaining_mb <= 1e-9:
                    req.served = True
                    self.collector.served_requests += 1
                    self.collector.served_delays_s.append(t + dt_s - req.created_at)
                    beam.backlog.pop(0)

        utilization = used_channels / total_channels if total_channels > 0 else 0.0
        fairness = self.collector.jain_fairness([x for x in throughputs if x > 0])

        blocked_rate = self.collector.blocked_requests / max(1, self.collector.total_requests)
        blocked_queue_cap_rate = self.collector.blocked_by_queue_cap / max(1, self.collector.total_requests)
        blocked_timeout_rate = self.collector.blocked_by_timeout / max(1, self.collector.total_requests)

        acceptance_rate = self.collector.accepted_requests / max(1, self.collector.total_requests)
        service_rate = self.collector.served_requests / max(1, self.collector.total_requests)

        mean_served_delay_s = self.collector.mean_or_zero(self.collector.served_delays_s)
        p95_served_delay_s = self.collector.percentile_or_zero(self.collector.served_delays_s, 95)
        mean_timeout_delay_s = self.collector.mean_or_zero(self.collector.timeout_delays_s)

        offered_load_mbps = (offered_mb * 8.0) / dt_s
        accepted_load_mbps = (accepted_mb * 8.0) / dt_s
        capacity_sum_mbps = sum(throughputs)
        goodput_sum_mbps = (served_step_mb * 8.0) / dt_s

        self.history["time"].append(t)
        self.history["offered_load_mbps"].append(offered_load_mbps)
        self.history["accepted_load_mbps"].append(accepted_load_mbps)
        self.history["capacity_sum_mbps"].append(capacity_sum_mbps)
        self.history["goodput_sum_mbps"].append(goodput_sum_mbps)
        self.history["served_step_mb"].append(served_step_mb)
        self.history["queue_sum"].append(sum(beam.queue_len for beam in self.beams.values()))
        self.history["blocked_rate"].append(blocked_rate)
        self.history["blocked_queue_cap_rate"].append(blocked_queue_cap_rate)
        self.history["blocked_timeout_rate"].append(blocked_timeout_rate)
        self.history["utilization"].append(utilization)
        self.history["fairness"].append(fairness)
        self.history["acceptance_rate"].append(acceptance_rate)
        self.history["service_rate"].append(service_rate)
        self.history["mean_served_delay_s"].append(mean_served_delay_s)
        self.history["p95_served_delay_s"].append(p95_served_delay_s)
        self.history["mean_timeout_delay_s"].append(mean_timeout_delay_s)

        self.step_idx += 1

    def run(self) -> dict:
        duration_s = self.cfg["simulation"]["duration_s"]
        dt_s = self.cfg["simulation"]["dt_s"]
        t = 0.0
        while t < duration_s:
            self.step(t, dt_s)
            t += dt_s
        return self.history

    def save_plots(self, out_dir: str | Path) -> None:
        out_dir = Path(out_dir)
        out_dir.mkdir(parents=True, exist_ok=True)

        series = [
            ("capacity_sum_mbps", "Capacidade alocada total (Mbps)"),
            ("goodput_sum_mbps", "Goodput real total (Mbps)"),
            ("queue_sum", "Fila total"),
            ("blocked_rate", "Taxa de bloqueio acumulada"),
            ("blocked_queue_cap_rate", "Bloqueio acumulado por fila máxima"),
            ("blocked_timeout_rate", "Bloqueio acumulado por timeout"),
            ("utilization", "Utilização de canais"),
            ("fairness", "Jain fairness"),
            ("acceptance_rate", "Taxa de aceitação"),
            ("service_rate", "Taxa de serviço"),
            ("mean_served_delay_s", "Atraso médio servido (s)"),
            ("p95_served_delay_s", "P95 atraso servido (s)"),
            ("mean_timeout_delay_s", "Atraso médio de timeout (s)"),
        ]

        for key, ylabel in series:
            plt.figure(figsize=(8, 4))
            plt.plot(self.history["time"], self.history[key])
            plt.xlabel("Tempo (s)")
            plt.ylabel(ylabel)
            plt.grid(True, alpha=0.3)
            plt.tight_layout()
            plt.savefig(out_dir / f"{key}.png", dpi=150)
            plt.close()

        plt.figure(figsize=(8, 4))
        plt.plot(self.history["time"], self.history["offered_load_mbps"], label="Carga oferecida (Mbps)")
        plt.plot(self.history["time"], self.history["accepted_load_mbps"], label="Carga aceita (Mbps)")
        plt.plot(self.history["time"], self.history["capacity_sum_mbps"], label="Capacidade alocada (Mbps)")
        plt.plot(self.history["time"], self.history["goodput_sum_mbps"], label="Goodput real (Mbps)")
        plt.xlabel("Tempo (s)")
        plt.ylabel("Mbps")
        plt.grid(True, alpha=0.3)
        plt.legend()
        plt.tight_layout()
        plt.savefig(out_dir / "load_vs_goodput.png", dpi=150)
        plt.close()