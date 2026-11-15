# Aclaraciones para el equipo

Actualizado el 14 de noviembre de 2026. Las secciones 3 y 4 de esta carpeta son las versiones corregidas de ese día.

## 1. Cuántos machetes se necesitan: ≈ 460

| | Antes | Ahora |
|---|---|---|
| Machetes OK | 58 | **200** |
| Machetes con defecto | 260 | 260 |
| Total | 318 | **≈ 460** |

Solo cambiaron los machetes OK. Los 260 con defecto siguen igual.

### Por qué cambió

El cálculo anterior era 400 imágenes OK ÷ 7 capturas por machete ≈ 58 machetes. Ese cálculo trata las 7 capturas de un machete como intercambiables, y no lo son, porque cada una se toma con una luz distinta:

- con luz difusa (L1) se ven el color y el óxido;
- con luz rasante (L2) se ven los relieves y las líneas de flujo;
- con backlight (L3) se ve solo la silueta.

EfficientAD aprende cómo se ve una pieza normal. Si se entrena mezclando las tres luces, aprende que lo normal es cualquiera de esas tres apariencias y deja de notar los defectos. Por eso se entrena un modelo por luz, y cada modelo necesita sus propias 400 imágenes OK tomadas con esa luz.

Cada machete da 2 imágenes por luz (cara A y cara B):

    400 imágenes OK con L1 ÷ 2 por machete = 200 machetes OK

Con esos mismos 200 machetes salen también las 400 de L2 y las 400 de L3, porque cada machete pasa por las tres luces.

Un ejemplo: si se quieren 400 fotos de perfil de personas y cada persona da una sola foto de perfil, hacen falta 400 personas. Que cada una dé además fotos de frente no ayuda, porque esas no sirven para el álbum de perfiles.

El 58 no fue un error de quien escribió la sección: salió de una sugerencia equivocada que se le dio al equipo.

### Cifras finales (Tabla 4.2 de la sección 4)

| Concepto | Cálculo | Resultado |
|---|---|---|
| Machetes OK | 400 OK por luz ÷ 2 | 200 |
| Imágenes OK | 200 machetes × 7 capturas | 1 400 |
| Imágenes con defecto | 120 + 80 + 60 + 50 + 120 + 90 | 520 |
| Machetes con defecto | 520 ÷ 2 capturas útiles por pieza | 260 |
| Total de imágenes | 1 400 + 520 | 1 920 |
| Total de machetes | 200 + 260 | ≈ 460 |

### Qué decir si preguntan

- Los 200 machetes OK no cuestan nada: se fotografían piezas buenas de la producción normal y se devuelven a la línea.
- Los difíciles de conseguir son los 260 con defecto. Por eso la sección 4 dice que es una cifra de referencia y que las piezas salen del contenedor de rechazo o se provocan ajustando la inyectora.
- Se podría bajar a 300 OK por luz (150 machetes), pero se debilita el argumento basado en MVTec AD. La sección 4 mantiene 200.

## 2. Diferencias entre secciones

Las versiones corregidas de las secciones 3 y 4 ya coinciden con la propuesta de captura en estos puntos:

| Tema | Antes | Ahora en las tres partes |
|---|---|---|
| Fondo | La sección 4 decía fondo negro o gris mate | Placa de acrílico esmerilado sobre el backlight; paneles interiores negros mate |
| Iluminación | La sección 4 decía "luz dual" | Cuatro luces: L1 difusa polarizada, L2 rasante, L3 backlight, L4 contraluz de perfil |
| Modelos de anomalías | Un solo EfficientAD | Un EfficientAD-S por luz (L1, L2 y L3) |

El diagrama de arquitectura (`docs/arquitectura.*`) se actualizó con las 7 capturas por machete y un modelo por luz.

### Ajustes hechos después (14 de noviembre)

Las tres diferencias que quedaban ya están corregidas en los archivos de esta carpeta:

| Tema | Cómo quedó | Archivo cambiado |
|---|---|---|
| Capturas por machete | 7: en la cara B se repiten F1–F3 y F4 (perfil) se toma una sola vez | `captura/seccion-captura-pc12.md` y `captura/fig-c-secuencia-disparo.svg` |
| Referencia de escala | Dos marcadores ArUco de 40 mm y una regla milimétrica fija como verificación visual | `captura/seccion-captura-pc12.md` |
| Formato de fecha de la UI | `es-SV` (El Salvador) | `ui/prototipo-ui-pc12.html` |

También se agregó `ui/justificacion-web.md` (por qué web y no app), y `/info` ahora devuelve `"equipo": "Tenazas"`. Las evidencias de `docs/evidencias/` se rehicieron con ese nombre. La URL del túnel y las credenciales de prueba no cambiaron.
