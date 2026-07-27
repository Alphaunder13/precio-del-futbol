"""La descarga tiene que coincidir con lo que se ve en pantalla."""

from __future__ import annotations

import io

import pandas as pd
import pytest

from src.data_loader import app_config, cargar_datos, copy
from src.export import a_csv, nombre_fichero, tabla_publica
from src.index import calcular


@pytest.fixture(scope="module")
def datos():
    return cargar_datos()


@pytest.fixture(scope="module")
def publica(datos):
    return tabla_publica(calcular(datos), datos.fuentes)


def test_las_columnas_van_en_espanol_legible(publica):
    esperadas = set(app_config()["columnas_descarga"].values())
    assert set(publica.columns) <= esperadas
    for columna in publica.columns:
        assert "_" not in columna


def test_la_descarga_tiene_una_fila_por_club(publica, datos):
    assert len(publica) == len(datos.clubes)


def test_el_csv_se_relee_sin_perder_filas(publica):
    crudo = a_csv(publica)
    releido = pd.read_csv(io.BytesIO(crudo), sep=";", decimal=",", encoding="utf-8-sig")
    assert len(releido) == len(publica)
    assert list(releido.columns) == list(publica.columns)


def test_los_precios_de_la_descarga_coinciden_con_el_dataset(publica, datos):
    columna = app_config()["columnas_descarga"]["precio_eur"]
    descargados = sorted(publica[columna].tolist())
    dataset = sorted(datos.precios["precio_eur"].dropna().tolist())
    assert descargados == pytest.approx(dataset)


def test_los_estados_se_traducen(publica):
    columna = app_config()["columnas_descarga"]["estado_verificacion"]
    assert set(publica[columna]) <= set(copy()["estados"].values())


def test_el_nombre_del_fichero_no_lleva_barras():
    nombre = nombre_fichero()
    assert "/" not in nombre and nombre.endswith(".csv")


def test_cada_fila_lleva_su_fuente(publica):
    columna = app_config()["columnas_descarga"]["url"]
    assert publica[columna].str.startswith("http").all()
