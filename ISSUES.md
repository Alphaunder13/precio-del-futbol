# Clubes descartados y limitaciones abiertas

Este archivo no es una lista de fallos. Que un club no publique su tarifario es
un resultado del estudio y se documenta aquí con la búsqueda exacta que se hizo,
para que cualquiera pueda repetirla.

Criterio de entrada: DECISIONS.md D-004.

---

## Clubes fuera del dataset v0.1.0

### Rayo Vallecano — `no_publicado`

- **Fecha de consulta:** 2026-07-27
- **Fuente revisada:** https://www.rayovallecano.es/noticias/campana-de-abonados-202627
  (página oficial de la campaña de abonados 2026/27, publicada el 24 de julio de 2026)
- **Qué sí publica el club:** las cinco fases de renovación con sus fechas, las
  franjas de edad de cada modalidad (Peke, Infantil, Joven, Adulto, Tercera
  Edad), qué partidos cubre el abono (19 de LaLiga EA Sports más el primer
  partido de Copa como local) y las condiciones generales.
- **Qué no publica:** ni un solo precio. La página no contiene tabla de tarifas
  por zona ni importe alguno para ninguna modalidad.
- **Dónde está el precio:** solo dentro de la plataforma de renovación, a la que
  se accede identificándose con el abono de la temporada anterior.
- **Por qué queda fuera:** D-006 prohíbe entrar en flujos de compra o registro.
  Sin tarifario en abierto no hay `abono_adulto_mas_barato` verificable, y D-004
  lo hace bloqueante.
- **Nota adicional:** el club declara tener el cupo de abonados completo, de modo
  que la fase de altas nuevas solo se abre si se producen bajas. Es un caso
  distinto al de un club que oculta el precio: aquí prácticamente no hay producto
  a la venta para un aficionado nuevo.

### Sevilla FC — `no_publicado`

- **Fecha de consulta:** 2026-07-27
- **Fuente revisada:** https://sevillafc.es/actualidad/noticias/campana-abonos-2026-2027
- **Qué sí publica el club:** la estructura completa del producto. El pago del
  asiento cubre los 19 partidos de LaLiga EA Sports y el XV Trofeo Antonio
  Puerta; la cuota anual de socio se cobra aparte en enero de 2027; la cuota de
  alta de nuevo socio es de 125 €; existe una "regla de los 14 partidos" que
  penaliza al abonado que no usa ni cede su asiento.
- **Qué no publica:** la tabla de precios por zona. Ninguna página abierta del
  dominio la contiene.
- **Dónde está el precio:** en el Portal del Socio, que exige número de abonado
  y PIN, y en `entradas.sevillafc.es`, que es el proceso de compra.
- **Por qué queda fuera:** mismo motivo que Rayo Vallecano. D-006 y D-004.
- **Nota adicional:** es el caso más llamativo del estudio hasta ahora. El club
  documenta con detalle las obligaciones del abonado y no documenta en abierto lo
  que cuesta serlo.

---

## Limitaciones abiertas del dataset

### L-001 — El coste de alta no es comparable entre clubes

Algunos clubes cobran un suplemento por darse de alta como abonado nuevo
(Osasuna: 100 €; Sevilla: 125 €) y otros no lo publican porque su campaña es
solo de renovación (Getafe). D-010 fija cómo se registra. El efecto práctico es
que el precio de un club con campaña cerrada a nuevos abonados está registrado
sin ese coste y por tanto **infravalorado** respecto a los que sí lo publican.
Se marca con confianza media y se avisa en la ficha del club.

### L-002 — Lo que cubre el abono no es idéntico

Osasuna excluye del carnet dos partidos de liga declarados "Día del Club", de
modo que el abono cubre 17 de los 19 partidos de liga en casa. Getafe y Espanyol
incluyen los 19 más Copa del Rey. El precio por partido corrige parte de esta
diferencia, pero no toda: se documenta en cada ficha.

### L-003 — Varios clubes tienen el aforo de abonados completo

Rayo Vallecano y, en la práctica, Osasuna (solo pueden darse de alta quienes
tuvieran el carné 'Soy Rojillo' la temporada anterior) no venden abonos
libremente. El precio existe, pero el producto no está realmente disponible para
un aficionado cualquiera. Es una limitación del significado del dato, no del dato.
