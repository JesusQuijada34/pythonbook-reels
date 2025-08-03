# PythonBook Reels Downloader

**PythonBook Reels Downloader** es una aplicación multiplataforma y nativa construida con PyQt5 que permite descargar Reels de Facebook de manera rápida, sencilla e interactiva. Utiliza `yt-dlp` como motor de descarga, permitiendo elegir el formato/calidad del archivo resultante y guardar los videos en la carpeta que el usuario desee.

## Características

- **Multiplataforma:** Funciona en Windows, macOS y Linux.
- **Interfaz moderna:** UI agrupada, menús, tooltips y barra de estado.
- **Icono integrado:** Al lanzar la app aparece con el icono personalizado en la barra de tareas.
- **Descarga real:** Utiliza `yt-dlp` para obtener videos y audios directamente desde Facebook.
- **Selección de formato:** Descarga en calidad "best", MP4, WEBM o solo audio.
- **Progreso visual:** Barra de avance y notificaciones.
- **Menús de ayuda y salida.**

## Requisitos

- **Python 3.7 o superior**
- **PyQt5**
- **yt-dlp**

## Instalación

Sigue estos pasos para instalar y correr la aplicación:

### 1. Instala Python

Descarga e instala Python desde [python.org](https://www.python.org/).

### 2. Instala las dependencias

Abre la terminal o CMD y ejecuta:

```bash
pip install pyqt5 yt-dlp
```

### 3. Ejecuta la aplicación

En la terminal, navega hasta la carpeta donde está el archivo y ejecuta:

```bash
python app/pythonbook_reels_downloader.py
```

## Uso paso a paso (para principiantes)

1. **Abre la app**: Se mostrará la ventana principal con el icono personalizado.
2. **Ingresa la URL**: Copia y pega la URL del Reel de Facebook en el campo correspondiente.
   - Ejemplo: `https://facebook.com/reel/1234567890`
3. **Elige la carpeta de destino**: Haz clic en el botón "Elegir..." y selecciona donde se guardará el video.
4. **Selecciona el formato**: Escoge entre "best", "mp4", "webm" o "audio only" según tu preferencia.
5. **Haz clic en "Descargar"**:
   - Verás la barra de progreso avanzar.
   - Al finalizar, se mostrará una notificación con la ruta del archivo descargado.
6. **Abre tu carpeta** y disfruta del video.

## Menús y opciones

- **Archivo > Salir:** Cierra la aplicación.
- **Ayuda > Acerca de:** Muestra información sobre el programa.

## Solución de problemas

- Si ves el mensaje “yt-dlp no está instalado...”, ejecuta en terminal:  
  `pip install yt-dlp`
- Si el video no descarga:
  - Verifica la URL (debe ser pública).
  - Asegúrate de tener conexión a internet.
  - Prueba otro formato.

## Notas técnicas

- Para descargas de Reels privados o protegidos, puede requerirse autenticación, lo cual no está soportado en esta versión básica.
- El motor de descarga es `yt-dlp`, que se actualiza constantemente para soportar nuevos formatos y sitios.
- Puedes modificar el código para agregar nuevas funciones, como descargas por lote, soporte de cookies o integración con otras plataformas.

## Licencia

Este software se entrega bajo licencia MIT. Puedes usar, modificar y redistribuir libremente.

## Créditos

- Icono por el usuario
- Basado en PyQt5 y yt-dlp.

---

¡Gracias por usar PythonBook Reels Downloader!
