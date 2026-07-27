# Estado del proyecto

**Versión:** v0.1.0, completa a falta del despliegue
**Última actualización:** 2026-07-28
**Temporada del dataset:** 2026/27

---

## Dónde estamos

Producto terminado y funcionando en local. Ocho clubes con tarifa oficial
verificada, cuatro revisados y documentados fuera del ranking, 32 tests en verde
y las cinco páginas comprobadas en el navegador.

**Lo único que falta es el despliegue**, que requiere una acción humana: crear el
repositorio remoto y autorizar la aplicación en Streamlit Community Cloud.

### El ranking actual

| # | Club | Zona | Precio | Horas | €/partido | Confianza |
|---|---|---|---|---|---|---|
| 1 | Málaga CF | Fondo Alto | 234 € | 16,1 h | 12,32 € | alta |
| 2 | Getafe CF | Fondos | 330 € | 17,3 h | 17,37 € | media |
| 3 | RCD Espanyol | Corner Superior | 309 € | 17,5 h | 16,26 € | alta |
| 4 | Levante UD | Gol Orriols-Alboraya Corner | 262 € | 17,6 h | 13,79 € | media |
| 5 | RC Celta | Marcador Baixo | 266 € | 18,0 h | 14,00 € | media |
| 6 | Real Racing Club | Preferencia Sur | 315 € | 20,9 h | 16,58 € | media |
| 7 | CA Osasuna | Sectores 113-114-115 | 410 € | 22,6 h | 24,12 € | media |
| 8 | RC Deportivo | Pabellón Inferior | 380 € | 25,8 h | 20,00 € | alta |

Siete comunidades autónomas representadas. El más barato en euros no es el más
barato en horas, y el orden por euros y por horas no coincide en ningún tramo.

### Fuera del ranking (4)

Rayo Vallecano, Sevilla FC y Deportivo Alavés no publican tarifa en abierto.
Villarreal CF quedó `sin_confirmar` porque su página no cargó. Todo en
`ISSUES.md` y en `data/descartados.csv`.

---

## Lo que ya existe

- `DECISIONS.md`: catorce decisiones, con la definición del comparable escrita
  antes de recoger el primer dato y las cuatro que forzó la recogida real.
- `ISSUES.md`: cuatro clubes descartados y seis limitaciones abiertas.
- `config/`: `copy_es.yaml` con todo el texto visible, `index_weights.yaml` con
  todos los parámetros del cálculo, `app_config.yaml` con enums y rutas.
- `data/`: cinco CSV. Cada precio con zona, fuente, fecha, estado y confianza.
- `src/`: `data_loader`, `validacion`, `index`, `export`, `ui_components`.
- `scripts/importar.py`: importador atómico con `--dry-run`.
- `tests/`: 32 tests, todos en verde.
- `pages/`: Inicio, Ranking, Ficha de club, Datos, Metodología.

---

## Próxima acción exacta

**Desplegar.** Requiere intervención humana en dos puntos que no se pueden
automatizar sin credenciales:

1. Crear el repositorio remoto en GitHub y hacer `git push`.
2. Entrar en share.streamlit.io, autorizar el repositorio y desplegar
   `streamlit_app.py`.

Recordatorios de despliegue conocidos:

- Si se tocan módulos de `src/`, tocar también `requirements.txt` para forzar la
  reconstrucción del contenedor.
- Streamlit Cloud auto-commitea `.devcontainer/` al desplegar: hacer
  `git pull --rebase` antes del siguiente push.
- La aplicación se duerme por inactividad: despertarla antes de concluir que el
  despliegue ha fallado.
- Verificar en una sesión de navegador limpia y confirmar que la versión
  desplegada es la correcta.

### Después del despliegue, por orden

1. Reintentar Villarreal CF para llegar a nueve clubes.
2. `entrada_suelta_mas_barata` (D-003), que aún no tiene ningún registro. Es el
   único punto del alcance de la v0.1.0 que queda sin cubrir.
3. Revisar si Getafe, Racing o Levante abren altas nuevas y publican precio, para
   subir esos tres registros de confianza media a alta.

---

## Decisiones que necesitan validación humana

- **El repositorio, ¿público o privado?** Streamlit Community Cloud funciona con
  ambos. No se crea ninguno sin decidirlo.
- **`entrada_suelta_mas_barata` sigue vacía.** El umbral de calidad (D-004) no la
  hace bloqueante, así que la v0.1.0 se sostiene sin ella, pero el alcance
  original la incluía. Conviene decidir si se publica sin esa métrica o se
  retrasa el lanzamiento hasta tenerla.
