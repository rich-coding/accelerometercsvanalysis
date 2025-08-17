import pandas as pd
import matplotlib.pyplot as plt

def plot_data(file_path):
    """
    Lee un archivo CSV con datos de aceleración y genera un gráfico de líneas.

    Args:
        file_path (str): La ruta al archivo CSV.
    """
    try:
        # 1. Lee el archivo CSV usando pandas
        # 'usecols' especifica las columnas que nos interesan, evitando errores
        df = pd.read_csv(file_path, usecols=['time', 'ax', 'ay', 'az', 'atotal'])

        # 2. Crea la figura y los ejes para el gráfico
        plt.figure(figsize=(12, 6))

        # 3. Genera un gráfico de línea para cada eje y el total
        plt.plot(df['time'], df['ax'], label='Eje X (ax)')
        plt.plot(df['time'], df['ay'], label='Eje Y (ay)')
        plt.plot(df['time'], df['az'], label='Eje Z (az)')
        plt.plot(df['time'], df['atotal'], label='Total (atotal)', linestyle='--', linewidth=2.5)

        # 4. Añade títulos y etiquetas para mayor claridad
        plt.title('Aceleración vs. Tiempo', fontsize=16)
        plt.xlabel('Tiempo (s)', fontsize=12)
        plt.ylabel('Aceleración (m/s²)', fontsize=12)
        plt.grid(True)
        plt.legend()

        # 5. Muestra el gráfico
        plt.show()

    except FileNotFoundError:
        print(f"Error: El archivo '{file_path}' no se encontró.")
    except KeyError:
        print("Error: El archivo CSV no contiene las columnas requeridas ('time', 'ax', 'ay', 'az', 'atotal').")

# Ruta a tu archivo CSV. Asegúrate de que esta ruta sea correcta.
csv_file = 'csv\sample.csv'  # Cambia 'your_data.csv' por el nombre de tu archivo

# Llama a la función para generar el gráfico
plot_data(csv_file)