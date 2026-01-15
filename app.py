import requests
import csv
from typing import List, Dict
BASE_URL = "https://app.skiliket.net/server/api/v1"

PERIODO_INICIO = "2025-01-07%2000:00:00"
PERIODO_FINAL = "2026-01-14%2023:59:59"

def obtener_measurements_types(device_id: int) -> List[str]:
    """
    Docstring para obtener_measurements_types
    
    :param device_id: El id del dispositivo (1-10)
    :type device_id: int
    :return: Todos los tipos de cosas que mide ese dispositivo en particular
    :rtype: json
    """
    url = f"{BASE_URL}/devices/{device_id}/devicemeasurements/types"
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()
    return data["data"]


def obtener_mediciones(device_id: int, categoria: str) -> List[Dict]:
    """
    Docstring para obtener_mediciones
    
    :param device_id: El id del dispositivo (1-10)
    :type device_id: int
    :param categoria: El nombre de la medicion (Lo que mide)
    :type categoria: str
    :return: Los datos de esas mediciones
    :rtype: jsoon
    """
    url = (
        f"{BASE_URL}/devices/{device_id}/devicemeasurements?type={categoria}&start={PERIODO_INICIO}&end={PERIODO_FINAL}"
    )
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()
    if isinstance(data, dict) and "data" in data:
        return data["data"]
    if isinstance(data, list):
        return data
    return []


def exportar_device_categoria_csv(device_id: int, categoria: str, data: List[Dict]) -> None:
    """
    Docstring para exportar_device_categoria_csv
    
    :param device_id: El id del dispositivo (1-10)
    :type device_id: int
    :param categoria: El nombre de la medicion (Lo que mide)
    :type categoria: str
    :param data: Los datos de las mediciones
    :type data: List[Dict]
    """
    nombre_archivo = f"data/device_{device_id}_{categoria.replace(' ', '_')}.csv"
    with open(nombre_archivo, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow([
            "id",
            "device_id",
            "type",
            "time",
            "latitude",
            "longitude",
            "value",
            "created_at",
            "updated_at"
        ])
        for item in data:
            writer.writerow([
                item.get("id"),
                device_id,
                item.get("type"),
                item.get("time"),
                item.get("latitude"),
                item.get("longitude"),
                item.get("value"),
                item.get("created_at"),
                item.get("updated_at")
            ])
    print(f"CSV creado: {nombre_archivo}")


def exportar_todos_los_devices() -> None:
    """
    Docstring para exportar_todos_los_devices
    Funcion principal para crear los csv de toda la info
    """
    for device_id in range(1, 11):
        print(f"\nProcesando dispositivo: {device_id}")
        try:
            categorias = obtener_measurements_types(device_id)
        except Exception as e:
            print(f"Error obteniendo categorías: {e}")
            continue
        for categoria in categorias:
            print(f"Medida: {categoria}")
            try:
                data = obtener_mediciones(device_id, categoria)
            except Exception as e:
                print(f"Error obteniendo datos: {e}")
                continue
            if not isinstance(data, list):
                print(f"Respuesta inesperada: {data}")
                continue
            if not data:
                print("Sin datos")
                continue
            exportar_device_categoria_csv(device_id, categoria, data)

if __name__ == '__main__':
    exportar_todos_los_devices()