"""Preparación de las descargas.

El CSV que se descarga el usuario lleva las columnas con nombre legible en
español. Ningún nombre técnico en snake_case sale de aquí.
"""

from __future__ import annotations

import pandas as pd

from src.data_loader import app_config, copy
from src.ui_components import si_no


def tabla_publica(calculado: pd.DataFrame, fuentes: pd.DataFrame) -> pd.DataFrame:
    """Une el cálculo con la URL de su fuente y renombra a español legible."""
    cfg = app_config()
    columnas = cfg["columnas_descarga"]
    c = copy()

    urls = fuentes.set_index("fuente_id")["url"].to_dict()
    tabla = calculado.copy()
    tabla["url"] = tabla["fuente_id"].map(urls)

    tabla["incluye_copa"] = tabla["incluye_copa"].apply(si_no)
    tabla["estado_verificacion"] = tabla["estado_verificacion"].map(c["estados"]).fillna("")
    tabla["confianza"] = tabla["confianza"].map(c["confianza"]).fillna("")

    presentes = [col for col in columnas if col in tabla.columns]
    return tabla[presentes].rename(columns={col: columnas[col] for col in presentes})


def a_csv(tabla: pd.DataFrame) -> bytes:
    """CSV UTF-8 con BOM, para que se abra bien en Excel en español."""
    return tabla.to_csv(index=False, encoding="utf-8-sig", sep=";", decimal=",").encode("utf-8-sig")


def nombre_fichero() -> str:
    cfg = app_config()["app"]
    plantilla = copy()["datos"]["nombre_fichero"]
    return plantilla.format(temporada=cfg["temporada"].replace("/", "-"))
