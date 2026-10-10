# 🚀 Microstock Automation Suite

Una herramienta automatizada en Python diseñada para creadores visuales e ilustradores digitales. Este script procesa directorios locales de ilustraciones (2D, 3D, Pixel Art y Vectores), valida requisitos técnicos y genera metadatos bilingües de forma autónoma para acelerar la distribución en agencias de microstock como Adobe Stock y Shutterstock.

## ⚙️ Características Principales

*   **Validación Geométrica (MP):** Analiza la densidad de píxeles de cada imagen sin saturar la memoria RAM. Alerta si un archivo no cumple con el estándar mínimo de la industria (4 Megapíxeles).
*   **Traducción Neuronal de Metadatos:** Extrae las palabras clave del nombre del archivo en español (ej. `robot_cyberpunk_cuantica.jpg`) y utiliza `deep-translator` para generar automáticamente los equivalentes en inglés (`robot`, `cyberpunk`, `quantum`).
*   **Priorización de Tags:** Combina los términos específicos del archivo con un núcleo de etiquetas universales de diseño, eliminando duplicados y limitando la salida al estándar de 50 palabras clave máximas.
*   **Exportación Estructurada:** Genera un archivo `.csv` con las cabeceras exactas exigidas por los portales de carga masiva (FTP) de las agencias de stock (`Filename`, `Title`, `Keywords`, `Category`, `Releases`).

## 🛠️ Requisitos del Sistema

*   Python 3.10 o superior.
*   `Pillow` (para el procesamiento ligero de imágenes).
*   `deep-translator` (para la traducción local de etiquetas).

## 📦 Instalación

1. Clona este repositorio en tu máquina local:
   ```bash
   git clone [https://github.com/TU_USUARIO/suite-automatizacion-microstock.git](https://github.com/TU_USUARIO/suite-automatizacion-microstock.git)
