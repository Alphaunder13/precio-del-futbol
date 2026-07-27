"""Integridad del dataset. Si algo de esto falla, no se publica."""

from __future__ import annotations

import pandas as pd
import pytest

from src.data_loader import app_config, cargar_datos
from src.validacion import validar


@pytest.fixture(scope="module")
def datos():
    return cargar_datos()


def test_el_dataset_publicado_es_valido(datos):
    errores = validar(datos)
    assert errores == [], "El dataset publicado no pasa su propia validación:\n" + "\n".join(errores)


def test_identificadores_unicos(datos):
    assert datos.clubes["club_id"].is_unique
    assert datos.precios["precio_id"].is_unique
    assert datos.fuentes["fuente_id"].is_unique
    assert datos.salarios["comunidad_autonoma"].is_unique


def test_integridad_referencial(datos):
    clubes = set(datos.clubes["club_id"])
    fuentes = set(datos.fuentes["fuente_id"])
    comunidades = set(datos.salarios["comunidad_autonoma"])

    assert set(datos.precios["club_id"]) <= clubes
    assert set(datos.precios["fuente_id"]) <= fuentes
    assert set(datos.clubes["comunidad_autonoma"]) <= comunidades


def test_ningun_precio_negativo_ni_absurdo(datos):
    precios = datos.precios["precio_eur"].dropna()
    assert (precios > 0).all()
    assert (precios < 3000).all()


def test_todo_registro_tiene_fuente_y_fecha(datos):
    assert (datos.precios["fuente_id"].str.len() > 0).all()
    assert (datos.precios["fecha_consulta"].str.len() == 10).all()
    assert (datos.fuentes["fecha_consulta"].str.len() == 10).all()


def test_estados_dentro_del_enum(datos):
    enums = app_config()["enums"]
    assert set(datos.precios["estado_verificacion"]) <= set(enums["estado_verificacion"])
    assert set(datos.precios["confianza"]) <= set(enums["confianza"])
    assert set(datos.precios["metrica"]) <= set(enums["metrica"])


def test_el_precio_total_cuadra_con_sus_componentes(datos):
    """precio_eur debe ser reconstruible: no puede haber un número que salga de la nada."""
    for _, fila in datos.precios.iterrows():
        alta = fila["precio_alta_eur"]
        renov = fila["precio_renovacion_eur"]
        suplemento = fila["suplemento_alta_eur"]
        base = alta if pd.notna(alta) else renov
        esperado = base + (suplemento if pd.notna(suplemento) else 0)
        assert fila["precio_eur"] == pytest.approx(esperado), (
            f"{fila['precio_id']}: el precio total no cuadra con base + suplemento."
        )


def test_alcance_entre_8_y_12_clubes(datos):
    """Criterio de aceptación de la v0.1.0."""
    assert 8 <= len(datos.clubes) <= 12


def test_todo_club_del_dataset_supera_el_umbral_de_calidad(datos):
    """D-004: un club solo entra con abono adulto verificado."""
    abonos = datos.precios[datos.precios["metrica"] == "abono_adulto_mas_barato"]
    assert set(abonos["club_id"]) == set(datos.clubes["club_id"])
    assert (abonos["estado_verificacion"] == "verificado").all()


def test_los_clubes_descartados_estan_documentados(datos):
    """D-012: no publicar la tarifa es un resultado, y se publica con su prueba."""
    descartados = datos.descartados
    assert not descartados.empty
    enums = app_config()["enums"]["estado_verificacion"]
    assert set(descartados["estado_verificacion"]) <= set(enums)
    assert descartados["url_revisada"].str.startswith("http").all()
    assert (descartados["fecha_consulta"].str.len() == 10).all()
    assert (descartados["nota"].str.len() > 40).all(), "Cada descarte necesita explicar qué se buscó."


def test_ningun_club_esta_a_la_vez_dentro_y_fuera(datos):
    dentro = set(datos.clubes["nombre"])
    fuera = set(datos.descartados["club"])
    assert dentro.isdisjoint(fuera)


def test_confianza_media_si_no_hay_precio_de_nuevo_abonado(datos):
    """D-010: si falta el coste de alta, el registro no puede declararse de confianza alta."""
    for _, fila in datos.precios.iterrows():
        if fila["estado_precio_nuevo_abonado"] == "no_publicado":
            assert fila["confianza"] != "alta", (
                f"{fila['precio_id']}: sin precio de nuevo abonado no puede tener confianza alta."
            )
