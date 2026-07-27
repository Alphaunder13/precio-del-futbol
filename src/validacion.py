"""Validación del dataset.

Devuelve siempre una lista de mensajes. Lista vacía significa dataset válido.
La usan los tests y el importador atómico, que no escribe nada si esta lista no
está vacía.
"""

from __future__ import annotations

import re
from datetime import date

import pandas as pd

from src.data_loader import Dataset, app_config, pesos

FECHA = re.compile(r"^\d{4}-\d{2}-\d{2}$")


def _ids_unicos(df: pd.DataFrame, columna: str, tabla: str) -> list[str]:
    duplicados = df[df[columna].duplicated(keep=False)][columna].unique()
    return [f"{tabla}: identificador repetido '{d}' en la columna {columna}." for d in duplicados]


def _referencias(hijas: pd.DataFrame, columna: str, validas: set[str], tabla: str) -> list[str]:
    errores = []
    for valor in hijas[columna]:
        if valor and valor not in validas:
            errores.append(f"{tabla}: '{valor}' en {columna} no existe en la tabla de origen.")
    return errores


def validar(datos: Dataset) -> list[str]:
    cfg = app_config()
    enums = cfg["enums"]
    rangos = pesos()["rangos_validos"]
    errores: list[str] = []

    errores += _ids_unicos(datos.clubes, "club_id", "clubes")
    errores += _ids_unicos(datos.precios, "precio_id", "precios")
    errores += _ids_unicos(datos.fuentes, "fuente_id", "fuentes")
    errores += _ids_unicos(datos.salarios, "comunidad_autonoma", "salarios")

    clubes_validos = set(datos.clubes["club_id"])
    fuentes_validas = set(datos.fuentes["fuente_id"])
    comunidades_validas = set(datos.salarios["comunidad_autonoma"])

    errores += _referencias(datos.precios, "club_id", clubes_validos, "precios")
    errores += _referencias(datos.precios, "fuente_id", fuentes_validas, "precios")
    errores += _referencias(datos.fuentes, "club_id", clubes_validos, "fuentes")
    errores += _referencias(datos.clubes, "comunidad_autonoma", comunidades_validas, "clubes")

    for _, fila in datos.precios.iterrows():
        pid = fila["precio_id"]

        if fila["estado_verificacion"] not in enums["estado_verificacion"]:
            errores.append(f"precios[{pid}]: estado '{fila['estado_verificacion']}' fuera del enum permitido.")
        if fila["confianza"] not in enums["confianza"]:
            errores.append(f"precios[{pid}]: confianza '{fila['confianza']}' fuera del enum permitido.")
        if fila["metrica"] not in enums["metrica"]:
            errores.append(f"precios[{pid}]: métrica '{fila['metrica']}' fuera del enum permitido.")

        if not fila["fuente_id"]:
            errores.append(f"precios[{pid}]: no tiene fuente.")
        if not FECHA.match(fila["fecha_consulta"] or ""):
            errores.append(f"precios[{pid}]: fecha de consulta ausente o mal formada (se espera AAAA-MM-DD).")
        elif date.fromisoformat(fila["fecha_consulta"]) > date.today():
            errores.append(f"precios[{pid}]: la fecha de consulta está en el futuro.")

        precio = fila["precio_eur"]
        if pd.isna(precio):
            errores.append(f"precios[{pid}]: no tiene precio.")
        else:
            limites = rangos["abono_eur"] if fila["metrica"] == "abono_adulto_mas_barato" else rangos["entrada_eur"]
            if precio < 0:
                errores.append(f"precios[{pid}]: precio negativo ({precio}).")
            elif not (limites["minimo"] <= precio <= limites["maximo"]):
                errores.append(
                    f"precios[{pid}]: precio {precio} € fuera del rango razonable "
                    f"({limites['minimo']}-{limites['maximo']} €)."
                )

        partidos = fila["partidos_liga_incluidos"]
        if pd.isna(partidos) or partidos <= 0:
            errores.append(f"precios[{pid}]: partidos de liga incluidos ausente o no positivo.")

        if not fila["zona"]:
            errores.append(f"precios[{pid}]: no indica la zona del estadio.")

    for _, fila in datos.salarios.iterrows():
        ccaa = fila["comunidad_autonoma"]
        salario = fila["salario_bruto_anual_eur"]
        limites = rangos["salario_bruto_anual_eur"]
        if pd.isna(salario):
            errores.append(f"salarios[{ccaa}]: sin importe.")
        elif not (limites["minimo"] <= salario <= limites["maximo"]):
            errores.append(f"salarios[{ccaa}]: {salario} € fuera del rango razonable.")
        if not fila["fuente_id"]:
            errores.append(f"salarios[{ccaa}]: no tiene fuente.")

    for _, fila in datos.fuentes.iterrows():
        if not str(fila["url"]).startswith("http"):
            errores.append(f"fuentes[{fila['fuente_id']}]: la URL no es una dirección web válida.")
        if not FECHA.match(fila["fecha_consulta"] or ""):
            errores.append(f"fuentes[{fila['fuente_id']}]: fecha de consulta ausente o mal formada.")

    return errores
