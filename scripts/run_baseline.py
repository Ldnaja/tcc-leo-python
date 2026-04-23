from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.scenarios.baseline import BaselineScenario


def main() -> None:
    parser = argparse.ArgumentParser(description="Executa o cenário baseline NTN LEO.")
    parser.add_argument(
        "--config",
        type=str,
        default="configs/baseline.yaml",
        help="Caminho para o arquivo YAML de configuração.",
    )
    parser.add_argument(
        "--outdir",
        type=str,
        default=None,
        help="Diretório de saída dos resultados. Se omitido, usa results/<nome_do_config>.",
    )
    args = parser.parse_args()

    config_path = Path(args.config)
    if not config_path.exists():
        raise FileNotFoundError(f"Arquivo de configuração não encontrado: {config_path}")

    scenario = BaselineScenario(config_path=config_path)
    history = scenario.run()

    config_name = config_path.stem
    out_dir = Path(args.outdir) if args.outdir else Path("results") / config_name
    out_dir.mkdir(parents=True, exist_ok=True)

    scenario.save_plots(out_dir)

    df = pd.DataFrame(history)
    df.to_csv(out_dir / "history.csv", index=False)

    avg_offered = sum(history["offered_load_mbps"]) / max(1, len(history["offered_load_mbps"]))
    avg_accepted = sum(history["accepted_load_mbps"]) / max(1, len(history["accepted_load_mbps"]))
    avg_capacity = sum(history["capacity_sum_mbps"]) / max(1, len(history["capacity_sum_mbps"]))
    avg_goodput = sum(history["goodput_sum_mbps"]) / max(1, len(history["goodput_sum_mbps"]))

    final_capacity = history["capacity_sum_mbps"][-1] if history["capacity_sum_mbps"] else 0.0
    final_goodput = history["goodput_sum_mbps"][-1] if history["goodput_sum_mbps"] else 0.0
    final_queue = history["queue_sum"][-1] if history["queue_sum"] else 0
    final_blocked = history["blocked_rate"][-1] if history["blocked_rate"] else 0.0
    final_blocked_queue_cap = history["blocked_queue_cap_rate"][-1] if history["blocked_queue_cap_rate"] else 0.0
    final_blocked_timeout = history["blocked_timeout_rate"][-1] if history["blocked_timeout_rate"] else 0.0
    final_utilization = history["utilization"][-1] if history["utilization"] else 0.0
    final_fairness = history["fairness"][-1] if history["fairness"] else 0.0

    summary = {
        "config": str(config_path),
        "samples": len(history["time"]),
        "avg_offered_load_mbps": avg_offered,
        "avg_accepted_load_mbps": avg_accepted,
        "avg_capacity_mbps": avg_capacity,
        "avg_goodput_mbps": avg_goodput,
        "final_capacity_mbps": final_capacity,
        "final_goodput_mbps": final_goodput,
        "final_queue": final_queue,
        "final_blocked_rate": final_blocked,
        "final_blocked_queue_cap_rate": final_blocked_queue_cap,
        "final_blocked_timeout_rate": final_blocked_timeout,
        "final_utilization": final_utilization,
        "final_fairness": final_fairness,
    }

    with open(out_dir / "summary.json", "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)

    with open(out_dir / "summary.txt", "w", encoding="utf-8") as f:
        f.write("--- RESUMO ---\n")
        f.write(f"Config utilizada: {config_path}\n")
        f.write(f"Amostras: {len(history['time'])}\n")
        f.write(f"Carga oferecida média (Mbps): {avg_offered:.2f}\n")
        f.write(f"Carga aceita média (Mbps): {avg_accepted:.2f}\n")
        f.write(f"Capacidade alocada média (Mbps): {avg_capacity:.2f}\n")
        f.write(f"Goodput real médio (Mbps): {avg_goodput:.2f}\n")
        f.write(f"Capacidade alocada final (Mbps): {final_capacity:.2f}\n")
        f.write(f"Goodput real final (Mbps): {final_goodput:.2f}\n")
        f.write(f"Fila final: {final_queue}\n")
        f.write(f"Bloqueio acumulado total: {final_blocked:.4f}\n")
        f.write(f"Bloqueio acumulado por fila máxima: {final_blocked_queue_cap:.4f}\n")
        f.write(f"Bloqueio acumulado por timeout: {final_blocked_timeout:.4f}\n")
        f.write(f"Utilização final: {final_utilization:.4f}\n")
        f.write(f"Fairness final: {final_fairness:.4f}\n")
        f.write(f"Resultados em: {out_dir.resolve()}\n")

    print("--- RESUMO ---")
    print(f"Config utilizada: {config_path}")
    print(f"Amostras: {len(history['time'])}")
    print(f"Carga oferecida média (Mbps): {avg_offered:.2f}")
    print(f"Carga aceita média (Mbps): {avg_accepted:.2f}")
    print(f"Capacidade alocada média (Mbps): {avg_capacity:.2f}")
    print(f"Goodput real médio (Mbps): {avg_goodput:.2f}")
    print(f"Capacidade alocada final (Mbps): {final_capacity:.2f}")
    print(f"Goodput real final (Mbps): {final_goodput:.2f}")
    print(f"Fila final: {final_queue}")
    print(f"Bloqueio acumulado total: {final_blocked:.4f}")
    print(f"Bloqueio acumulado por fila máxima: {final_blocked_queue_cap:.4f}")
    print(f"Bloqueio acumulado por timeout: {final_blocked_timeout:.4f}")
    print(f"Utilização final: {final_utilization:.4f}")
    print(f"Fairness final: {final_fairness:.4f}")
    print(f"Resultados em: {out_dir.resolve()}")


if __name__ == "__main__":
    main()