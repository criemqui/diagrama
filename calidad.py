import pandas as pd
import requests
import time
from typing import Set

# Función para cargar los datos demográficos
def ej_1_cargar_datos_demograficos() -> pd.DataFrame:
    url_demographics = "https://public.opendatasoft.com/explore/dataset/us-cities-demographics/download/?format=csv&timezone=Europe/Berlin&lang=en&use_labels_for_header=true&csv_separator=%3B"
    demographics_data = pd.read_csv(url_demographics, sep=';')
    return demographics_data

# Función para limpiar nombres de ciudades
def limpiar_nombre_ciudad(ciudad: str) -> str:
    # Reemplazar caracteres especiales y manejar nombres complejos
    ciudad_limpia = ciudad.replace("/", " ").replace("-", " ").replace(",", "")
    ciudad_limpia = ciudad_limpia.split(" ")[0]  # Tomar solo la primera parte del nombre si es muy largo
    return ciudad_limpia

# Función para cargar los datos de calidad del aire
def ej_2_cargar_calidad_aire(ciudades: Set[str]) -> pd.DataFrame:
    api_url = "https://api.api-ninjas.com/v1/airquality"
    api_key = "34BYjFN2PlUWoh9prtD7BA==7ftQC1mYRzd8yt3B"  # Asegúrate de reemplazar esto con tu propia clave de API

    air_quality_data = []

    for ciudad in ciudades:
        city, state = ciudad.split(", ")
        city = limpiar_nombre_ciudad(city)
        try:
            # Hacer una solicitud a la API para obtener la calidad del aire de la ciudad
            response = requests.get(api_url, headers={"X-Api-Key": api_key}, params={"city": city})
            response.raise_for_status()  # Lanza una excepción para códigos de estado 4xx/5xx
            data = response.json()
            # Tomar el elemento "concentration" de cada entrada
            concentration = data.get("overall_aqi")  # Cambiar "concentration" a "overall_aqi" si es necesario
            if concentration is not None:
                air_quality_data.append({"City": city, "State": state, "Air Quality Concentration": concentration})
            else:
                air_quality_data.append({"City": city, "State": state, "Air Quality Concentration": float("nan")})
        except requests.exceptions.RequestException as e:
            print(f"Error obteniendo datos para {city}, {state}: {e}")
            air_quality_data.append({"City": city, "State": state, "Air Quality Concentration": float("nan")})
        # Pausa para evitar superar el límite de solicitudes a la API
        time.sleep(1)

    air_quality_df = pd.DataFrame(air_quality_data)
    return air_quality_df

# Usar las funciones definidas
demographics_data = ej_1_cargar_datos_demograficos()

# Crear un conjunto de ciudades con formato "City, State"
ciudades = {f"{row['City']}, {row['State']}" for index, row in demographics_data.iterrows()}

air_quality_df = ej_2_cargar_calidad_aire(ciudades)

# Imprimir los primeros registros del DataFrame de calidad del aire
print(air_quality_df.head())
