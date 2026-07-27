"""Ranking: tabla ordenable con precio absoluto y precio en horas de trabajo."""

from __future__ import annotations

import plotly.express as px
import streamlit as st

from src.data_loader import cargar_datos, copy
from src.index import calcular
from src.ui_components import cabecera, etiqueta_confianza, euros, horas, pie

c = copy()
columnas = c["ranking"]["columnas"]
datos = cargar_datos()
tabla = calcular(datos)

cabecera(c["ranking"]["titulo"], c["ranking"]["entradilla"])

grafico = px.bar(
    tabla,
    x="horas_trabajo",
    y="nombre",
    orientation="h",
    labels={"horas_trabajo": columnas["horas"], "nombre": columnas["club"]},
    text=tabla["horas_trabajo"].apply(horas),
    color="horas_trabajo",
    color_continuous_scale="Oranges",
)
grafico.update_layout(
    yaxis={"categoryorder": "total descending"},
    coloraxis_showscale=False,
    height=420,
    margin={"l": 0, "r": 0, "t": 10, "b": 0},
)
st.plotly_chart(grafico, use_container_width=True)

vista = tabla[
    [
        "posicion",
        "nombre",
        "comunidad_autonoma",
        "zona",
        "precio_eur",
        "horas_trabajo",
        "precio_por_partido",
        "partidos_liga_incluidos",
        "confianza",
    ]
].copy()
vista["precio_eur"] = tabla["precio_eur"].apply(euros)
vista["horas_trabajo"] = tabla["horas_trabajo"].apply(horas)
vista["precio_por_partido"] = tabla["precio_por_partido"].apply(euros)
vista["partidos_liga_incluidos"] = tabla["partidos_liga_incluidos"].astype(int)
vista["confianza"] = tabla["confianza"].apply(etiqueta_confianza)

vista = vista.rename(
    columns={
        "posicion": columnas["posicion"],
        "nombre": columnas["club"],
        "comunidad_autonoma": columnas["comunidad"],
        "zona": columnas["zona"],
        "precio_eur": columnas["precio"],
        "horas_trabajo": columnas["horas"],
        "precio_por_partido": columnas["por_partido"],
        "partidos_liga_incluidos": columnas["partidos"],
        "confianza": columnas["confianza"],
    }
)

st.dataframe(vista, hide_index=True, use_container_width=True)
st.info(c["ranking"]["aviso_confianza_media"])

pie()
