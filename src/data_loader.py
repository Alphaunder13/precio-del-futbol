"""Carga de configuración y datos.

Ningún otro módulo lee del disco. Si algún día los CSV se sustituyen por otra
cosa, solo cambia este archivo.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from functools import lru_cache
from pathlib import Path

import pandas as pd
import yaml

RAIZ = Path(__file__).resolve().parent.parent
CONFIG = RAIZ / "config"


@lru_cache(maxsize=None)
def cargar_config(nombre: str) -> dict:
    """Devuelve un YAML de config/ como diccionario."""
    ruta = CONFIG / f"{nombre}.yaml"
    if not ruta.exists():
        raise FileNotFoundError(ruta)
    with ruta.open(encoding="utf-8") as f:
        return yaml.safe_load(f)


def copy() -> dict:
    return cargar_config("copy_es")


def pesos() -> dict:
    return cargar_config("index_weights")


def app_config() -> dict:
    return cargar_config("app_config")


@dataclass(frozen=True)
class Dataset:
    clubes: pd.DataFrame
    precios: pd.DataFrame
    fuentes: pd.DataFrame
    salarios: pd.DataFrame
    # Clubes revisados que no entran al ranking. Forman parte del resultado
    # (D-012), así que viajan con el dataset y no en una nota al margen.
    descartados: pd.DataFrame = field(default_factory=pd.DataFrame)


def _leer(ruta: Path) -> pd.DataFrame:
    if not ruta.exists():
        raise FileNotFoundError(ruta)
    return pd.read_csv(ruta, encoding="utf-8", dtype=str, keep_default_na=False)


def _a_numero(serie: pd.Series) -> pd.Series:
    """Convierte a float dejando en NaN las celdas vacías."""
    return pd.to_numeric(serie.replace("", pd.NA), errors="coerce")


def cargar_datos(raiz: Path | None = None) -> Dataset:
    """Lee los cuatro CSV y tipa las columnas numéricas."""
    base = Path(raiz) if raiz else RAIZ
    cfg = app_config()["rutas"]

    clubes = _leer(base / cfg["clubes"])
    precios = _leer(base / cfg["precios"])
    fuentes = _leer(base / cfg["fuentes"])
    salarios = _leer(base / cfg["salarios"])

    for col in (
        "precio_renovacion_eur",
        "precio_alta_eur",
        "suplemento_alta_eur",
        "precio_eur",
        "partidos_liga_incluidos",
    ):
        precios[col] = _a_numero(precios[col])

    salarios["salario_bruto_anual_eur"] = _a_numero(salarios["salario_bruto_anual_eur"])
    salarios["anio_referencia"] = _a_numero(salarios["anio_referencia"])

    descartados = _leer(base / cfg["descartados"])

    return Dataset(
        clubes=clubes,
        precios=precios,
        fuentes=fuentes,
        salarios=salarios,
        descartados=descartados,
    )
