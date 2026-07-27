"""El índice tiene que ser determinista y reproducible a mano."""

from __future__ import annotations

import pytest

from src.data_loader import cargar_datos, pesos
from src.index import calcular, euros_por_hora, horas_de_trabajo, precio_por_partido, tramo


@pytest.fixture(scope="module")
def tabla():
    return calcular(cargar_datos())


def test_mismo_input_mismo_output():
    a = calcular(cargar_datos())
    b = calcular(cargar_datos())
    assert a.equals(b)


def test_calculo_de_horas_reproducible_a_mano():
    # 30.000 € al año entre 1.800 horas son 16,666... €/hora.
    # Un abono de 500 € son 30 horas exactas.
    assert euros_por_hora(30000, 1800) == pytest.approx(16.6666667)
    assert horas_de_trabajo(500, 30000, 1800) == pytest.approx(30.0)


def test_precio_por_partido_usa_los_partidos_reales_del_club():
    # D-011: dividir siempre entre 19 falsearía a los clubes que cubren menos.
    assert precio_por_partido(340, 17) == pytest.approx(20.0)
    assert precio_por_partido(380, 19) == pytest.approx(20.0)


def test_los_tramos_respetan_los_umbrales_de_configuracion():
    umbrales = pesos()["umbrales_horas_abono"]
    assert tramo(umbrales["muy_bajo"] - 0.1, umbrales) == "muy_bajo"
    assert tramo(umbrales["muy_bajo"], umbrales) == "bajo"
    assert tramo(umbrales["alto"], umbrales) == "muy_alto"


def test_cada_club_aparece_una_sola_vez(tabla):
    assert tabla["club_id"].is_unique


def test_el_ranking_esta_ordenado_por_horas(tabla):
    horas = tabla["horas_trabajo"].tolist()
    assert horas == sorted(horas)
    assert tabla["posicion"].tolist() == list(range(1, len(tabla) + 1))


def test_ningun_club_se_queda_sin_salario(tabla):
    assert tabla["salario_bruto_anual_eur"].notna().all(), (
        "Hay un club cuya comunidad autónoma no tiene salario cargado."
    )


def test_las_horas_coinciden_con_el_calculo_directo(tabla):
    horas_anuales = pesos()["jornada_laboral"]["horas_anuales"]
    for _, fila in tabla.iterrows():
        esperado = fila["precio_eur"] / (fila["salario_bruto_anual_eur"] / horas_anuales)
        assert fila["horas_trabajo"] == pytest.approx(esperado)
