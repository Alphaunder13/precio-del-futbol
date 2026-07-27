"""Inicio: el número estrella y el ranking, sin scroll."""

from __future__ import annotations

import streamlit as st

from src.data_loader import cargar_datos, copy
from src.index import calcular
from src.ui_components import cabecera, euros, horas, numero, pie

c = copy()
datos = cargar_datos()
tabla = calcular(datos)

cabecera(c["inicio"]["titulo"], c["inicio"]["entradilla"])

mas_caro = tabla.iloc[-1]
mas_barato = tabla.iloc[0]

destacado = (
    f"### {c['inicio']['destacado_prefijo']} **{mas_caro['nombre']}** "
    f"{c['inicio']['destacado_sufijo']} "
    f"**{numero(mas_caro['horas_trabajo'], 1)}** {c['inicio']['destacado_unidad']}"
)
st.markdown(destacado)
st.caption(c["inicio"]["destacado_pie"].format(comunidad=mas_caro["comunidad_autonoma"]))

col1, col2, col3, col4 = st.columns(4)
col1.metric(
    c["inicio"]["etiqueta_mas_barato"],
    horas(mas_barato["horas_trabajo"]),
    help=f"{mas_barato['nombre']} · {euros(mas_barato['precio_eur'])}",
)
col2.metric(
    c["inicio"]["etiqueta_mas_caro"],
    horas(mas_caro["horas_trabajo"]),
    help=f"{mas_caro['nombre']} · {euros(mas_caro['precio_eur'])}",
)
sin_publicar = datos.descartados[datos.descartados["estado_verificacion"] == "no_publicado"]
col3.metric(c["inicio"]["etiqueta_clubes"], str(len(tabla)))
col4.metric(c["inicio"]["etiqueta_sin_publicar"], str(len(sin_publicar)))

columnas = c["ranking"]["columnas"]
resumen = tabla[["posicion", "nombre", "comunidad_autonoma", "precio_eur", "horas_trabajo"]].rename(
    columns={
        "posicion": columnas["posicion"],
        "nombre": columnas["club"],
        "comunidad_autonoma": columnas["comunidad"],
        "precio_eur": columnas["precio"],
        "horas_trabajo": columnas["horas"],
    }
)
resumen[columnas["precio"]] = tabla["precio_eur"].apply(euros)
resumen[columnas["horas"]] = tabla["horas_trabajo"].apply(horas)

st.dataframe(resumen, hide_index=True, use_container_width=True)
st.caption(c["inicio"]["pie_ranking"])

pie()
