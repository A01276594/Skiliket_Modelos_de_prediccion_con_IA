import requests
from datetime import datetime, timedelta
import os

def obtener_datos_recientes(device_id: int, categoria: str, minutos: int = 60) -> list[dict]:
    """
    Docstring para obtener_datos_recientes
    
    :param device_id: El numero del dispositivo skilliket
    :type device_id: int
    :param categoria: El nombre de la categoria
    :type categoria: str
    :param minutos: El rango de tiempo atras que se va a recolletar
    :type minutos: int
    :return: La lista con los datos del dispositivo y categoria solicitados
    :rtype: list[dict]
    """
    ahora = datetime.now()
    inicio = (ahora - timedelta(minutes=minutos)).strftime("%Y-%m-%d %H:%M:%S")
    final = ahora.strftime("%Y-%m-%d %H:%M:%S")
    url = f"{os.getenv('URL_API')}/devices/{device_id}/devicemeasurements"
    params = {
        "type": categoria,
        "start": inicio,
        "end": final
    }
    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json().get("data", [])