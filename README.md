# 🌳 Skiliket - Sistema de Predicción Ambiental con IA

![Python](https://img.shields.io/badge/Python-3.9%2B-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-Dashboard-red)
![Prefect](https://img.shields.io/badge/Prefect-Orchestration-orange)
![XGBoost](https://img.shields.io/badge/ML-XGBoost-green)

**Predicción proactiva de calidad del aire y alertas automatizadas mediante IoT y Machine Learning.**

---

## 📋 Descripción del Proyecto

[cite_start]Este proyecto transforma la red de sensores Skiliket de un sistema de monitoreo pasivo a uno **proactivo**[cite: 894]. [cite_start]Utilizando un modelo de aprendizaje automático (**XGBoost**), el sistema analiza variables ambientales críticas (CO2, TVOC, Humedad) para predecir la calidad del aire con **30 minutos de antelación**[cite: 39, 46, 897, 898].

[cite_start]El sistema orquesta la extracción de datos, la inferencia del modelo y la notificación de alertas a **Microsoft Teams** de forma autónoma [cite: 215, 277][cite_start], permitiendo una gestión eficiente de la ventilación y protegiendo la salud de los ocupantes del campus[cite: 385, 898].

### 🎯 Propósito
* [cite_start]**Vigilar:** Monitoreo 24/7 de los 10 dispositivos IoT distribuidos en el campus[cite: 221, 903].
* [cite_start]**Predecir:** Anticipar condiciones de riesgo (Clasificación "Peligro") antes de que ocurran[cite: 384, 895].
* [cite_start]**Alertar:** Notificaciones automáticas en tiempo real vía Webhooks de MS Teams[cite: 277, 916].
* [cite_start]**Visualizar:** Dashboard interactivo para la toma de decisiones basada en datos[cite: 339, 919].

---

## 📂 Estructura del Repositorio

```text
.
├── extras/
│   ├── data/                  # Datasets históricos y CSVs procesados [cite: 569, 904]
│   └── notebooks/             # Exploración (EDA), limpieza y pruebas de modelos [cite: 10, 587]
├── src/
│   ├── bot.py                 # Integración con Microsoft Teams (Adaptive Cards) [cite: 277, 940]
│   ├── data.py                # Ingesta y conexión con API Skiliket [cite: 928]
│   ├── model.py               # Lógica de ML: Feature engineering e inferencia [cite: 931]
│   ├── dashboard.py           # Interfaz visual (Streamlit) [cite: 339, 411]
│   ├── main.py                # Orquestador del flujo de trabajo [cite: 936]
│   ├── deploy.py              # Configuración del despliegue (Prefect Scheduler) [cite: 936]
│   └── utils/                 # Configuración y logging [cite: 329, 925]
├── requirements.txt           # Dependencias del proyecto
└── README.md                  # Documentación
```

## ⚙️ Arquitectura y Metodología

### 1. Pipeline de Datos (ETL)

**Ingesta**  
Conexión a la API de Skiliket para extraer ventanas móviles de datos de los últimos **60 min**.

**Limpieza**  
Filtrado automático de ruido de hardware para lecturas anómalas superiores a **5000 ppm**.

**Transformación**  
Generación de *lags* temporales (**t-15 min**) y promedios móviles para capturar la inercia del sistema.

---

### 2. Modelo de Predicción (Core ML)

**Algoritmo**  
XGBoost (*Extreme Gradient Boosting*).

**Estrategia**  
Clasificación de riesgo en **3 niveles**:
- 🟢 Verde — Seguro  
- 🟡 Amarillo — Precaución  
- 🔴 Rojo — Peligro  

**Entrenamiento**  
Datos históricos divididos en:
- **80%** entrenamiento  
- **20%** evaluación  

Se utilizó ponderación de muestras para penalizar errores en la clase crítica de peligro.

---

### 3. Automatización y Alertas

**Orquestación**  
Implementación de **Prefect** para ejecutar el flujo de análisis cada **30 minutos**.

**Notificaciones**  
Envío de tarjetas adaptativas a **Microsoft Teams** cuando se detecta una predicción de **Clase 2 (Peligro)**.

---

### 4. Visualización

**Dashboard**  
Construido en **Streamlit**, presenta el estado actual de los sensores y proyecciones a futuro.  
Incluye explicaciones interpretativas del modelo para facilitar la toma de decisiones.

---

## 🚀 Instalación y Despliegue

### Prerrequisitos
- Python **3.9** o superior  
- Acceso a la API de Skiliket  
- Webhook de canal de Microsoft Teams  

### Pasos de Instalación

**Clonar el repositorio**
```bash
git clone https://github.com/A01276594/Skiliket_Modelos_de_prediccion_con_IA.git
cd Skiliket_Modelos_de_prediccion_con_IA
```

**Instalar dependencias**
```bash
pip install -r requirements.txt
```

**Configurar Variables de Entorno**  
Crea un archivo `.env` en la raíz del proyecto con las siguientes claves:

```env
RUTA_CSV=
URL_API=
WEBHOOK_TEAMS=
MODEL_PATH=
DASHBOARD_URL=
```

---

## ▶️ Ejecución

### Modo Dashboard (Visualización)
Para ver las gráficas y el estado del sistema en tiempo real:

```bash
streamlit run src/dashboard.py
```

### Modo Producción (Servicio de Alertas)
Levanta el servicio de monitoreo continuo (ejecución cada 30 min):

```bash
python src/deploy.py
```

> Se recomienda usar **pm2** para mantener el proceso activo en el servidor.

---

## ⚠️ Limitaciones Conocidas

**Ruido en Sensores**  
Se han detectado dispositivos que reportan picos de CO₂ físicamente imposibles superiores a **55,000 ppm**.  
El sistema aplica filtros de rango, pero se sugiere revisión técnica del hardware.

**Intermitencia de Datos**  
No todos los sensores registran todos los parámetros de manera consistente, lo que puede afectar la confiabilidad de las predicciones en ciertas zonas.

---

## 🗺️ Roadmap y Próximos Pasos

- [ ] **Datos**: Incrementar el dataset histórico para capturar mejor la estacionalidad.  
- [ ] **Modelo**: Ajuste fino de los umbrales de alerta.  
- [ ] **Infraestructura**: Desacoplar el dashboard de la lógica de inferencia para mayor escalabilidad.  
- [ ] **Hardware**: Calibración física de la red de sensores.

---

## 👥 Contribución

Este proyecto fue desarrollado por el **Equipo A5** como parte del **Servicio Social – Invierno 2026**.

- Ángel Esparza Enríquez
- Francisco Alejandro Delgado García
- Víctor Alejandro Rojas Gámez
- Valeria Flores Medina  

**Estado:** 🟢 Funcional / En Mantenimiento

**Versión:** 1.0.0  
**Última actualización:** Febrero 2026  
**Estado:** En desarrollo activo con limitaciones de datos conocidas


