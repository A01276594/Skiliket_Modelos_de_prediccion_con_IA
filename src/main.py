import pandas as pd
from prefect import flow, task
from data import obtener_datos_recientes
from model import predict_air_quality, es_alerta_peligrosa
from bot import enviar_alerta_teams
from utils.config import DEVICES_MAP
from utils.logger import Logger

@task(retries=2, name="Procesar Sensor")
def procesar_sensor(device_id: int) -> str | None:
    """
    Docstring para procesar_sensor
    
    :param device_id: El numero del dispositivo skilliket
    :type device_id: int
    :return: Los datos del dispositivo o None si no hay datos
    :rtype: str | None
    """
    nombre_ubicacion = DEVICES_MAP.get(device_id, f"Dispositivo {device_id}")    
    categorias = ["ECO2", "Humidity", "TVOC", "AQI"]
    data_dict = {}
    try: 
        for cat in categorias:
            raw_data = obtener_datos_recientes(device_id, cat, minutos=60)
            if not raw_data:
                Logger.warning(f"Sin datos para sensor {device_id} - {cat}")
                return None
            df_temp = pd.DataFrame(raw_data)
            df_temp['time'] = pd.to_datetime(df_temp['time'])
            df_temp = df_temp[['time', 'value']].rename(columns={'value': cat.lower()}).set_index('time')
            data_dict[cat.lower()] = df_temp        
        if len(data_dict) != len(categorias):
             return f"Sensor {device_id} datos incompletos"
        df_sensor = pd.concat(data_dict.values(), axis=1).interpolate(method='time').ffill()
        clase_predicha = predict_air_quality(df_sensor)
        aqi_actual = df_sensor['aqi'].iloc[-1]    
        if es_alerta_peligrosa(clase_predicha):
            enviar_alerta_teams(
                valor_aqi=aqi_actual, 
                ubicacion=nombre_ubicacion, 
                estado_txt="🚨 PELIGRO: Calidad mala", 
                color_card="Attention"
            )
        return f"Sensor {device_id} procesado correctamente"
    except Exception as e:
        Logger.error(f"Error procesando sensor {device_id}: {str(e)}")
        return f"Error en sensor {device_id}"

@flow(name="Monitoreo Total Calidad Aire")
def air_quality_global_flow():
    for d_id in range(1, 11):
        procesar_sensor(d_id)

if __name__ == "__main__":
    air_quality_global_flow()