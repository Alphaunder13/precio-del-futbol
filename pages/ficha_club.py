"""Ficha de club: cada número, con su desglose, su fuente y su fecha."""

from __future__ import annotations

import pandas as pd
import streamlit as st

from src.data_loader import cargar_datos, copy
from src.index import calcular, desglose
from src.ui_components import (
    cabecera,
    etiqueta_confianza,
    etiqueta_estado,
    euros,
    fecha,
    horas,
    numero,
    pie,
    si_no,
)

c = copy()
f = c["ficha"]
datos = cargar_datos()
tabla = calcular(datos)

cabecera(f["titulo"])

nombres = tabla["nombre"].tolist()
elegido = st.selectbox(f["selector"], nombres)
fila = tabla[tabla["nombre"] == elegido].iloc[0]
d = desglose(fila)

st.subheader(f["bloque_precio"])
col1, col2, col3 = st.columns(3)
col1.metric(f["etiqueta_renovacion"], euros(d["precio_renovacion"]))
col2.metric(
    f["etiqueta_alta"],
    euros(d["precio_alta"]) if pd.notna(d["precio_alta"]) else etiqueta_estado(fila["estado_precio_nuevo_abonado"]),
)
col3.metric(f["etiqueta_suplemento"], euros(d["suplemento_alta"]))

col4, col5, col6 = st.columns(3)
col4.metric(f["etiqueta_total"], euros(d["precio"]))
col5.metric(f["etiqueta_zona"], fila["zona"])
col6.metric(f["etiqueta_partidos"], f"{int(d['partidos'])} · {si_no(fila['incluye_copa'])}")

st.subheader(f["bloque_calculo"])
st.markdown(
    f["formula_horas"].format(
        precio=euros(d["precio"]),
        salario=euros(d["salario"]),
        horas_anuales=numero(d["horas_anuales"], 0),
        resultado=numero(d["horas_trabajo"], 1),
    )
)
st.markdown(
    f["formula_partido"].format(
        precio=euros(d["precio"]),
        partidos=int(d["partidos"]),
        resultado=euros(d["precio_por_partido"]),
    )
)

col7, col8, col9 = st.columns(3)
col7.metric(f["etiqueta_salario"], euros(d["salario"]))
col8.metric(f["etiqueta_hora"], euros(d["euros_por_hora"]))
col9.metric(f["etiqueta_horas"], horas(d["horas_trabajo"]))

st.subheader(f["bloque_fuente"])
fuente = datos.fuentes[datos.fuentes["fuente_id"] == fila["fuente_id"]].iloc[0]
col10, col11 = st.columns(2)
col10.metric(f["etiqueta_estado"], etiqueta_estado(fila["estado_verificacion"]))
col11.metric(f["etiqueta_confianza"], etiqueta_confianza(fila["confianza"]))
st.caption(f"{f['etiqueta_consulta']}: {fecha(fila['fecha_consulta'])}")
st.link_button(f["ver_fuente"], fuente["url"])

st.subheader(f["etiqueta_nota"])
st.write(fila["nota"])

pie()
