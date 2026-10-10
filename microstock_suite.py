import os
import csv
from PIL import Image
from deep_translator import GoogleTranslator

class MicrostockAutomator:
    def __init__(self, directorio_arte):
        """
        Inicializa la suite de automatización con capacidad de traducción.
        """
        self.directorio = directorio_arte
        self.columnas_csv = ['Filename', 'Title', 'Keywords', 'Category', 'Releases']
        self.datos_exportacion = []
        # Inicializamos el traductor de Español a Inglés
        self.traductor = GoogleTranslator(source='es', target='en')

    def validar_dimensiones(self, ruta_imagen):
        """
        Verifica que la ilustración supere los 4 Megapíxeles.
        """
        try:
            with Image.open(ruta_imagen) as img:
                ancho, alto = img.size
                megapixeles = (ancho * alto) / 1000000
                if megapixeles >= 4.0:
                    return True
                else:
                    print(f"⚠️ Advertencia: {os.path.basename(ruta_imagen)} tiene {megapixeles:.1f} MP. Podría ser rechazada.")
                    return False
        except Exception as e:
            print(f"Error al leer la imagen {ruta_imagen}: {e}")
            return False

    def generar_metadatos(self, nombre_archivo):
        """
        Genera el título y traduce automáticamente las palabras clave al inglés,
        creando un bloque de metadatos bilingüe y priorizado.
        """
        nombre_base = os.path.splitext(nombre_archivo)[0]
        titulo_limpio = nombre_base.replace('_', ' ').replace('-', ' ').capitalize()
        
        tags_universales = [
            "illustration", "ilustracion", "design", "diseño", "graphic", "grafico",
            "art", "arte", "digital", "creative", "creativo", "background", "fondo",
            "concept", "concepto", "vector", "2d", "isolated", "aislado", "modern"
        ]
        
        tags_especificos_es = titulo_limpio.lower().split()
        
        print(f"   Traduciendo tags para: '{titulo_limpio}'...")
        tags_especificos_en = []
        for palabra in tags_especificos_es:
            try:
                traduccion = self.traductor.translate(palabra)
                if traduccion:
                    tags_especificos_en.append(traduccion.lower())
            except Exception:
                pass # Si falla una palabra, continuamos sin detener el script
                
        # Combinamos español, inglés y universales
        todas_las_keywords = tags_especificos_es + tags_especificos_en + tags_universales
        keywords_unicas = list(dict.fromkeys(todas_las_keywords))
        
        # Limitamos a 50 palabras clave
        keywords_finales = ", ".join(keywords_unicas[:50])
        
        return titulo_limpio, keywords_finales

    def procesar_directorio(self):
        """
        Itera sobre las ilustraciones, valida, traduce y prepara la tabla.
        """
        print(f"🔍 Escaneando el directorio: {self.directorio}...\n")
        archivos_validos = [f for f in os.listdir(self.directorio) if f.lower().endswith(('.jpg', '.jpeg', '.png', '.eps'))]
        
        if not archivos_validos:
            print("No se encontraron ilustraciones en el directorio.")
            return

        for archivo in archivos_validos:
            ruta_completa = os.path.join(self.directorio, archivo)
            self.validar_dimensiones(ruta_completa)
            titulo, keywords = self.generar_metadatos(archivo)
            
            self.datos_exportacion.append({
                'Filename': archivo,
                'Title': titulo,
                'Keywords': keywords,
                'Category': '1', 
                'Releases': ''
            })
            print(f"✅ Procesado y traducido: {archivo}")

    def exportar_csv(self, nombre_salida="metadatos_stock.csv"):
        """
        Escribe los datos estructurados en el archivo CSV.
        """
        if not self.datos_exportacion:
            return
            
        ruta_salida = os.path.join(self.directorio, nombre_salida)
        with open(ruta_salida, mode='w', newline='', encoding='utf-8') as archivo_csv:
            escritor = csv.DictWriter(archivo_csv, fieldnames=self.columnas_csv)
            escritor.writeheader()
            for fila in self.datos_exportacion:
                escritor.writerow(fila)
                
        print(f"\n🚀 ¡Éxito! CSV de metadatos generado en: {ruta_salida}")

if __name__ == "__main__":
    CARPETA_ARTE = './mis_ilustraciones' 
    if not os.path.exists(CARPETA_ARTE):
        os.makedirs(CARPETA_ARTE)
        print(f"Carpeta '{CARPETA_ARTE}' creada. Coloca tus diseños allí y ejecuta de nuevo.")
    else:
        automatizador = MicrostockAutomator(CARPETA_ARTE)
        automatizador.procesar_directorio()
        automatizador.exportar_csv()
