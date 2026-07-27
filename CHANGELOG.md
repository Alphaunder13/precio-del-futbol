# Registro de cambios

Formato: lo más reciente arriba. Las versiones siguen el criterio del proyecto,
no semver estricto, porque aquí lo que cambia sobre todo son los datos.

---

## [No publicado] — v0.1.0 en construcción

### 2026-07-27 — Comparable definido y tres primeros clubes verificados

**Añadido**
- `DECISIONS.md` con la definición del comparable escrita antes de recoger
  ningún dato: `abono_adulto_mas_barato` y `entrada_suelta_mas_barata`, con sus
  exclusiones explícitas (D-001 a D-003).
- Umbral de calidad por club, estados de verificación y ética de recolección
  (D-004 a D-006).
- `config/index_weights.yaml` con todos los pesos, divisores, umbrales y rangos
  de validación.
- Dataset inicial: CA Osasuna, Getafe CF y RCD Espanyol, los tres con tarifario
  oficial verificado, fuente enlazada y fecha de consulta.
- Capa salarial del INE (EAES 2024, datos definitivos) para Navarra, Madrid y
  Cataluña.
- `ISSUES.md` con Rayo Vallecano y Sevilla FC descartados por no publicar tarifa
  en abierto, con la búsqueda realizada.
- `README.md` y `PROJECT_STATE.md`.

**Corregido**
- D-007: la unidad geográfica del salario pasa de provincia a comunidad
  autónoma. La Encuesta Anual de Estructura Salarial del INE no publica
  desagregación provincial. Se corrigió antes de cargar ningún dato.

**Decidido sobre la marcha, al chocar con los datos reales**
- D-010: el precio del abono se guarda descompuesto en tarifa base más
  suplemento de alta de nuevo abonado, porque varios clubes cobran el segundo
  por separado y un número único sería opaco.
- D-011: `partidos_liga_incluidos` es columna del dataset. El abono de Osasuna
  cubre 17 de los 19 partidos de liga, no 19. El precio por partido se divide
  por el valor real de cada club.
- D-012: que un club no publique su tarifa es un resultado del estudio y se
  publica como tal, no se esconde como si fuera un hueco del dataset.
