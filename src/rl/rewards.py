from __future__ import annotations


def compute_reward(step_info: dict, queue_norm: float = 100.0, goodput_norm: float = 250.0) -> tuple[float, dict]:
    goodput_term = min(step_info["goodput_sum_mbps"] / goodput_norm, 2.0)
    blocked_term = min(step_info["blocked_step_ratio"], 1.0)
    queue_term = min(step_info["queue_sum"] / queue_norm, 2.0)
    delay_term = min(step_info["step_mean_served_delay_s"] / 40.0, 1.0)
    fairness_term = step_info["fairness"]

    reward = (
        1.00 * goodput_term
        - 0.80 * blocked_term
        - 0.25 * queue_term
        - 0.15 * delay_term
        + 0.05 * fairness_term
    )

    terms = {
        "goodput_term": goodput_term,
        "blocked_term": blocked_term,
        "queue_term": queue_term,
        "delay_term": delay_term,
        "fairness_term": fairness_term,
        "reward": reward,
    }
    return float(reward), terms