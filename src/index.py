"""Cálculo del índice.

Por reglas, determinista y auditable. Mismo dato de entrada, mismo resultado.
Sin aprendizaje automático y sin aleatoriedad. Todos los parámetros vienen de
config/index_weights.yaml. Ver DECISIONS.md D-008.
"""

from __future__ import annotations

import pandas as pd

from src.data_loader import Dataset, pesos

METRICA_ABONO = "abono_adulto_mas_barato"


def euros_por_hora(salario_anual: float, horas_anuales: int) -> float:
    """Salario bruto anual convertido a euros por hora trabajada."""
    return salario_anual / horas_anuales


def horas_de_trabajo(precio: float, salario_anual: float, horas_anuales: int) -> float:
    """Cuántas horas hay que trabajar, al salario medio, para pagar ese precio."""
    return precio / euros_por_hora(salario_anual, horas_anuales)


def precio_por_partido(precio: float, partidos: int) -> float:
    """Reparte el precio entre los partidos que el abono cubre de verdad (D-011)."""
    return precio / partidos


def tramo(horas: float, umbrales: dict) -> str:
    """Etiqueta cualitativa. Devuelve la clave, nunca el texto: el texto vive en copy_es."""
    if horas < umbrales["muy_bajo"]:
        return "muy_bajo"
    if horas < umbrales["bajo"]:
        return "bajo"
    if horas < umbrales["medio"]:
        return "medio"
    if horas < umbrales["alto"]:
        return "alto"
    return "muy_alto"


def calcular(datos: Dataset) -> pd.DataFrame:
    """Devuelve una fila por club con el abono y todas las cifras derivadas."""
    cfg = pesos()
    horas_anuales = cfg["jornada_laboral"]["horas_anuales"]
    umbrales = cfg["umbrales_horas_abono"]

    abonos = datos.precios[datos.precios["metrica"] == METRICA_ABONO]

    tabla = abonos.merge(datos.clubes, on="club_id", how="left", validate="one_to_one")
    # Solo las columnas que hacen falta: salarios comparte nombres con precios
    # (fuente_id, fecha_consulta) y un merge completo los duplicaría.
    salarios = datos.salarios[["comunidad_autonoma", "salario_bruto_anual_eur", "anio_referencia"]]
    tabla = tabla.merge(salarios, on="comunidad_autonoma", how="left", validate="many_to_one")

    tabla["euros_por_hora"] = tabla["salario_bruto_anual_eur"].apply(
        lambda s: euros_por_hora(s, horas_anuales) if pd.notna(s) else pd.NA
    )
    tabla["horas_trabajo"] = [
        horas_de_trabajo(p, s, horas_anuales) if pd.notna(p) and pd.notna(s) else pd.NA
        for p, s in zip(tabla["precio_eur"], tabla["salario_bruto_anual_eur"])
    ]
    tabla["precio_por_partido"] = [
        precio_por_partido(p, int(n)) if pd.notna(p) and pd.notna(n) and n > 0 else pd.NA
        for p, n in zip(tabla["precio_eur"], tabla["partidos_liga_incluidos"])
    ]
    tabla["tramo"] = [
        tramo(h, umbrales) if pd.notna(h) else pd.NA for h in tabla["horas_trabajo"]
    ]

    orden = cfg["orden_por_defecto"]
    tabla = tabla.sort_values(
        by=[orden["columna"], "nombre"], ascending=[orden["ascendente"], True]
    ).reset_index(drop=True)
    tabla.insert(0, "posicion", range(1, len(tabla) + 1))
    return tabla


def desglose(fila: pd.Series) -> dict:
    """Todo lo necesario para explicar de dónde sale cada número de una fila."""
    cfg = pesos()
    return {
        "precio_renovacion": fila.get("precio_renovacion_eur"),
        "precio_alta": fila.get("precio_alta_eur"),
        "suplemento_alta": fila.get("suplemento_alta_eur"),
        "precio": fila["precio_eur"],
        "salario": fila.get("salario_bruto_anual_eur"),
        "horas_anuales": cfg["jornada_laboral"]["horas_anuales"],
        "euros_por_hora": fila.get("euros_por_hora"),
        "horas_trabajo": fila.get("horas_trabajo"),
        "partidos": fila.get("partidos_liga_incluidos"),
        "precio_por_partido": fila.get("precio_por_partido"),
    }
