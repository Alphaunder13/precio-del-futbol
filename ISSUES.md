# Clubes descartados y limitaciones abiertas

Este archivo no es una lista de fallos. Que un club no publique su tarifario es
un resultado del estudio y se documenta aquí con la búsqueda exacta que se hizo,
para que cualquiera pueda repetirla.

Criterio de entrada: DECISIONS.md D-004. Los descartes viven también en
`data/descartados.csv`, que es lo que alimenta la página de Metodología.

---

## Clubes fuera del dataset v0.1.0

### Rayo Vallecano — `no_publicado`

- **Fecha de consulta:** 2026-07-27
- **Fuente revisada:** https://www.rayovallecano.es/noticias/campana-de-abonados-202627
- **Qué sí publica:** las cinco fases de renovación con sus fechas, las franjas
  de edad de cada modalidad, qué partidos cubre el abono (19 de LaLiga EA Sports
  más el primer partido de Copa como local) y las condiciones generales.
- **Qué no publica:** ni un solo precio.
- **Dónde está el precio:** solo dentro de la plataforma de renovación, a la que
  se accede con el abono de la temporada anterior.
- **Nota:** el club declara tener el cupo de abonados completo, de modo que la
  fase de altas nuevas solo se abre si se producen bajas.

### Sevilla FC — `no_publicado`

- **Fecha de consulta:** 2026-07-27
- **Fuente revisada:** https://sevillafc.es/actualidad/noticias/campana-abonos-2026-2027
- **Qué sí publica:** la estructura completa del producto. El asiento cubre los
  19 partidos de LaLiga EA Sports y el XV Trofeo Antonio Puerta; la cuota anual
  de socio se cobra aparte en enero de 2027; la cuota de alta de nuevo socio es
  de 125 €; la "regla de los 14 partidos" penaliza al abonado que no usa ni cede
  su asiento.
- **Qué no publica:** la tabla de precios por zona.
- **Dónde está el precio:** en el Portal del Socio, que exige número de abonado
  y PIN, y en `entradas.sevillafc.es`, que es el proceso de compra.
- **Nota:** el caso más llamativo del estudio. El club documenta con detalle las
  obligaciones del abonado y no documenta en abierto lo que cuesta serlo.

### Deportivo Alavés — `no_publicado`

- **Fecha de consulta:** 2026-07-28
- **Fuentes revisadas:**
  - https://deportivoalaves.com/abonados-temporada-26-27
  - https://deportivoalaves.com/condicionesabono-26-27
- **Qué sí publica:** el calendario completo de la campaña, el funcionamiento de
  la lista de espera, todas las ventajas del abono y el detalle de cada
  descuento (20% por desempleo acreditado ante Lanbide, 20% por discapacidad
  superior al 50%, descuento familiar progresivo desde el tercer miembro, 15%
  por club convenido, 10% por ser abonado de Baskonia). Publica incluso que la
  renovación tiene un 10% de descuento **respecto al precio de nuevas altas**.
- **Qué no publica:** el importe base sobre el que se aplican todos esos
  porcentajes. Ninguna de las dos páginas contiene una tabla de precios.
- **Nota:** es el caso más curioso. El club detalla con precisión los descuentos
  sobre un número que nunca enseña.

### Villarreal CF — `sin_confirmar`

- **Fecha de consulta:** 2026-07-28
- **Fuente revisada:** https://villarrealcf.es/es/campana-de-abonos-2026-27-seguim-amb-tu/
- **Qué pasó:** la página oficial de la campaña no llegó a cargar su contenido
  en ninguna de las consultas, ni antes ni después de rechazar las cookies. Se
  quedó permanentemente en estado de carga.
- **Por qué no es un `no_publicado`:** no se puede afirmar que el club no
  publique su tarifa. Solo que no se pudo comprobar. Marcarlo como no publicado
  sería atribuirle algo que no consta.
- **Pendiente:** repetir la comprobación. Es el candidato número uno para
  ampliar el dataset a nueve clubes.

---

## Limitaciones abiertas del dataset

### L-001 — El precio de nuevo abonado no está disponible en todos los clubes

Cuatro de los ocho clubes publican precio de nuevo abonado: Espanyol y Celta con
tarifa única, Málaga y Deportivo con dos tablas separadas de renovación y alta.
Osasuna publica el suplemento de alta (100 €) por separado. Getafe, Racing y
Levante solo publican renovación, porque sus campañas eran solo de renovación en
el momento de la consulta.

Efecto práctico: **el precio de esos tres clubes está infravalorado** respecto a
lo que pagaría alguien que se abona hoy. Se marca con confianza media, se avisa
en la ficha del club y hay un test que impide declararlos de confianza alta.

La magnitud del sesgo no es despreciable. En los clubes que publican ambos
precios, el alta cuesta entre un 19% y un 20% más que la renovación (Málaga
195 → 234 €, Deportivo 320 → 380 €).

### L-002 — Lo que cubre el abono no es idéntico

Osasuna excluye del carnet dos partidos de liga declarados "Día del Club": su
abono cubre 17 de los 19 partidos de liga en casa, y la Copa del Rey no está
incluida. Racing y Málaga incluyen los 19 de liga pero no la Copa. Getafe,
Espanyol, Celta, Deportivo y Levante incluyen liga y Copa.

El precio por partido corrige parte de esta diferencia, pero no toda.

### L-003 — Varios clubes tienen el aforo de abonados completo

Rayo Vallecano, Racing y Levante no vendían abonos nuevos en el momento de la
consulta. Osasuna solo admite altas de quienes tuvieran el carné 'Soy Rojillo'
la temporada anterior. Alavés y Celta funcionan por lista de espera. El precio
existe, pero el producto no está realmente disponible para un aficionado
cualquiera. Es una limitación del significado del dato, no del dato.

### L-004 — Racing publica el rango, no la tabla

El Racing es el único club del dataset cuyo precio no procede de una tabla de
tarifas, sino de una frase de su nota oficial: los carnés de adulto "oscilan
entre los 315 euros de Preferencia Sur y los 663 de Tribuna Oeste". La cifra es
oficial, del club, y nombra la zona, así que cumple el umbral. Pero no se puede
comprobar el resto de zonas ni si alguna modalidad adulta queda por debajo.

### L-005 — El dato salarial es de 2024 y los precios de 2026/27

No se actualiza a euros de hoy. Hacerlo obligaría a asumir una hipótesis de
inflación que el producto no necesita y que introduciría un supuesto discutible
en el número estrella. Se declara en Metodología.

### L-006 — La comunidad autónoma es una unidad gruesa

Ver DECISIONS.md D-007. Getafe y el centro de Madrid comparten cifra salarial.
Cornellà y Barcelona también. Es la desagregación más fina que publica el INE de
forma homogénea en esta estadística.
