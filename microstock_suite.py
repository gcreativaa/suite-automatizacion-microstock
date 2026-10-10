import os
import csv
from PIL import Image

class MicrostockAutomator:
    def __init__(self, directorio_arte):
        """
        Inicializa la suite de automatización.
        Define la ruta donde están tus ilustraciones listas para procesar.
        """
        self.directorio = directorio_arte
        # Formato estándar de metadatos requerido por Adobe Stock y Shutterstock
        self.columnas_csv = ['Filename', 'Title', 'Keywords', 'Category', 'Releases']
        self.datos_exportacion = []

    def validar_dimensiones(self, ruta_imagen):
        """
        Abre la imagen y verifica sus dimensiones.
        Las plataformas de microstock suelen requerir un mínimo de 4 Megapíxeles.
        """
        try:
            with Image.open(ruta_imagen) as img:
                ancho, alto = img.size
                megapixeles = (ancho * alto) / 1000000
                if megapixeles >= 4.0:
                    return True
                else:
                    print(f"⚠️ Advertencia: {os.path.basename(ruta_imagen)} tiene {megapixeles:.1f} MP. Podría ser rechazada por ser muy pequeña.")
                    return False
        except Exception as e:
            print(f"Error al leer la imagen {ruta_imagen}: {e}")
            return False

    def generar_metadatos(self, nombre_archivo):
        """
        Núcleo de procesamiento de texto. Toma el nombre del archivo, lo limpia,
        y genera un título descriptivo junto con un bloque de 50 palabras clave priorizadas.
        """
        # Limpiamos el nombre del archivo (ej. "robot_cyberpunk_01.jpg" -> "robot cyberpunk")
        nombre_base = os.path.splitext(nombre_archivo)[0]
        titulo_limpio = nombre_base.replace('_', ' ').replace('-', ' ').capitalize()
        
        # Diccionario base de expansión. 
        # Aquí puedes inyectar tus algoritmos de NLP o diccionarios bilingües.
        tags_universales = [
            "illustration", "ilustracion", "design", "diseño", "graphic", "grafico",
            "art", "arte", "digital", "creative", "creativo", "background", "fondo",
            "concept", "concepto", "vector", "2d", "isolated", "aislado", "modern"
        ]
        
        # Extraemos palabras clave específicas del título
        tags_especificos = titulo_limpio.lower().split()
        
        # Combinamos y eliminamos duplicados, asegurando que los tags específicos vayan primero
        todas_las_keywords = tags_especificos + tags_universales
        keywords_unicas = list(dict.fromkeys(todas_las_keywords))
        
        # Limitamos a 50 palabras clave (estándar máximo de la industria)
        keywords_finales = ", ".join(keywords_unicas[:50])
        
        return titulo_limpio, keywords_finales

    def procesar_directorio(self):
        """
        Itera sobre cada ilustración, valida, genera metadatos y prepara la tabla de datos.
        """
        print(f"🔍 Escaneando el directorio: {self.directorio}...\n")
        
        archivos_validos = [f for f in os.listdir(self.directorio) if f.lower().endswith(('.jpg', '.jpeg', '.png', '.eps'))]
        
        if not archivos_validos:
            print("No se encontraron ilustraciones en el directorio.")
            return

        for archivo in archivos_validos:
            ruta_completa = os.path.join(self.directorio, archivo)
            
            # Verificamos si la imagen cumple con los requisitos técnicos
            self.validar_dimensiones(ruta_completa)
            
            # Generamos el título y los tags bilingües
            titulo, keywords = self.generar_metadatos(archivo)
            
            # Agregamos la fila a nuestra base de datos en memoria
            # Category '1' suele ser genérica (Ilustraciones/Arte), 'Releases' queda en blanco si no hay personas reales
            self.datos_exportacion.append({
                'Filename': archivo,
                'Title': titulo,
                'Keywords': keywords,
                'Category': '1', 
                'Releases': ''
            })
            
            print(f"✅ Procesado: {archivo}")

    def exportar_csv(self, nombre_salida="metadatos_stock.csv"):
        """
        Escribe los datos estructurados en un archivo CSV listo para subir a las plataformas.
        """
        if not self.datos_exportacion:
            return
            
        ruta_salida = os.path.join(self.directorio, nombre_salida)
        
        with open(ruta_salida, mode='w', newline='', encoding='utf-8') as archivo_csv:
            escritor = csv.DictWriter(archivo_csv, fieldnames=self.columnas_csv)
            escritor.writeheader()
            for fila in self.datos_exportacion:
                escritor.writerow(fila)
                
        print(f"\n🚀 ¡Éxito! CSV de metadatos generado impecablemente en: {ruta_salida}")

# ==========================================
# Ejecución principal del programa
# ==========================================
if __name__ == "__main__":
    # Define la carpeta donde tienes tus ilustraciones o pixel art.
    # Usa '.' para el directorio actual, o una ruta absoluta como 'C:/Usuarios/TuNombre/Arte_Terminado'
    CARPETA_ARTE = './mis_ilustraciones' 
    
    # Si la carpeta no existe, la creamos para evitar errores
    if not os.path.exists(CARPETA_ARTE):
        os.makedirs(CARPETA_ARTE)
        print(f"Se ha creado la carpeta '{CARPETA_ARTE}'. Por favor, coloca allí tus diseños y vuelve a ejecutar el script.")
    else:
        # Instanciamos la clase y ejecutamos el flujo de trabajo
        automatizador = MicrostockAutomator(CARPETA_ARTE)
        automatizador.procesar_directorio()
        automatizador.exportar_csv()