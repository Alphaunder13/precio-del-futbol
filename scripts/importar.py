"""Importador atómico.

Valida todo en memoria, escribe a un archivo temporal en el mismo directorio y
sustituye con os.replace. Si algo falla, el dataset original no se toca. Nunca
hace appends sueltos: una carga a medias corrompe el dataset.

Uso:
    python scripts/importar.py entrada.csv --tabla precios --dry-run
    python scripts/importar.py entrada.csv --tabla precios
"""

from __future__ import annotations

import argparse
import os
import sys
import tempfile
from pathlib import Path

import pandas as pd

RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ))

from src.data_loader import Dataset, app_config, cargar_datos  # noqa: E402
from src.validacion import validar  # noqa: E402

CLAVES = {
    "clubes": "club_id",
    "precios": "precio_id",
    "fuentes": "fuente_id",
    "salarios": "comunidad_autonoma",
}


def _fusionar(actual: pd.DataFrame, entrante: pd.DataFrame, clave: str) -> tuple[pd.DataFrame, list, list]:
    """Sustituye las filas cuya clave ya existe y añade las nuevas."""
    existentes = set(actual[clave])
    actualizadas = [v for v in entrante[clave] if v in existentes]
    nuevas = [v for v in entrante[clave] if v not in existentes]

    conservadas = actual[~actual[clave].isin(set(entrante[clave]))]
    fusionado = pd.concat([conservadas, entrante], ignore_index=True)
    return fusionado, nuevas, actualizadas


def _escribir_atomico(df: pd.DataFrame, destino: Path) -> None:
    destino.parent.mkdir(parents=True, exist_ok=True)
    tmp = tempfile.NamedTemporaryFile(
        mode="w", encoding="utf-8", newline="", delete=False, dir=destino.parent, suffix=".tmp"
    )
    try:
        df.to_csv(tmp, index=False)
        tmp.flush()
        os.fsync(tmp.fileno())
        tmp.close()
        os.replace(tmp.name, destino)
    except Exception:
        tmp.close()
        Path(tmp.name).unlink(missing_ok=True)
        raise


def importar(origen: Path, tabla: str, dry_run: bool) -> int:
    if tabla not in CLAVES:
        print(f"Tabla desconocida: {tabla}. Opciones: {', '.join(CLAVES)}.")
        return 2

    clave = CLAVES[tabla]
    entrante = pd.read_csv(origen, encoding="utf-8", dtype=str, keep_default_na=False)
    if clave not in entrante.columns:
        print(f"El archivo de entrada no tiene la columna clave '{clave}'.")
        return 2

    datos = cargar_datos()
    actual_bruto = pd.read_csv(
        RAIZ / app_config()["rutas"][tabla], encoding="utf-8", dtype=str, keep_default_na=False
    )

    faltan = set(actual_bruto.columns) - set(entrante.columns)
    sobran = set(entrante.columns) - set(actual_bruto.columns)
    if faltan or sobran:
        if faltan:
            print(f"Faltan columnas en la entrada: {', '.join(sorted(faltan))}.")
        if sobran:
            print(f"Sobran columnas en la entrada: {', '.join(sorted(sobran))}.")
        return 2

    fusionado, nuevas, actualizadas = _fusionar(actual_bruto, entrante, clave)
    fusionado = fusionado[actual_bruto.columns]

    candidato = Dataset(
        clubes=fusionado if tabla == "clubes" else datos.clubes,
        precios=fusionado if tabla == "precios" else datos.precios,
        fuentes=fusionado if tabla == "fuentes" else datos.fuentes,
        salarios=fusionado if tabla == "salarios" else datos.salarios,
    )
    if tabla in ("precios", "salarios"):
        candidato = _retipar(candidato, tabla, fusionado)

    errores = validar(candidato)

    print(f"Tabla: {tabla}")
    print(f"Filas nuevas: {len(nuevas)}" + (f" -> {', '.join(map(str, nuevas))}" if nuevas else ""))
    print(
        f"Filas actualizadas: {len(actualizadas)}"
        + (f" -> {', '.join(map(str, actualizadas))}" if actualizadas else "")
    )

    if errores:
        print(f"\nRechazado. {len(errores)} problema(s) de validación:")
        for e in errores:
            print(f"  - {e}")
        print("\nNo se ha escrito nada.")
        return 1

    print("\nValidación correcta.")
    if dry_run:
        print("Modo --dry-run: no se ha escrito nada.")
        return 0

    _escribir_atomico(fusionado, RAIZ / app_config()["rutas"][tabla])
    print(f"Escrito {len(fusionado)} filas en {app_config()['rutas'][tabla]}.")
    return 0


def _retipar(candidato: Dataset, tabla: str, fusionado: pd.DataFrame) -> Dataset:
    """Convierte a número las columnas que la validación espera numéricas."""
    df = fusionado.copy()
    if tabla == "precios":
        for col in (
            "precio_renovacion_eur",
            "precio_alta_eur",
            "suplemento_alta_eur",
            "precio_eur",
            "partidos_liga_incluidos",
        ):
            df[col] = pd.to_numeric(df[col].replace("", pd.NA), errors="coerce")
        return Dataset(candidato.clubes, df, candidato.fuentes, candidato.salarios)
    for col in ("salario_bruto_anual_eur", "anio_referencia"):
        df[col] = pd.to_numeric(df[col].replace("", pd.NA), errors="coerce")
    return Dataset(candidato.clubes, candidato.precios, candidato.fuentes, df)


def main() -> int:
    parser = argparse.ArgumentParser(description="Importador atómico de El Precio del Fútbol.")
    parser.add_argument("origen", type=Path, help="CSV de entrada.")
    parser.add_argument("--tabla", required=True, choices=sorted(CLAVES), help="Tabla destino.")
    parser.add_argument(
        "--dry-run", action="store_true", help="Informa de qué entraría y qué se rechaza, sin escribir."
    )
    args = parser.parse_args()
    return importar(args.origen, args.tabla, args.dry_run)


if __name__ == "__main__":
    raise SystemExit(main())
