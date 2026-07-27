"""Formato y piezas de interfaz reutilizables.

Cualquier número que vea el usuario pasa por aquí, para que el formato español
(miles con punto, decimales con coma) sea uno solo en toda la aplicación.
"""

from __future__ import annotations

from datetime import date

import pandas as pd
import streamlit as st

from src.data_loader import app_config, copy, pesos


def _formato() -> dict:
    return app_config()["formato"]


def numero(valor, decimales: int = 2) -> str:
    """Formato español: 1.234,56."""
    if valor is None or (isinstance(valor, float) and pd.isna(valor)) or pd.isna(valor):
        return copy()["comunes"]["sin_dato"]
    fmt = _formato()
    bruto = f"{float(valor):,.{decimales}f}"
    return bruto.replace(",", "\x00").replace(".", fmt["separador_decimal"]).replace(
        "\x00", fmt["separador_miles"]
    )


def euros(valor, decimales: int | None = None) -> str:
    if decimales is None:
        decimales = pesos()["redondeo"]["euros"]
    if valor is None or pd.isna(valor):
        return copy()["comunes"]["sin_dato"]
    return f"{numero(valor, decimales)} {_formato()['simbolo_moneda']}"


def horas(valor, decimales: int | None = None) -> str:
    if decimales is None:
        decimales = pesos()["redondeo"]["horas_trabajo"]
    if valor is None or pd.isna(valor):
        return copy()["comunes"]["sin_dato"]
    return f"{numero(valor, decimales)} {copy()['comunes']['horas']}"


def fecha(valor: str) -> str:
    if not valor:
        return copy()["comunes"]["sin_dato"]
    return date.fromisoformat(valor).strftime(_formato()["formato_fecha"])


def si_no(valor: str) -> str:
    c = copy()["comunes"]
    return c["si"] if str(valor).strip().lower() in {"si", "sí", "true", "1"} else c["no"]


def etiqueta_estado(clave: str) -> str:
    return copy()["estados"].get(clave, clave)


def etiqueta_confianza(clave: str) -> str:
    return copy()["confianza"].get(clave, clave)


def etiqueta_tramo(clave) -> str:
    if clave is None or pd.isna(clave):
        return copy()["comunes"]["sin_dato"]
    return copy()["tramos"].get(clave, clave)


def cabecera(titulo: str, entradilla: str = "") -> None:
    st.title(titulo)
    if entradilla:
        st.caption(entradilla)


def pie() -> None:
    st.divider()
    st.caption(copy()["pie"]["disclaimer"])
