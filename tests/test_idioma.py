"""El idioma no se revisa a ojo: se vigila con tests. Ver DECISIONS.md D-009."""

from __future__ import annotations

import re
from pathlib import Path

import pytest

from src.data_loader import RAIZ, app_config, copy

# Palabras inglesas frecuentes que delatarían una interfaz sin traducir.
PALABRAS_INGLESAS = {
    "the", "and", "or", "of", "for", "with", "from", "this", "that", "your", "you",
    "price", "prices", "ticket", "tickets", "season", "team", "teams", "match",
    "matches", "download", "search", "filter", "settings", "loading", "error",
    "warning", "submit", "next", "previous", "page", "home", "about", "data",
    "source", "sources", "average", "hours", "wage", "salary", "city", "stadium",
    "cheapest", "methodology", "notes", "show", "hide", "select", "none", "all",
}

SNAKE_CASE = re.compile(r"\b[a-z]+(?:_[a-z0-9]+)+\b")
MARCADOR = re.compile(r"\{[a-z_]+\}")
LLAMADA_STREAMLIT = re.compile(r"\bst\.(?:title|header|subheader|caption|write|markdown|"
                               r"metric|button|selectbox|multiselect|radio|checkbox|"
                               r"download_button|error|warning|info|success|expander|"
                               r"text_input|slider|tabs)\(\s*(['\"])(.+?)\1")


def _cadenas(obj, ruta="") -> list[tuple[str, str]]:
    """Aplana el YAML de copy en pares (ruta, texto)."""
    salida = []
    if isinstance(obj, dict):
        for k, v in obj.items():
            salida += _cadenas(v, f"{ruta}.{k}" if ruta else k)
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            salida += _cadenas(v, f"{ruta}[{i}]")
    elif isinstance(obj, str):
        salida.append((ruta, obj))
    return salida


@pytest.fixture(scope="module")
def textos():
    return _cadenas(copy())


def test_ninguna_cadena_visible_en_ingles(textos):
    whitelist = {p.lower() for entrada in app_config()["whitelist_ingles"] for p in entrada.split()}
    fallos = []
    for ruta, texto in textos:
        palabras = {p.strip(".,;:()¿?¡!·").lower() for p in texto.split()}
        intrusas = (palabras & PALABRAS_INGLESAS) - whitelist
        if intrusas:
            fallos.append(f"{ruta}: {', '.join(sorted(intrusas))}")
    assert not fallos, "Cadenas visibles con palabras en inglés:\n" + "\n".join(fallos)


def test_ningun_nombre_tecnico_expuesto_al_usuario(textos):
    fallos = []
    for ruta, texto in textos:
        sin_marcadores = MARCADOR.sub("", texto)
        if SNAKE_CASE.search(sin_marcadores):
            fallos.append(f"{ruta}: {texto}")
    assert not fallos, "Texto visible con nombres técnicos en snake_case:\n" + "\n".join(fallos)


def test_las_columnas_de_descarga_son_legibles():
    for tecnico, legible in app_config()["columnas_descarga"].items():
        assert "_" not in legible, f"La columna '{tecnico}' se descarga como '{legible}'."
        assert legible[0].isupper(), f"La columna '{legible}' debería empezar en mayúscula."


def test_el_codigo_no_contiene_texto_visible_a_pelo():
    """Todo lo que ve el usuario sale de copy_es.yaml, no de una cadena en el código."""
    fallos = []
    for carpeta in ("pages", "src"):
        for archivo in (RAIZ / carpeta).rglob("*.py"):
            for numero, linea in enumerate(archivo.read_text(encoding="utf-8").splitlines(), 1):
                encontrado = LLAMADA_STREAMLIT.search(linea)
                if encontrado and len(encontrado.group(2)) > 2:
                    fallos.append(f"{archivo.relative_to(RAIZ)}:{numero}: {encontrado.group(2)[:60]}")
    assert not fallos, (
        "Texto visible escrito en el código en vez de en copy_es.yaml:\n" + "\n".join(fallos)
    )


def test_el_disclaimer_esta_presente_y_es_completo():
    texto = copy()["pie"]["disclaimer"].lower()
    for exigido in ("independiente", "información pública", "sin afiliación", "pueden cambiar", "web oficial"):
        assert exigido in texto, f"Al disclaimer le falta '{exigido}'."
