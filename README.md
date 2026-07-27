# El Precio del Fútbol

Cuánto cuesta ir al fútbol en España, y cuánto cuesta de verdad según dónde
vives.

El número que persigue este proyecto es uno solo: **el abono más barato de un
club equivale a N horas de trabajo al salario medio de su comunidad autónoma**.

Herramienta gratuita, datos abiertos, cálculo auditable.

---

## Estado

v0.1.0 en construcción. Temporada 2026/27, LaLiga EA Sports.
El estado real y la próxima acción están en [PROJECT_STATE.md](PROJECT_STATE.md).

---

## Cómo está hecho

Todo precio del dataset lleva **fuente, fecha de consulta y estado de
verificación**. Ningún precio se estima a ojo: si no se encuentra en la web
oficial del club sin iniciar sesión, se registra como `no_publicado` y se
publica como tal.

El cálculo es determinista: mismo dato de entrada, mismo resultado. Sin
aprendizaje automático y sin aleatoriedad. Todos los pesos y umbrales viven en
[`config/index_weights.yaml`](config/index_weights.yaml), ninguno en el código.

La definición del comparable —qué abono se compara con qué abono, y qué queda
excluido— está en [DECISIONS.md](DECISIONS.md) y se escribió **antes** de recoger
el primer dato. Los clubes que no llegan al umbral de calidad, y el motivo, están
en [ISSUES.md](ISSUES.md).

---

## Cómo se recogen los datos

- Solo información visible públicamente **sin iniciar sesión**.
- Si el precio solo aparece dentro del proceso de compra o tras registro, se
  marca `no_publicado`. No se completan flujos de compra ni se crean cuentas.
- Se respeta `robots.txt`, comprobado dominio a dominio y registrado en
  `data/fuentes.csv`.
- No se recoge ningún dato personal.

---

## Estructura

```
config/    copy_es.yaml, index_weights.yaml, app_config.yaml
data/      clubes.csv, precios.csv, fuentes.csv, salarios.csv
src/       data_loader, validacion, index, export, ui_components
pages/     Inicio, Ranking, Ficha de club, Datos, Metodología
scripts/   importador atómico con --dry-run
tests/
```

---

## Aviso

Prototipo independiente elaborado con información pública, sin afiliación ni
respaldo de ningún club ni de ninguna competición. Los precios corresponden a la
fecha de consulta y pueden cambiar. Verifica en la web oficial del club antes de
comprar.
