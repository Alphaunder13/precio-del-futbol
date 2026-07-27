"""Datos: explorador filtrable y descarga en CSV con columnas en español."""

from __future__ import annotations

import streamlit as st

from src.data_loader import cargar_datos, copy
from src.export import a_csv, nombre_fichero, tabla_publica
from src.index import calcular
from src.ui_components import cabecera, etiqueta_confianza, pie

c = copy()
d = c["datos"]
datos = cargar_datos()
tabla = calcular(datos)

cabecera(d["titulo"], d["entradilla"])

comunidades = [d["filtro_todos"]] + sorted(tabla["comunidad_autonoma"].unique().tolist())
confianzas = [d["filtro_todos"]] + [etiqueta_confianza(x) for x in sorted(tabla["confianza"].unique())]

col1, col2 = st.columns(2)
comunidad = col1.selectbox(d["filtro_comunidad"], comunidades)
confianza = col2.selectbox(d["filtro_confianza"], confianzas)

filtrada = tabla
if comunidad != d["filtro_todos"]:
    filtrada = filtrada[filtrada["comunidad_autonoma"] == comunidad]
if confianza != d["filtro_todos"]:
    filtrada = filtrada[filtrada["confianza"].apply(etiqueta_confianza) == confianza]

if filtrada.empty:
    st.warning(d["sin_resultados"])
else:
    publica = tabla_publica(filtrada, datos.fuentes)
    st.dataframe(publica, hide_index=True, use_container_width=True)
    st.download_button(
        label=d["descargar"],
        data=a_csv(publica),
        file_name=nombre_fichero(),
        mime="text/csv",
    )

pie()
