# Estado del proyecto

**Versión:** v0.1.0 en construcción
**Última actualización:** 2026-07-27
**Temporada del dataset:** 2026/27

---

## Dónde estamos

Hito 1 cerrado: comparable definido y **tres primeros clubes verificados** con
tarifario oficial, tal como pedía el encargo antes de escalar al resto.

### Clubes en el dataset (3)

| Club | Zona más barata adulto | Base | Alta nuevo abonado | Total | Confianza |
|---|---|---|---|---|---|
| CA Osasuna | Sectores 113/114/115 | 310 € | 100 € | **410 €** | media |
| Getafe CF | Fondos | 330 € | no publicado | **330 €** | media |
| RCD Espanyol | Corner Superior | 309 € | 0 € (incluida) | **309 €** | alta |

### Clubes revisados y descartados (2)

Rayo Vallecano y Sevilla FC: no publican tarifa en abierto. Documentado en
`ISSUES.md`. Cuentan como hallazgo, no como fallo (D-012).

### Capa salarial

INE, Encuesta Anual de Estructura Salarial 2024 (datos definitivos), salario
bruto medio anual por comunidad autónoma. Cargadas solo las tres comunidades en
uso: Navarra, Madrid y Cataluña.

---

## Lo que ya existe

- `DECISIONS.md` con doce decisiones, incluida la definición del comparable
  escrita antes de recoger el primer dato.
- `ISSUES.md` con los dos clubes descartados y tres limitaciones abiertas.
- `config/index_weights.yaml` con todos los pesos, divisores y umbrales.
- `data/clubes.csv`, `data/precios.csv`, `data/fuentes.csv`, `data/salarios.csv`.

---

## Próxima acción exacta

**Escalar la recogida al resto de clubes hasta llegar a un mínimo de 8**, por
este orden de candidatos, que son los que con más probabilidad publican tarifa
en abierto:

1. Levante UD — `abonos.levanteud.com` y nota oficial de renovación
2. RC Celta — campaña "Ágora e sempre"
3. Deportivo Alavés
4. Villarreal CF
5. RC Deportivo, Real Racing Club y Málaga CF (recién ascendidos, campañas nuevas)
6. Elche CF — la tarifa está en `abonados.elchecf.es`, que redirige; comprobar si
   hay versión en abierto antes de descartar

Para cada uno: comprobar `robots.txt`, localizar tarifario oficial, extraer zona
adulto más barata, registrar base + suplemento de alta + partidos incluidos.

### Después de eso, en orden

1. `entrada_suelta_mas_barata` para los clubes ya cargados (D-003).
2. `src/` — `data_loader`, `validacion`, `index`, `export`, `ui_components`.
3. `tests/` — se escriben junto a cada módulo, no al final.
4. `config/copy_es.yaml` con todo el texto visible.
5. `scripts/` — importador atómico con `--dry-run`.
6. Páginas Streamlit: Inicio, Ranking, Ficha de club, Datos, Metodología.
7. Despliegue en Streamlit Community Cloud y verificación en producción.

---

## Decisiones que necesitan validación humana

- **Ninguna bloqueante ahora mismo.**
- A vigilar: si al terminar la recogida no se alcanzan 8 clubes con tarifa
  verificable, hay que decidir si se baja el umbral de calidad o se reduce el
  alcance. Esa decisión no se toma sin consultar.
