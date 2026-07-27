# Decisiones de diseño

Registro de las decisiones que condicionan el producto. Se escribe antes de
recoger datos y solo se modifica añadiendo entradas nuevas, nunca reescribiendo
las anteriores.

---

## D-001 — El problema del comparable

**Fecha:** 2026-07-27
**Estado:** vigente

Los clubes de LaLiga EA Sports no fijan precios de forma comparable entre sí.
Las diferencias detectadas antes de recoger ningún dato:

- **Por zona del estadio.** Un club puede tener cuatro zonas y otro dieciséis.
  "El abono más barato" no significa lo mismo en los dos.
- **Por categoría de partido.** Algunos clubes clasifican los partidos en
  categorías (A/B/C, oro/plata/bronce) y el precio de la entrada suelta depende
  del rival. Otros usan precio único o precio dinámico.
- **Por condición del comprador.** Socio, abonado, no socio, nuevo abonado,
  renovación. El mismo asiento tiene precios distintos según quién lo compre.
- **Por edad.** Infantil, joven, adulto, sénior, con cortes de edad distintos en
  cada club.
- **Por estructura del producto.** Algunos clubes separan cuota de socio y
  abono; otros los integran en un pago único.

Comparar mal invalida el producto entero. Un ranking que enfrente el abono de
tribuna de un club con el de fondo de otro no mide nada.

---

## D-002 — Métrica 1: `abono_adulto_mas_barato`

**Fecha:** 2026-07-27
**Estado:** vigente

El precio del abono de temporada completa de liga que cumple **todas** estas
condiciones a la vez:

1. **Adulto sin descuento.** La modalidad general para una persona adulta, sin
   carné joven, infantil, sénior, de discapacidad, de desempleo ni ningún otro
   descuento por condición personal.
2. **Zona más económica del estadio.** La localidad de menor precio disponible
   en la campaña de abonos, sea cual sea su nombre comercial.
3. **Precio de nuevo abonado.** El que paga alguien que se abona por primera
   vez, no el de renovación. Si el club solo publica el de renovación, el
   registro baja de confianza y se anota.
4. **Temporada completa de liga en casa.** Cubre los 19 partidos de LaLiga EA
   Sports como local. Si el abono incluye obligatoriamente otras competiciones,
   se anota en la nota del registro.
5. **Precio final que paga el aficionado**, con IVA y con los cargos
   obligatorios que el club publique junto al precio.

### Qué queda excluido, explícitamente

- Carné joven, infantil, bebé, sénior o jubilado.
- Cuotas de socio que no den derecho a asiento.
- Promociones puntuales, precios de lanzamiento y descuentos por pronto pago.
- Zonas de hospitality, palcos, VIP, butacas premium y áreas con servicios.
- Packs, abonos de media temporada y abonos de solo copa o solo Europa.
- Localidades de visitante.
- Abonos de fútbol femenino, filial o categorías inferiores.

### Cuando el club integra cuota de socio y abono

Si para acceder al abono es **obligatorio** pagar además una cuota de socio, el
precio registrado es la **suma** de ambos conceptos, y se anota el desglose en
la nota. Es lo que desembolsa realmente el aficionado, que es lo que el producto
mide. Si la cuota es opcional, no se suma.

---

## D-003 — Métrica 2: `entrada_suelta_mas_barata`

**Fecha:** 2026-07-27
**Estado:** vigente

El precio de la entrada individual más barata para **un partido de liga de
categoría intermedia**, adulto, sin descuentos, en la zona más económica.

- Si el club clasifica los partidos en categorías, se toma la **intermedia**.
  Con número par de categorías, la inmediatamente inferior a la mediana (criterio
  conservador: se prefiere no inflar el precio).
- Si el club **no** usa categorías, se registra el precio único y se hace
  constar el hecho en la nota. Que un club no segmente por rival es información,
  no un vacío.
- Si el club usa **precio dinámico** y el precio depende del momento de compra,
  se registra el precio visible en la fecha de consulta y se marca `estimacion`,
  porque no es reproducible.

### Exclusiones

Las mismas de D-002, más: partidos de copa, europeos y amistosos.

---

## D-004 — Umbral de calidad para entrar al dataset

**Fecha:** 2026-07-27
**Estado:** vigente

Un club entra en la versión v0.1.0 **solo si** tiene un
`abono_adulto_mas_barato` verificable con fuente oficial del club, accesible sin
iniciar sesión y sin entrar en un proceso de compra.

`entrada_suelta_mas_barata` es deseable pero **no** bloqueante: un club puede
entrar con el abono verificado y la entrada como `no_publicado`.

Si el club no alcanza el umbral, queda fuera y se documenta en `ISSUES.md` la
búsqueda realizada. Es preferible un dataset de 8 clubes sólidos que uno de 12
con huecos.

---

## D-005 — Estados de verificación

**Fecha:** 2026-07-27
**Estado:** vigente

| Estado | Significado |
|---|---|
| `verificado` | Visible en la web oficial del club sin iniciar sesión, con URL y fecha de consulta. |
| `estimacion` | Derivado de una fuente pública que no es el tarifario oficial, o no reproducible (precio dinámico). Se indica la fuente. |
| `no_publicado` | El club no publica ese precio de forma accesible sin registro o sin entrar en la compra. **Es un hallazgo, no un fallo.** |
| `sin_confirmar` | No se pudo determinar. |

Un precio nunca se infiere ni se estima a ojo. Si no se encuentra, es
`no_publicado` o `sin_confirmar`.

---

## D-006 — Ética de recolección

**Fecha:** 2026-07-27
**Estado:** vigente

- Solo información visible públicamente **sin iniciar sesión**.
- Si el precio únicamente aparece dentro del proceso de compra o tras registro,
  se marca `no_publicado`. No se completan flujos de compra ni se crean cuentas.
- Se respeta `robots.txt`. Ritmo humano, sin scraping agresivo. La recolección
  de v0.1.0 es manual y asistida, no automatizada.
- No se recoge ningún dato personal.
- El dataset registra la URL exacta consultada para que cualquiera pueda
  reproducir la comprobación.

---

## D-007 — Fuente salarial

**Fecha:** 2026-07-27
**Estado:** vigente

El precio relativo se expresa en **horas de trabajo al salario medio de la
comunidad autónoma del club**.

> **Corregido el 2026-07-27, antes de cargar ningún dato.** La versión inicial
> de esta decisión decía "provincia". Al ir a la fuente resultó que la Encuesta
> Anual de Estructura Salarial del INE publica el salario bruto medio anual por
> trabajador desagregado por **comunidad autónoma**, no por provincia. Se cambia
> la unidad geográfica en lugar de buscar una fuente provincial de peor calidad
> o de mezclar dos estadísticas distintas.

- Fuente: INE, Encuesta Anual de Estructura Salarial (EAES), salario bruto medio
  anual por trabajador y comunidad autónoma. Último dato definitivo disponible:
  **2024**, publicado en 2026. Salario medio nacional de referencia:
  29.540,26 €.
- Cada cifra que entra en `data/salarios.csv` se comprueba una a una contra la
  publicación del INE. No se vuelca la tabla entera de golpe: solo entran las
  comunidades autónomas de los clubes que están en el dataset.
- Se usa **salario bruto**, no neto: el neto depende de la situación personal de
  cada contribuyente y no es comparable entre provincias sin supuestos que el
  producto no quiere asumir.
- Conversión a hora: **1.800 horas anuales**, equivalente a una jornada completa
  de 40 horas semanales con 14,5 días de vacaciones y festivos al mes descontados
  de forma aproximada. Es un divisor convencional y explícito; está en
  `config/index_weights.yaml` y cualquiera puede cambiarlo y recalcular.
- El dato del INE va con retraso respecto a la temporada. Se registra el año de
  referencia de la estadística y se declara en Metodología. **No se actualiza a
  euros de hoy**: hacerlo introduciría un supuesto de inflación que el producto
  no necesita.

### Limitación asumida

El salario medio autonómico no es la renta de la persona que va al fútbol. La
métrica no dice "un aficionado trabaja N horas", dice "el abono equivale a N
horas al salario medio de su comunidad autónoma". Es una unidad de comparación
territorial, no una medida de esfuerzo individual. Se declara así en la página
de Metodología.

Además, la comunidad autónoma es una unidad gruesa: mete en el mismo saco a
Getafe y al centro de Madrid, o a Cornellà y a Barcelona. Se asume y se declara.

---

## D-008 — Índice determinista

**Fecha:** 2026-07-27
**Estado:** vigente

El índice se calcula por reglas. Mismo dato de entrada, mismo resultado, siempre.
Sin aprendizaje automático, sin aleatoriedad, sin llamadas a modelos.

Todos los pesos, divisores y umbrales viven en `config/index_weights.yaml`.
Ninguno se escribe en el código.

Cualquier cifra mostrada en la interfaz debe poder expandirse hasta ver la
operación que la produce y los datos que la alimentan.

---

## D-009 — Idioma

**Fecha:** 2026-07-27
**Estado:** vigente

Todo el texto visible va en español de España desde el primer commit. El copy
está centralizado en `config/copy_es.yaml`; el código no contiene cadenas
literales destinadas al usuario.

Únicas excepciones admitidas en inglés: nombre del producto, marcas, nombres
propios y nombres oficiales de competición (por ejemplo, "LaLiga EA Sports").
La lista cerrada vive en `config/app_config.yaml` y hay un test que la vigila.

---

## D-010 — El precio del abono se guarda descompuesto

**Fecha:** 2026-07-27
**Estado:** vigente
**Motivo:** surgió al recoger los tres primeros clubes.

Varios clubes cobran un **suplemento por darse de alta** como abonado nuevo, que
no forma parte de la tarifa de la zona. Osasuna cobra 100 € el primer año.
Sevilla FC cobra 125 €. Getafe no lo publica porque su campaña es solo de
renovación.

Si se guardara un único número, sería imposible saber qué contiene. Por eso cada
registro de `abono_adulto_mas_barato` guarda tres campos:

| Campo | Contenido |
|---|---|
| `precio_base_eur` | Tarifa publicada de la zona más barata para adulto. |
| `suplemento_alta_eur` | Coste de alta de nuevo abonado, si el club lo publica. |
| `precio_eur` | La suma. Es el número que ordena el ranking (D-002). |

`estado_suplemento_alta` usa el mismo enum de D-005. Cuando vale `no_publicado`,
`precio_eur` es igual a `precio_base_eur` y **el registro baja a confianza
media**, porque el precio real de un abonado nuevo es necesariamente igual o
mayor. La ficha del club lo dice con esas palabras: el dato puede estar
infravalorado.

Las tres cifras se muestran siempre en la ficha del club. Ningún número del
ranking es opaco.

---

## D-011 — Los partidos incluidos se guardan por club

**Fecha:** 2026-07-27
**Estado:** vigente
**Motivo:** surgió al recoger los tres primeros clubes.

No todos los abonos cubren lo mismo, y la diferencia no es menor:

- Espanyol y Getafe incluyen los 19 partidos de liga en casa **y** la Copa del
  Rey.
- Osasuna incluye **17** de los 19 de liga: dos jornadas se declaran "Día del
  Club" y se pagan aparte (50 € cada una si se añaden fuera de la renovación).
  La Copa del Rey no está incluida.

Por eso `partidos_liga_incluidos` e `incluye_copa` son columnas del dataset y no
una nota al pie. El **precio por partido de liga** se calcula dividiendo entre
`partidos_liga_incluidos` de ese club, no entre 19 fijos. Dividir por 19 en todos
los casos daría a Osasuna un precio por partido artificialmente bajo.

---

## D-012 — No publicar el precio es un dato, no una ausencia

**Fecha:** 2026-07-27
**Estado:** vigente

Al recoger los primeros clubes aparecieron dos casos, Rayo Vallecano y Sevilla
FC, en los que el club publica en abierto las fases, las fechas, las franjas de
edad y hasta las obligaciones del abonado, pero **no el precio**. La tarifa solo
existe dentro de la plataforma de renovación o del proceso de compra.

Estos clubes no entran en el ranking, porque D-004 exige precio verificable. Pero
**sí entran en el producto**: la página de Metodología publica el recuento de
clubes que no publican tarifa, con la URL revisada y la fecha, y `ISSUES.md`
guarda la búsqueda completa.

El producto responde a "cuánto cuesta ir al fútbol". "No se puede saber sin
identificarse" es una respuesta legítima a esa pregunta y se comunica como tal.

---

## D-013 — Las gradas de acceso condicionado quedan fuera

**Fecha:** 2026-07-28
**Estado:** vigente
**Motivo:** surgió al comparar ocho clubes.

Casi todos los clubes tienen alguna localidad barata a la que **no puede acceder
cualquiera**: gradas de animación (Levante Fans 1909, Arabako Garrasia, Grada
Animación del Espanyol), gradas de peñas (Deportivo) y zonas de movilidad
reducida (Málaga, Espanyol, Racing).

Ninguna entra en `abono_adulto_mas_barato`, aunque a veces sea la más económica.
El motivo es el mismo en los tres casos: exigen pertenecer a un colectivo o
acreditar una condición personal, y D-002 pide el precio que paga un adulto
cualquiera sin condiciones. Se anota en la nota de cada club cuando aplica.

Lo mismo vale para los descuentos por ser accionista del club (Levante), por
antigüedad (Racing, Sevilla) o por convenio: son condiciones personales.

---

## D-014 — Las estadísticas oficiales se leen en formato máquina

**Fecha:** 2026-07-28
**Estado:** vigente
**Motivo:** se detectó un error real durante la carga.

Al cargar los salarios se consultó dos veces la misma nota de prensa del INE y
las dos lecturas **no coincidieron**: una asignaba a Comunitat Valenciana la
cifra que la otra daba a Cantabria. Una tercera consulta devolvió valores de un
año distinto. El error era de transcripción al leer una tabla de texto, no del
organismo.

A partir de ahora los datos estadísticos se descargan de la interfaz de datos
del INE en formato máquina y se procesan con código, sin ningún resumen de por
medio:

```
https://servicios.ine.es/wstempus/js/ES/DATOS_TABLA/28191?nult=1
```

La cifra nacional que devuelve esa consulta (29.540,26 € en 2024) coincide con
la publicada, lo que sirve de comprobación cruzada.

**Regla general:** si un dato existe en formato máquina, se toma de ahí. Leer
una tabla a ojo es una fuente de error silenciosa, y este producto no puede
permitirse un salario mal asignado: contamina todo el ranking de esa comunidad.
