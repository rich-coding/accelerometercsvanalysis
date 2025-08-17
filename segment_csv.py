import pandas as pd
import os
import random
import shutil

# Establecer la semilla para reproducibilidad
random.seed(42)

# --- CONFIGURACIÓN INICIAL ---
# Carpeta con los archivos CSV de entrada
directorio_entrada = 'csv'
# Carpeta para guardar los segmentos de salida
directorio_salida = 'csv_segments'
# Duración de cada segmento en segundos
duracion_segmento_seg = 5
# Cantidad de segmentos a generar por cada archivo CSV
cantidad_segmentos = 50

# --- LÓGICA DEL SCRIPT ---

# 1. Verificar y preparar el directorio de salida
if os.path.exists(directorio_salida):
    print(f"Eliminando la carpeta existente: {directorio_salida}")
    shutil.rmtree(directorio_salida)
os.makedirs(directorio_salida)
print(f"Carpeta de salida '{directorio_salida}' creada.")

# 2. Listar todos los archivos CSV en el directorio de entrada
try:
    archivos_csv = [archivo for archivo in os.listdir(directorio_entrada) if archivo.endswith('.csv')]
    if not archivos_csv:
        print(f"No se encontraron archivos .csv en el directorio '{directorio_entrada}'.")
        exit()
except FileNotFoundError:
    print(f"Error: El directorio '{directorio_entrada}' no se encontró.")
    exit()

# 3. Procesar cada archivo CSV
for archivo_csv in archivos_csv:
    ruta_entrada = os.path.join(directorio_entrada, archivo_csv)
    
    try:
        # Cargar el archivo CSV en un DataFrame de pandas
        df_original = pd.read_csv(ruta_entrada)
        print(f"Procesando archivo: {archivo_csv}")

        # Renombrar la columna 'time' a 'timestamp' y eliminar la columna 'atotal'
        df_original.rename(columns={'time': 'timestamp'}, inplace=True)
        if 'atotal' in df_original.columns:
            df_original.drop(columns=['atotal'], inplace=True)

        # Calcular la duración total del archivo en segundos
        duracion_total_seg = df_original['timestamp'].iloc[-1]
        
        # Calcular la tasa de muestreo promedio y el número de filas por segmento
        # Calculamos el promedio de las diferencias de tiempo para una estimación más precisa
        tasa_muestreo_promedio_seg = df_original['timestamp'].diff().mean()
        filas_por_segmento = int(duracion_segmento_seg / tasa_muestreo_promedio_seg)

        # Generar los segmentos
        for i in range(cantidad_segmentos):
            # Calcular un punto de inicio aleatorio en segundos
            inicio_aleatorio_seg = random.uniform(0, duracion_total_seg - duracion_segmento_seg)
            
            # Encontrar el índice más cercano al punto de inicio
            inicio_index = (df_original['timestamp'] - inicio_aleatorio_seg).abs().idxmin()
            
            # Extraer el segmento del DataFrame
            segmento_df = df_original.iloc[inicio_index : inicio_index + filas_por_segmento].copy()
            
            # Crear el nombre del archivo de salida
            nombre_base = os.path.splitext(archivo_csv)[0]
            nombre_segmento = f"{nombre_base}_seg{i+1}.csv"
            ruta_salida = os.path.join(directorio_salida, nombre_segmento)
            
            # Guardar el segmento en un nuevo archivo CSV
            segmento_df.to_csv(ruta_salida, index=False)
            
        print(f"Se han generado {cantidad_segmentos} segmentos para {archivo_csv}.")
        
    except pd.errors.ParserError:
        print(f"Error: No se pudo leer el archivo '{archivo_csv}'. Asegúrate de que es un CSV válido.")
    except Exception as e:
        print(f"Ocurrió un error al procesar {archivo_csv}: {e}")

print("\nProceso de segmentación de archivos CSV completado.")