import pandas as pd
import numpy as np
from xgboost import XGBClassifier
from sklearn.metrics import classification_report, accuracy_score
from sklearn.preprocessing import LabelEncoder
from sklearn.utils.class_weight import compute_sample_weight

AGGRESSIVENESS = 3.0 

def categorize_aqi(val) -> int:
    """
    Docstring para categorize_aqi
    
    :param val: El valor del dato sin transformar
    :return: Los datos transformados
    :rtype: int
    """
    if pd.isna(val): return val
    if val <= 1: return 0  # Verde (Seguro)
    if val == 2: return 1  # Amarillo (Precaucion)
    return 2               # Rojo (Peligro: incluye 3, 4, 5)

def prepare_data(df_list) -> pd.DataFrame:
    """
    Docstring para prepare_data
    
    :param df_list: La lista de dataframes
    :return: El dataframe unido con todas las variables que usamos
    :rtype: DataFrame
    """
    processed_list = []
    for df in df_list:
        temp_df = df.copy()
        temp_df['time'] = pd.to_datetime(temp_df['time']).dt.round('1min')
        temp_df = temp_df[['time', 'value']]        
        if 'type' in df.columns:
            sensor_name = df['type'].iloc[0].lower().replace(" ", "_")
        else:
            sensor_name = "sensor"
        temp_df = temp_df.rename(columns={'value': sensor_name})
        temp_df = temp_df.drop_duplicates('time').set_index('time')
        processed_list.append(temp_df)
    main_df = pd.concat(processed_list, axis=1, sort=True)
    main_df = main_df.interpolate(method='time').ffill()
    return main_df

def create_features(df) -> pd.DataFrame:
    """
    Docstring para create_features
    
    :param df: El dataframe con todas las variables unidas
    :return: Un dataframe transformado y adaptado al modelo
    :rtype: DataFrame
    """
    df = df.copy()
    df.columns = [c.lower() for c in df.columns]    
    df['hour'] = df.index.hour
    df['day_of_week'] = df.index.dayofweek
    if 'aqi' in df.columns:
        df['aqi_lag_15'] = df['aqi'].shift(15)
        df['aqi_rolling_mean'] = df['aqi'].rolling(window=30).mean()
        df['aqi_volatility'] = df['aqi'].rolling(window=30).std()
        future_aqi = df['aqi'].shift(-30)       
        df['target_aqi_future'] = future_aqi.apply(categorize_aqi)        
    if 'eco2' in df.columns:
        df['eco2_lag_15'] = df['eco2'].shift(15)
        df['eco2_diff'] = df['eco2'].diff()
        df['eco2_rolling_mean'] = df['eco2'].rolling(window=30).mean()    
    return df.dropna()

def train_model(df) -> XGBClassifier:
    """
    Docstring para train_model
    
    :param df: El dataframe adaptado al modelo
    :return: El modelo entrenado para predecir la calidad del aire
    :rtype: XGBClassifier
    """
    features = [col for col in df.columns if col != 'target_aqi_future']
    X = df[features]
    y_raw = df['target_aqi_future'].round().astype(int)    
    split_point = int(len(df) * 0.8)
    X_train = X.iloc[:split_point]
    X_test = X.iloc[split_point:]
    y_train_raw = y_raw.iloc[:split_point]
    y_test_raw = y_raw.iloc[split_point:]
    le = LabelEncoder()
    y_train = le.fit_transform(y_train_raw)    
    weights = compute_sample_weight(class_weight='balanced', y=y_train)
    danger_class = 2
    if danger_class in le.classes_:
        danger_idx_transformed = le.transform([danger_class])[0]
        danger_indices = np.where(y_train == danger_idx_transformed)[0]
        weights[danger_indices] *= AGGRESSIVENESS
    else:
        print("No hay aqi de calidad 3, 4 o 5")
    y_test = []
    known_classes = set(le.classes_)
    for label in y_test_raw:
        if label in known_classes:
            y_test.append(le.transform([label])[0])
        else:
            closest = min(known_classes, key=lambda x: abs(x-label))
            y_test.append(le.transform([closest])[0])
    y_test = np.array(y_test)
    model = XGBClassifier(
        n_estimators=100,
        learning_rate=0.1,
        max_depth=5,
        objective='multi:softmax',
        num_class=len(le.classes_), 
        random_state=42
    )    
    model.fit(X_train, y_train, sample_weight=weights)    
    preds = model.predict(X_test)
    print("-" * 60)
    print(f"Accuracy: {accuracy_score(y_test, preds)}")
    print("-" * 60)
    class_names_map = {0: 'Verde (Seguro)', 1: 'Amarillo (Precaucion)', 2: 'Rojo (Peligro)'}
    target_names = [class_names_map.get(cls, str(cls)) for cls in le.classes_]
    try:
        print(classification_report(y_test, preds, target_names=target_names))
    except:
        print(classification_report(y_test, preds))
    print("-" * 60)
    return model


if __name__ == "__main__":
    print("Iniciando entrenamiento")    
    base_path = '/Users/victoralejandrorojasgamez/Downloads/tareas_tec/skiliket/Skiliket_Modelos_de_prediccion_con_IA/data/csvs/'
    try:
        df_eco2 = pd.read_csv(base_path + 'device_2_ECO2.csv')
        df_hum = pd.read_csv(base_path + 'device_1_Humidity.csv')
        df_tvoc = pd.read_csv(base_path + 'device_2_TVOC.csv')
        df_aqi = pd.read_csv(base_path + 'device_2_AQI.csv')        
        main_df = prepare_data([df_eco2, df_hum, df_tvoc, df_aqi])
        final_df = create_features(main_df)
        my_model = train_model(final_df)
        print("Modelo entrenado")
    except Exception as e:
        print(f"Ocurrió un error inesperado: {e}")