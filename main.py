import argparse
import json
import logging
import yaml
import pandas as pd
from datetime import datetime
from pathlib import Path

from core.generador import generar_clientes
from core.inyector_errores import inyectar_errores
from core.validador import validar_clientes


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%d/%m/%Y %H:%M:%S"
)
log = logging.getLogger(__name__)

ruta_configuracion = Path("configuracion/global.yaml")
ruta_archivos = Path("output/archivos")
ruta_reportes = Path("output/reportes")


def _cargar_config() -> dict:

    with open(ruta_configuracion) as f:
        return yaml.safe_load(f)


def _parsear_args(config: dict) -> argparse.Namespace:

    parser = argparse.ArgumentParser(description="TDM Data Sintética — Generador de clientes")
    parser.add_argument("--n", type=int, default=config["registros"], help="Número de registros")
    parser.add_argument("--seed", type=int, default=config["seed"], help="Semilla de reproducibilidad")
    parser.add_argument("--error_rate", type=float, default=config["error_rate"], help="Tasa de error (0-1)")
    parser.add_argument("--formato", type=str, default=config["formato"], choices=["csv", "json"], help="Formato de salida")
    return parser.parse_args()


def _nombre_archivo(seed: int, formato: str) -> str:

    timestamp = datetime.now().strftime("%Y%m%d_%H%M")
    return f"clientes_{timestamp}_seed{seed}.{formato}"


def _exportar(clientes: list[dict], args: argparse.Namespace) -> Path:

    ruta_archivos.mkdir(exist_ok=True)
    nombre = _nombre_archivo(args.seed, args.formato)
    ruta = ruta_archivos / nombre

    if args.formato == "csv":
        pd.DataFrame(clientes).to_csv(ruta, index=False, encoding="utf-8")
    else:
        with open(ruta, "w", encoding="utf-8") as f:
            json.dump(clientes, f, ensure_ascii=False, indent=2)

    return ruta


def _exportar_reporte(reporte: dict, seed: int) -> Path:

    ruta_reportes.mkdir(exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M")
    ruta = ruta_reportes / f"reporte_{timestamp}_seed{seed}.json"

    with open(ruta, "w", encoding="utf-8") as f:
        json.dump(reporte, f, ensure_ascii=False, indent=2)

    return ruta


def main():
    config = _cargar_config()
    args = _parsear_args(config)

    log.info("=== Iniciando pipeline TDM Data Sintética ===")
    log.info(f"Parámetros: n={args.n}, seed={args.seed}, error_rate={args.error_rate}, formato={args.formato}")

    # 1. Generar clientes
    log.info(f"Generando {args.n} clientes sintéticos...")
    clientes = generar_clientes(n=args.n, seed=args.seed)
    log.info(f"{len(clientes)} clientes generados correctamente")

    # 2. Inyectar errores
    log.info(f"Inyectando errores con error_rate={args.error_rate}...")
    clientes_con_errores = inyectar_errores(
        clientes=clientes,
        error_rate=args.error_rate,
        seed=args.seed
    )
    n_errores = sum(1 for c in clientes_con_errores if "tipo_error" in c)
    log.info(f"{n_errores} errores inyectados")

    # 3. Validar
    log.info("Validando dataset...")
    reporte = validar_clientes(clientes_con_errores)
    log.info(f"Cumplimiento: {reporte['porcentaje_cumplimiento']}%")
    log.info(f"Errores detectados: {reporte['errores_totales']}")

    # 4. Exportar dataset
    ruta_dataset = _exportar(clientes_con_errores, args)
    log.info(f"Dataset exportado: {ruta_dataset}")

    # 5. Exportar reporte
    ruta_reporte = _exportar_reporte(reporte, args.seed)
    log.info(f"Reporte exportado: {ruta_reporte}")

    log.info("=== Pipeline finalizado ===")


if __name__ == "__main__":
    main()