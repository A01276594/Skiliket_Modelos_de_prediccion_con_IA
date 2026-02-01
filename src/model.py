import pandas as pd
import joblib
import os
from dotenv import load_dotenv

load_dotenv()
MODEL_PATH = os.getenv("MODEL_PATH")
_MODELO_CARGADO = None

def cargar_modelo() -> object | None:
    """
    Docstring para cargar_modelo
    
    :return: El modelo cargado para procesar los datos
    :rtype: object | None
    """
    global _MODELO_CARGADO
    if _MODELO_CARGADO:
        return _MODELO_CARGADO
    if os.path.exists(MODEL_PATH):
        _MODELO_CARGADO = joblib.load(MODEL_PATH)
        return _MODELO_CARGADO
    return None

def create_features_inference(df: pd.DataFrame) -> pd.DataFrame:
    """
    Docstring para create_features_inference
    
    :param df: El dataframe que se va a transformar
    :type df: DataFrame
    :return: El dataframe procesado y listo para ser predecido
    :rtype: DataFrame
    """
    df = df.copy()    
    df['hour'] = df.index.hour
    df['day_of_week'] = df.index.dayofweek    
    if 'aqi' in df.columns:
        df['aqi_lag_15'] = df['aqi'].shift(15)
        df['aqi_rolling_mean'] = df['aqi'].rolling(window=30).mean()
        df['aqi_volatility'] = df['aqi'].rolling(window=30).std()        
    if 'eco2' in df.columns:
        df['eco2_lag_15'] = df['eco2'].shift(15)
        df['eco2_diff'] = df['eco2'].diff()
        df['eco2_rolling_mean'] = df['eco2'].rolling(window=30).mean()
    return df

def predict_air_quality(df_reciente: pd.DataFrame) -> int:
    """
    Docstring para predict_air_quality
    
    :param df_reciente: El dataframe ya procesado y listo para ser predecido
    :type df_reciente: DataFrame
    :return: El numero de la calidad del aire
    :rtype: int
    """
    model = cargar_modelo()
    if not model:
        raise Exception(f"Modelo no encontrado en {MODEL_PATH}")    
    df_features = create_features_inference(df_reciente)
    features_row = df_features.tail(1)
    if hasattr(model, "feature_names_in_"):
        cols_modelo = model.feature_names_in_
        features_row = features_row[cols_modelo]
    prediction = model.predict(features_row)[0]
    return prediction

def es_alerta_peligrosa(prediccion_clase: int) -> bool:
    """
    Docstring para es_alerta_peligrosa
    
    :param prediccion_clase: El numero de la calidad del aire
    :type prediccion_clase: int
    :return: True si es peligrosa, False si no es peligrosa
    :rtype: bool
    """
    return prediccion_clase == 2