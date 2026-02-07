# Skiliket - Modelos de Predicción con IA

## Descripción del Proyecto

Sistema de predicción basado en inteligencia artificial para anticipar tendencias ambientales utilizando datos históricos de dispositivos IoT Skiliket. El proyecto implementa un modelo de machine learning que analiza variables ambientales para generar alertas y recomendaciones proactivas, ayudando en la toma de decisiones sostenibles.

### Pregunta Guía
**¿Cómo puede la IA predecir comportamientos ambientales y apoyar la toma de decisiones sostenibles?**

---

## Propósito

Explorar el uso de inteligencia artificial para:
- Anticipar tendencias ambientales
- Generar alertas tempranas basadas en patrones históricos
- Proporcionar recomendaciones para decisiones sostenibles
- Visualizar predicciones en tiempo real mediante un dashboard interactivo

---

## Estructura del Proyecto

```
.
├── extras/
│   ├── data/
│   │   ├── csvs/              # Archivos CSV generales
│   │   ├── devices/           # Datos por dispositivo
│   │   │   ├── device_1/
│   │   │   │   ├── variables/ # Variables específicas del dispositivo
│   │   │   │   ├── pivot_1.csv
│   │   │   │   └── pivot_1_min.csv
│   │   │   ├── device_2/
│   │   │   └── ...
│   │   ├── var/               # Datos de variables
│   │   └── other/             # Otros datos
│   └── notebooks/
│       ├── Visualización/     # Notebooks de visualización
│       └── devices_cleaning/  # Notebooks de limpieza de datos
├── src/
│   ├── resources/             # Recursos del proyecto
│   ├── utils/                 # Utilidades y funciones auxiliares
│   ├── bot.py                 # Bot de alertas (si aplica)
│   ├── dashboard.py           # Dashboard de Streamlit
│   ├── data.py                # Procesamiento de datos
│   ├── deploy.py              # Script de despliegue
│   ├── main.py                # Punto de entrada principal
│   └── model.py               # Definición y entrenamiento del modelo
├── requirements.txt           # Dependencias del proyecto
└── README.md                  # Este archivo
```

---

##  Proceso de Desarrollo

### 1 Preparación de Dataset
**Objetivo:** Recopilación y limpieza de datos históricos ambientales

**Actividades realizadas:**
- Extracción de datos de dispositivos IoT Skiliket
- Organización de datos por dispositivo en estructura jerárquica
- Limpieza y preprocesamiento de datos (notebooks en `extras/notebooks/devices_cleaning/`)
- Generación de tablas pivote para análisis temporal
- Creación de versiones minimizadas de datos para optimización

**Resultados:**
- Dataset estructurado por dispositivos
- Variables ambientales normalizadas
- Datos listos para entrenamiento del modelo

---

### 2 Selección y Entrenamiento de Modelo
**Objetivo:** Implementar un modelo de ML para predicciones ambientales

**Decisiones técnicas:**
- **Algoritmo seleccionado:** XGBoost (Extreme Gradient Boosting)
  - Razón: Excelente desempeño con datos tabulares
  - Capacidad para manejar relaciones no lineales
  - Robusto ante datos faltantes
  
- **División de datos:** 80/20 (Train/Test)
  - 80% para entrenamiento
  - 20% para validación

**Tipo de modelo:** Regresión/Series temporales (según el objetivo específico de predicción)

**Implementación:**
- Código principal en `src/model.py`
- Entrenamiento y evaluación documentados
- Guardado de modelo para inferencia

**Resultados del primer entrenamiento:**
- Modelo base funcional
- Métricas de evaluación registradas
- **Nota importante:** Los datos actuales presentan limitaciones de precisión que requieren mejoras

---

### 3 Sistema de Alertas
**Objetivo:** Implementar lógica para detección de tendencias negativas

**Componentes:**
- Sistema de alertas basado en umbrales
- Programación de recomendaciones automáticas
- Integración con el modelo predictivo

**Estado actual:**
- Lógica básica de alertas implementada
- Requiere calibración de umbrales con más datos

---

### 4 Dashboard de Predicciones
**Objetivo:** Visualización interactiva de predicciones en tiempo real

**Tecnología:** Streamlit

**Características implementadas:**
- Visualización de tendencias proyectadas
- Actualización en tiempo real (simulado)
- Interfaz intuitiva para usuarios no técnicos
- Documentación de cómo la IA apoya decisiones

**Acceso:** `streamlit run src/dashboard.py`

---

## Tecnologías Utilizadas

### Core ML/Data Science
- **XGBoost** - Modelo de gradient boosting
- **pandas** - Manipulación de datos
- **numpy** - Operaciones numéricas
- **scikit-learn** - Herramientas de ML (preprocessing, métricas)

### Visualización y Dashboard
- **Streamlit** - Framework para dashboard interactivo
- **matplotlib/seaborn** - Gráficos estáticos

### Otros
- **Python 3.x** - Lenguaje base
- Ver `requirements.txt` para dependencias completas

---

## Instalación y Uso

### Prerrequisitos
```bash
python 3.8+
pip
```

### Instalación

1. Clonar el repositorio:
```bash
git clone https://github.com/A01276594/Skiliket_Modelos_de_prediccion_con_IA.git
cd Skiliket_Modelos_de_prediccion_con_IA
```

2. Instalar dependencias:
```bash
pip install -r requirements.txt
```

### Ejecución

**Entrenar el modelo:**
```bash
python src/model.py
```

**Lanzar el dashboard:**
```bash
streamlit run src/dashboard.py
```

**Ejecutar pipeline completo:**
```bash
python src/main.py
```

---

## Limitaciones Actuales

### Calidad de Datos
- **Problema:** Los datos actuales presentan limitaciones de precisión
- **Impacto:** Las predicciones pueden no reflejar con exactitud patrones reales
- **Causa raíz:** 
  - Posible inconsistencia en la recopilación de datos de dispositivos
  - Insuficiente cantidad de datos históricos
  - Variabilidad en la calidad de sensores

### Precisión del Modelo
- Las métricas de evaluación sugieren necesidad de mejora
- El modelo base es funcional pero requiere optimización

---

## Próximos Pasos Recomendados

### Prioridad Alta: Mejora de Datos

1. **Auditoría de Calidad de Datos**
   - [ ] Analizar distribución de valores por variable
   - [ ] Identificar outliers y valores atípicos
   - [ ] Verificar consistencia temporal en las lecturas
   - [ ] Documentar patrones de datos faltantes

2. **Incremento de Dataset**
   - [ ] Recopilar más datos históricos (mínimo 6-12 meses)
   - [ ] Aumentar frecuencia de muestreo si es posible
   - [ ] Incorporar datos de más dispositivos para diversidad

3. **Validación de Sensores**
   - [ ] Verificar calibración de dispositivos Skiliket
   - [ ] Implementar controles de calidad en la recopilación
   - [ ] Establecer protocolos de mantenimiento preventivo

### Mejora del Modelo

4. **Feature Engineering**
   - [ ] Crear variables derivadas (promedios móviles, tendencias)
   - [ ] Incorporar variables temporales (hora del día, día de semana, estacionalidad)
   - [ ] Generar interacciones entre variables ambientales

5. **Optimización de Hiperparámetros**

   - [ ] Implementar búsqueda de hiperparámetros
   - [ ] Documentar configuración óptima encontrada

7. **Experimentación con Modelos Alternativos**
   - [ ] Probar LightGBM (alternativa a XGBoost)
   - [ ] Experimentar con Random Forest como baseline
   - [ ] Considerar modelos específicos para series temporales:
     - LSTM/GRU (redes neuronales recurrentes)
     - Prophet (Facebook)
     - ARIMA/SARIMA (modelos clásicos)
   - [ ] Implementar ensemble de modelos

### Evaluación y Métricas

7. **Sistema de Métricas Robusto**
   - [ ] Definir métricas de negocio (no solo técnicas)
   - [ ] Implementar backtesting en ventanas temporales
   - [ ] Crear sistema de monitoreo de drift de datos
   - [ ] Establecer benchmarks y objetivos claros

8. **Validación del Sistema de Alertas**
   - [ ] Calibrar umbrales con expertos del dominio
   - [ ] Medir tasa de falsos positivos/negativos
   - [ ] Implementar sistema de feedback de usuarios
   - [ ] Ajustar sensibilidad según criticidad

### Mejoras en el Dashboard

9. **Funcionalidades Adicionales**
   - [ ] Agregar intervalos de confianza a predicciones
   - [ ] Mostrar importancia de features
   - [ ] Implementar comparación histórico vs predicho
   - [ ] Agregar exportación de reportes (PDF/Excel)

10. **Experiencia de Usuario**
    - [ ] Agregar filtros por dispositivo y periodo
    - [ ] Incluir explicaciones interpretables (SHAP values)
    - [ ] Crear tutoriales interactivos
    - [ ] Implementar modo oscuro/claro

###  Documentación

11. **Documentación Técnica**
    - [ ] Documentar decisiones de arquitectura
    - [ ] Crear guía de contribución
    - [ ] Documentar API de modelos
    - [ ] Escribir casos de prueba

12. **Documentación de Usuario**
    - [ ] Manual de usuario del dashboard
    - [ ] Guía de interpretación de alertas
    - [ ] FAQs y troubleshooting
    - [ ] Videos demostrativos

---

## Contribución

**Áreas prioritarias para contribución:**
- Mejora de calidad de datos
- Optimización de modelos
- Nuevas visualizaciones en dashboard
- Tests unitarios
- Documentación

---

## 📄 Licencia

[Especificar licencia del proyecto]

---


**Versión:** 1.0.0  
**Última actualización:** Febrero 2026  
**Estado:** En desarrollo activo con limitaciones de datos conocidas


