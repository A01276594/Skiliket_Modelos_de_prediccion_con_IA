import pandas as pd

df_ECO2 = pd.read_csv('/Users/victoralejandrorojasgamez/Downloads/tareas_tec/skiliket/Skiliket_Modelos_de_prediccion_con_IA/data/csvs/device_1_ECO2.csv')
df_Humity = pd.read_csv('/Users/victoralejandrorojasgamez/Downloads/tareas_tec/skiliket/Skiliket_Modelos_de_prediccion_con_IA/data/csvs/device_1_Humidity.csv')
df_Noise = pd.read_csv('/Users/victoralejandrorojasgamez/Downloads/tareas_tec/skiliket/Skiliket_Modelos_de_prediccion_con_IA/data/csvs/device_1_Noise.csv')
df_Soil_Moisture = pd.read_csv('/Users/victoralejandrorojasgamez/Downloads/tareas_tec/skiliket/Skiliket_Modelos_de_prediccion_con_IA/data/csvs/device_1_Soil_Moisture.csv')
df_TVOC = pd.read_csv('/Users/victoralejandrorojasgamez/Downloads/tareas_tec/skiliket/Skiliket_Modelos_de_prediccion_con_IA/data/csvs/device_1_TVOC.csv')
df_UV_Intensity = pd.read_csv('/Users/victoralejandrorojasgamez/Downloads/tareas_tec/skiliket/Skiliket_Modelos_de_prediccion_con_IA/data/csvs/device_1_UV_Intensity.csv')
df_AQI = pd.read_csv('/Users/victoralejandrorojasgamez/Downloads/tareas_tec/skiliket/Skiliket_Modelos_de_prediccion_con_IA/data/csvs/device_2_AQI.csv')


print('\n')
print("""
      ********************
      ECO2
      ********************
      """)
for i, l in df_ECO2.head(30).iterrows():
    print(f'Fila {i}:')
    print(l)
    print('-' * 20) 
print('\n')
print('\n')
print('\n')

print('\n')
print("""
      ********************
      HUMINITY
      ********************
      """)
for i, l in df_Humity.head(30).iterrows():
    print(f'Fila {i}:')
    print(l)
    print('-' * 20) 
print('\n')
print('\n')
print('\n')


print('\n')
print("""
      ********************
      NOICE
      ********************
      """)
for i, l in df_Noise.head(30).iterrows():
    print(f'Fila {i}:')
    print(l)
    print('-' * 20) 
print('\n')
print('\n')
print('\n')

print('\n')
print("""
      ********************
      SOIL MOSTURE
      ********************
      """)
for i, l in df_Soil_Moisture.head().iterrows():
    print(f'Fila {i}:')
    print(l)
    print('-' * 20) 
print('\n')
print('\n')
print('\n')

print('\n')
print("""
      ********************
      TVOC
      ********************
      """)
for i, l in df_TVOC.head(30).iterrows():
    print(f'Fila {i}:')
    print(l)
    print('-' * 20) 
print('\n')
print('\n')
print('\n')

print('\n')
print("""
      ********************
      UV INTENSITY
      ********************
      """)
for i, l in df_UV_Intensity.head(30).iterrows():
    print(f'Fila {i}:')
    print(l)
    print('-' * 20) 
print('\n')
print('\n')
print('\n')

print('\n')
print("""
      ********************
      AQI
      ********************
      """)
for i, l in df_AQI.head(80).iterrows():
    print(f'Fila {i}:')
    print(l)
    print('-' * 20) 





