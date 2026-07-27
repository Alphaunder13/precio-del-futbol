"""Metodología: la definición del comparable, las exclusiones y los límites."""

from __future__ import annotations

import streamlit as st

from src.data_loader import cargar_datos, copy
from src.ui_components import cabecera, fecha, pie

c = copy()
m = c["metodologia"]
datos = cargar_datos()

cabecera(m["titulo"], m["intro"])

for seccion in m["secciones"]:
    st.subheader(seccion["titulo"])
    st.markdown(seccion["cuerpo"])

st.subheader(m["titulo_descartados"])
descartados = datos.descartados[list(m["tabla_descartados"])].copy()
descartados["estado_verificacion"] = descartados["estado_verificacion"].map(c["estados"]).fillna("")
descartados["fecha_consulta"] = descartados["fecha_consulta"].apply(fecha)
st.dataframe(descartados.rename(columns=m["tabla_descartados"]), hide_index=True, use_container_width=True)

st.subheader(m["titulo_fuentes"])
fuentes = datos.fuentes[["titulo", "url", "fecha_consulta"]].copy()
fuentes["fecha_consulta"] = fuentes["fecha_consulta"].apply(fecha)
fuentes = fuentes.rename(columns=m["tabla_fuentes"])
st.dataframe(fuentes, hide_index=True, use_container_width=True)

pie()
