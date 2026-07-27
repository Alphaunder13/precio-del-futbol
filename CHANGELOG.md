# Registro de cambios

Formato: lo más reciente arriba. Las versiones siguen el criterio del proyecto,
no semver estricto, porque aquí lo que cambia sobre todo son los datos.

---

## [No publicado] — v0.1.0 en construcción

### 2026-07-28 — Dataset de ocho clubes y producto completo

**Añadido**
- Cinco clubes más, todos con tarifario oficial verificado: RC Celta,
  Real Racing Club, Málaga CF, RC Deportivo y Levante UD. El dataset cubre ocho
  clubes en siete comunidades autónomas.
- `data/descartados.csv`: los clubes revisados que no entran al ranking, con la
  dirección revisada, la fecha y qué se buscó. Alimenta la página de Metodología,
  de modo que el recuento que ve el usuario no es un número escrito a mano.
- `src/`: `data_loader`, `validacion`, `index`, `export` y `ui_components`.
- `scripts/importar.py`: importador atómico. Valida en memoria, escribe a un
  temporal y sustituye con `os.replace`. Con `--dry-run` informa de qué entraría
  y qué se rechaza sin tocar nada.
- Las cinco páginas: Inicio, Ranking, Ficha de club, Datos y Metodología.
- 32 tests: integridad referencial, rangos, enums, determinismo del índice,
  coincidencia entre la descarga y el dataset, y vigilancia del idioma.

**Corregido**
- Los salarios se descargan ahora de la interfaz de datos del INE en formato
  máquina. Dos lecturas de la misma nota de prensa devolvieron cifras distintas
  para Cantabria y Comunitat Valenciana, y una tercera mezcló años. El error era
  de transcripción, no del organismo, pero habría contaminado el ranking entero
  de esas comunidades.
- El test de idioma detectó texto técnico en un mensaje de error visible ("la
  carpeta data") y en la entradilla de la página de Datos ("el dataset
  completo"). Corregidos los dos.
- `comunes.no` en el copy estaba sin comillas y YAML lo interpretaba como el
  booleano falso, así que la clave no era la cadena "no".

**Decidido**
- D-013: las gradas de animación, de peñas y de movilidad reducida quedan fuera
  del comparable aunque a veces sean la localidad más barata, porque exigen
  pertenecer a un colectivo o acreditar una condición personal.
- D-014: las estadísticas oficiales se leen en formato máquina, nunca de un
  resumen de texto.


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
