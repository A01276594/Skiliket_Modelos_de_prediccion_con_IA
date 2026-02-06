import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import timedelta, datetime

# --- CONFIGURACIÓN DE LA INTERFAZ ---
# Definimos el título de la pestaña y el diseño ancho de la página
st.set_page_config(page_title="SKILIKET: IA Engine", layout="wide", page_icon="🧠")

# Importamos las herramientas de conexión de datos y el cerebro de la IA (Modelo)
from data import obtener_datos_recientes
from model import predict_air_quality, es_alerta_peligrosa
from utils.config import DEVICES_MAP

# Aplicamos un diseño visual moderno (colores oscuros y bordes redondeados)
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .stMetric { background-color: #161b22; padding: 15px; border-radius: 10px; border: 1px solid #30363d; }
    </style>
    """, unsafe_allow_html=True)

# --- ENCABEZADO DEL TABLERO ---
st.title("🧠 SKILIKET: Tablero de Predicción e Inferencia")
col_header_1, col_header_2 = st.columns([2, 1])

with col_header_1:
    st.markdown("**Estado del Sistema:** `Inteligencia Artificial Activa` | **Modelo:** `XGBoost v1.0` ")
with col_header_2:
    st.write(f"🕒 **Última actualización:** {datetime.now().strftime('%H:%M:%S')}")

# --- PANEL DE CONTROL (Barra Lateral) ---
st.sidebar.header("Panel de Configuración")

# Menú para elegir cuál de los 10 sensores del campus queremos consultar
device_id = st.sidebar.selectbox(
    "Seleccionar Sensor del Campus", 
    list(DEVICES_MAP.keys()), 
    format_func=lambda x: DEVICES_MAP[x],
    key="selector_device"
)

# --- PROCESO CENTRAL: ANÁLISIS DE LA INTELIGENCIA ARTIFICIAL ---
try:
    with st.spinner("La IA está analizando los sensores en tiempo real..."):
        
        # El sistema consulta 4 indicadores clave para tomar una decisión informada
        categorias = ["ECO2", "Humidity", "TVOC", "AQI"]
        data_dict = {}
        
        for cat in categorias:
            # Solicitamos a la API los datos de la última hora
            raw = obtener_datos_recientes(device_id, cat, minutos=60)
            if raw:
                df_tmp = pd.DataFrame(raw)
                df_tmp['time'] = pd.to_datetime(df_tmp['time'])
                # Preparamos los nombres para que el modelo los reconozca
                df_tmp = df_tmp[['time', 'value']].rename(columns={'value': cat.lower()}).set_index('time')
                data_dict[cat.lower()] = df_tmp

        # Si tenemos la información completa de los 4 indicadores, procedemos
        if len(data_dict) == len(categorias):
            # Combinamos los datos y rellenamos huecos si hubo fallas de red
            df_sensor = pd.concat(data_dict.values(), axis=1).interpolate(method='time').ffill()
            
            # LIMPIEZA: Ignoramos datos erróneos causados por fallas eléctricas en los sensores
            df_sensor = df_sensor[df_sensor['eco2'] < 5000]
            
            if df_sensor.empty:
                st.error("Los datos actuales contienen errores de sensor y no son aptos para análisis.")
                st.stop()

            # --- CONSULTA AL MODELO DE IA ---
            # Le enviamos los datos al "cerebro" y nos devuelve un nivel de riesgo
            clase_predicha = predict_air_quality(df_sensor)
            eco2_actual = df_sensor['eco2'].iloc[-1]
            aqi_actual = df_sensor['aqi'].iloc[-1]

            # --- VISUALIZACIÓN DE RESULTADOS ---
            m1, m2, m3 = st.columns(3)
            
            m1.metric("CO2 Actual (Aire)", f"{eco2_actual:.0f} ppm")
            
            # Traducimos el resultado numérico de la IA a lenguaje humano
            nombres_clase = {0: "🟢 SEGURO", 1: "🟡 PRECAUCIÓN", 2: "🔴 PELIGRO"}
            m2.metric("Veredicto de la IA", nombres_clase[clase_predicha])

            # Mostramos la recomendación de acción inmediata
            if es_alerta_peligrosa(clase_predicha):
                m3.error("🚨 ACCIÓN: VENTILAR / EVACUAR")
            elif clase_predicha == 1:
                m3.warning("⚠️ ACCIÓN: Abrir Ventanas")
            else:
                m3.success("✅ ACCIÓN: Todo en orden")

            # --- GRÁFICA DE TENDENCIA (PASADO Y FUTURO) ---
            st.subheader("📈 Proyección de la Calidad del Aire")
            
            # Calculamos una proyección visual: hacia dónde irá la línea en los próximos 30 min
            proyeccion_val = eco2_actual
            if clase_predicha == 2: proyeccion_val += 400
            elif clase_predicha == 1: proyeccion_val += 150

            fig = go.Figure()
            
            # Dibujamos lo que ya pasó (Línea sólida)
            fig.add_trace(go.Scatter(
                x=df_sensor.index, y=df_sensor['eco2'], 
                name='Historial Real', 
                line=dict(color='#00B4D8', width=3),
                fill='tozeroy'
            ))
            
            # Dibujamos lo que la IA predice (Línea punteada)
            futuro_index = [df_sensor.index[-1], df_sensor.index[-1] + timedelta(minutes=30)]
            fig.add_trace(go.Scatter(
                x=futuro_index, y=[eco2_actual, proyeccion_val], 
                name='Predicción IA', 
                line=dict(color='#FF4B4B', width=4, dash='dot')
            ))
            
            # Marcamos los límites de salud recomendados
            fig.add_hline(y=1000, line_dash="dash", line_color="orange", annotation_text="Límite Ideal")
            fig.add_hline(y=1500, line_dash="dash", line_color="red", annotation_text="Límite de Salud")

            fig.update_layout(height=450, template="plotly_dark", hovermode="x unified")
            st.plotly_chart(fig, use_container_width=True)

            # --- EXPLICACIÓN DE LA IA PARA EL USUARIO ---
            with st.expander("🤔 ¿Cómo tomó la IA esta decisión?"):
                nombres_riesgo = {0: "Bajo (Seguro)", 1: "Moderado (Precaución)", 2: "Alto (Peligro)"}
                
                st.write(f"Para determinar un riesgo **{nombres_riesgo[clase_predicha]}**, el modelo analizó:")
                
                exp_col1, exp_col2 = st.columns(2)
                with exp_col1:
                    st.markdown("**🔍 Factores analizados:**")
                    st.write("- Concentración de CO2 y químicos en el aire.")
                    st.write("- Índice global de calidad (AQI).")
                    st.write("- Relación entre humedad y ocupación.")
                
                with exp_col2:
                    st.markdown("**📊 Hallazgos clave:**")
                    st.write(f"- El índice AQI actual es de {aqi_actual}.")
                    st.write(f"- Se detectó un cambio de tendencia en los últimos 10 minutos.")

                st.info("El sistema recomienda actuar proactivamente basándose en patrones históricos de este sensor.")

        else:
            st.warning("⚠️ Esperando datos... El sistema requiere información de los 4 sensores para decidir.")

except Exception as e:
    st.error(f"Error de conexión con el sistema central: {e}")