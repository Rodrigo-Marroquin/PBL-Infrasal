# Justificación de plataforma: por qué web y no app

Se eligió una aplicación web en lugar de una app nativa por la realidad operativa de la planta de IMACASA:

- **Quién la usa.** (1) Operarios de línea, que trabajan de pie y con equipo de protección personal, como guantes industriales. La interfaz usa botones amplios y alto contraste para manipularla con guantes; la pantalla pequeña de un smartphone es ineficiente y propensa a toques accidentales. (2) El supervisor de calidad, que consulta el tablero de las tres estaciones y el historial filtrable.
- **Dónde se usa.** El operario, junto a su estación (PC08, PC10 o PC12), donde el uso de teléfonos personales suele estar restringido por seguridad ocupacional (distracción o caída del dispositivo en la maquinaria). El supervisor, desde la oficina de calidad.
- **Con qué dispositivo.** En planta: monitores táctiles industriales o tablets reforzadas montadas en un brazo fijo en cada estación. El dispositivo pertenece a la estación, siempre está encendido y no depende del teléfono del operario. En la oficina: la PC del supervisor o su celular, fuera de la línea.
- **Despliegue y mantenimiento.** Con una arquitectura web centralizada, si en los próximos 6 meses se actualiza el modelo de IA o se agrega una estación, los cambios se reflejan al recargar el navegador. Una app nativa obligaría a instalar actualizaciones en cada dispositivo, lo que complica el mantenimiento de TI. Además, la web recibe los resultados en tiempo real por WebSocket desde la misma API.
