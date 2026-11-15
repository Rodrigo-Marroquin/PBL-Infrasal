# Propuesta conceptual de captura en planta (PC12 Inyectado)

> Texto para la sección de Arquitectura y servicios (punto 2 del PDF). Las referencias continúan la numeración IEEE de la Sección 3 (Persona 2): [8] es ArUco, ya citado allí.

## Requisitos que fija el análisis de defectos

La sección 4 define qué necesita ver la cámara. Los seis puntos de PC12 se dividen en tres tipos de captura:

- **Superficie y color** (óxido en hoja, mal inyectado por color o humedad): luz difusa y uniforme, sin brillos del acero.
- **Micro-relieve** (líneas de flujo, huellas): luz rasante a 15–20° que convierte el relieve en sombra.
- **Contorno y medida** (mal desbarbado, pollera tapada, largo, ancho y desface de cacha): silueta de alto contraste más una referencia de escala en milímetros.

Ninguna iluminación sirve para las tres cosas a la vez: la rasante crea las sombras que la difusa elimina, y el backlight oculta la superficie. Por eso la cabina **no usa una sola foto por pieza, sino una secuencia de capturas, una por cada tipo de luz**.

## Cámaras

**Cámara de área, no lineal.** En PC12 el operario coloca el machete en un soporte fijo y la pieza no se mueve durante la inspección. Una cámara lineal necesita que la pieza pase a velocidad constante, con un encoder, y eso obligaría a añadir una banda transportadora. La cámara de área captura la pieza completa estando quieta.

**Obturador global.** Todas las filas del sensor se exponen al mismo tiempo. Esto es necesario porque cada luz se enciende solo unos 15 ms: con obturador rodante (*rolling shutter*), parte de la imagen quedaría con la luz equivocada. También evita deformaciones si hay vibración en la planta.

**Resolución.** Se calcula con la regla de la sección 4 (δ_min ≥ 3 × GSD). Supuestos: machete de hasta 24" (≈ 610 mm) y campo de visión de 680 mm para incluir margen y los marcadores ArUco.

| | CAM-1 cenital | CAM-2 perfil |
|---|---|---|
| Uso | Caras A/B: superficie, contorno, medidas | Perfil de la cacha: desface |
| Modelo propuesto | Basler ace 2 a2A4096-9gcBAS [10] | Basler ace 2 a2A2448-23gcBAS [13] |
| Sensor | Sony IMX545, 1/1.1", 2.74 µm, obturador global | Sony IMX547, 1/1.8", 2.74 µm, obturador global [15] |
| Resolución | 4096 × 3000 (12 MP), ≈ 9 fps | 2448 × 2048 (5 MP), 23 fps |
| Interfaz | GigE | GigE |
| Lente | 16 mm, C-mount, 1.1", 12 MP (Basler C11-1620-12M [12]) | 12 mm, C-mount, ≥ 5 MP |
| Campo de visión | ≈ 680 × 498 mm | ≈ 200 × 167 mm |
| Distancia de trabajo (WD = f·FOV/ancho sensor) | ≈ 970 mm | ≈ 360 mm |
| Tamaño de píxel en la pieza (GSD) | 0.166 mm/px | 0.082 mm/px |
| Defecto mínimo detectable (3 × GSD) | **≈ 0.5 mm** | **≈ 0.25 mm** |

Alternativa equivalente para CAM-1: Teledyne FLIR Blackfly S BFS-PGE-122S6C-C (Sony IMX304, 4096 × 3000, 3.45 µm, obturador global, GigE con PoE, 10 fps) [11]. Se prefiere la Basler por su píxel más pequeño, que permite un sensor y un lente más compactos con la misma resolución.

Se elige **GigE** porque admite cables de hasta 100 m entre la cabina y el equipo edge, algo común en planta, frente a los ~5 m de USB3.

**Si el defecto mínimo real resulta menor a 0.5 mm** (por ejemplo, rebabas muy finas), se añade una tercera cámara enfocada solo en la cacha. Esa zona mide ≈ 165 mm y concentra 5 de los 6 defectos, así que con una cámara de 5 MP se bajaría a ≈ 0.25 mm.

## Iluminación

| Luz | Tipo | Posición | Defectos que revela |
|---|---|---|---|
| **L1** | 2 paneles LED difusos, 6000 K, con film polarizador | Arriba, a ±45°, fuera del cono de visión | Óxido, color, puntos de humedad |
| **L2** | 2 barras LED | A ambos lados del machete, a 15–20° sobre la placa | Líneas de flujo y huellas (mal inyectado) |
| **L3** | Panel backlight LED | Bajo una placa de acrílico esmerilado | Silueta: rebabas, pollera tapada, largo y ancho |
| **L4** | Panel de contraluz pequeño | Pared opuesta a CAM-2 | Silueta de perfil: desface de cacha |

**Polarización cruzada.** El acero templado de la hoja refleja la luz como un espejo, y esos brillos se confunden con defectos (riesgo 3 de la Sección 3). Se usa un filtro polarizador sobre L1 y otro sobre el lente de CAM-1, girado 90°: la reflexión especular conserva la polarización y queda bloqueada, mientras la luz difusa de la superficie sí pasa.

**Disparo secuencial.** Un controlador de iluminación multicanal (por ejemplo, Gardasoft serie RT, 4 canales [14]) recibe la señal del sensor de presencia, enciende una luz a la vez y dispara la cámara correspondiente (Fig. C):

| Captura | Luz | Cámara | Modelo que la usa |
|---|---|---|---|
| F1 | L1 difusa + polarizador | CAM-1 | EfficientAD (óxido, color) |
| F2 | L2 rasante | CAM-1 | EfficientAD (mal inyectado) |
| F3 | L3 backlight | CAM-1 | EfficientAD (rebabas, pollera) + YOLO26-seg (largo, ancho) |
| F4 | L4 contraluz | CAM-2 | YOLO26-seg + ArUco (desface) |

La secuencia completa dura ≈ 0.35 s por cara, limitada por los ≈ 9 fps de CAM-1. Con la inferencia en el equipo edge, el veredicto llega a la UI en menos de 0.5 s. El operario voltea la pieza y se repiten F1–F3 para la cara B; F4 (perfil) se toma una sola vez, así que son 7 capturas por machete, así que el ciclo total queda dominado por la manipulación manual y no por la captura.

## Soporte (cabina)

- **Estructura:** perfil de aluminio 40 × 40 mm y paneles negros mate. Medidas aproximadas: 800 mm de ancho × 600 mm de fondo × 1250 mm de alto. Los paneles aíslan la captura de la luz variable de la planta (ventanas, lámparas, hora del día), que de otro modo cambiaría la apariencia de las piezas y generaría falsos rechazos.
- **Acceso:** abertura frontal con cortina para cargar y voltear la pieza.
- **Placa de apoyo:** acrílico esmerilado de 5 mm, que también funciona como difusor del backlight L3.
- **Posicionamiento repetible:** un tope en el extremo de la cacha y dos pines a lo largo del lomo de la hoja. Así cada machete queda siempre en la misma posición, lo que simplifica la comparación contra la plantilla del molde.
- **Referencia de escala:** dos marcadores ArUco de 40 mm en esquinas opuestas de la placa y una regla milimétrica fija como verificación visual, dentro del campo de visión [8]. Con ellos se convierten píxeles a milímetros en cada imagen y se detecta si la cámara se movió. La distorsión del lente se corrige una vez, en la instalación, con un patrón de tablero de ajedrez.
- **Disparo:** un sensor fotoeléctrico de presencia en el tope detecta la pieza colocada e inicia la secuencia.
- **Conexión:** CAM-1 y CAM-2 van por GigE (switch con PoE) al equipo edge definido en la arquitectura. El controlador de luces se conecta por Ethernet o E/S digital.

Figuras: A, corte longitudinal; B, corte transversal; C, secuencia de disparo (archivos `fig-a…`, `fig-b…`, `fig-c….svg`).

## Supuestos

1. Largo máximo del machete: 24" (610 mm). Si IMACASA tiene modelos más largos, se aumenta la WD o se usa un lente de 12 mm.
2. El defecto mínimo de interés es ≥ 0.5 mm. Hay que confirmarlo con muestras reales en la fase piloto.
3. Las tolerancias dimensionales se toman de la plantilla 2D del molde, no de un CAD.
4. El espesor no se mide con visión 2D: queda con calibrador, por muestreo.

## Referencias (continúan la numeración de la Sección 3)

[10] Basler AG, "a2A4096-9gcBAS," *Basler Product Documentation*. [Online]. Available: https://docs.baslerweb.com/a2a4096-9gcbas

[11] Teledyne FLIR, "Blackfly S BFS-PGE-122S6 — Specifications and frame rates." [Online]. Available: https://softwareservices.flir.com/BFS-PGE-122S6/latest/Model/spec.html

[12] Basler AG, "Basler Lens C11-1620-12M f16mm." [Online]. Available: https://www.baslerweb.com/en/shop/basler-lens-c11-1620-12m-f16mm/

[13] Basler AG, "Basler ace 2 R a2A2448-23gcBAS." [Online]. Available: https://www.baslerweb.com/en-sg/shop/a2a2448-23gcbas/

[14] Novus Light Technologies Today, "Control of multi-lighting schemes for machine vision" (Gardasoft). [Online]. Available: https://www.novuslight.com/control-of-multi-lighting-schemes-for-machine-vision_N5884.html

[15] FRAMOS, "Sony IMX547 — Pregius S global shutter sensor." [Online]. Available: https://framos.com/en/products/imx547aamj-c-24265
