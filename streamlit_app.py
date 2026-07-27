"""Punto de entrada. Solo enruta: la lógica vive en src/ y el texto en config/."""

from __future__ import annotations

import streamlit as st

from src.data_loader import app_config, copy

c = copy()
cfg = app_config()["app"]

st.set_page_config(
    page_title=c["producto"]["nombre"],
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="expanded",
)

navegacion = st.navigation(
    [
        st.Page("pages/inicio.py", title=c["navegacion"]["inicio"], icon="⚽", default=True),
        st.Page("pages/ranking.py", title=c["navegacion"]["ranking"], icon="📊"),
        st.Page("pages/ficha_club.py", title=c["navegacion"]["ficha"], icon="🔎"),
        st.Page("pages/datos.py", title=c["navegacion"]["datos"], icon="📂"),
        st.Page("pages/metodologia.py", title=c["navegacion"]["metodologia"], icon="📐"),
    ]
)

st.sidebar.caption(c["producto"]["temporada_etiqueta"])
navegacion.run()
