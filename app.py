# ============================================================
# SISTEMA INTELIGENTE DE ALERTA TEMPRANA DE DENGUE
# Curso: Uso de Tecnologías Emergentes en Sistemas Sociotécnicos
# ============================================================

# ---------------------------
# 1. IMPORTACIÓN DE LIBRERÍAS
# ---------------------------

import streamlit as st              # Framework para aplicaciones web
import pandas as pd                 # Manipulación y análisis de datos
import matplotlib.pyplot as plt     # Visualización de datos
from prophet import Prophet         # Modelo de predicción de series temporales
import warnings

warnings.filterwarnings("ignore")  # Oculta mensajes no críticos


# --------------------------------
# 2. CONFIGURACIÓN GENERAL DE LA APP
# --------------------------------

# Define el título, ícono y ancho de la aplicación web
st.set_page_config(
    page_title="Sistema de Alerta Temprana de Dengue",
    page_icon="🦟",
    layout="wide"
)


# -----------------------
# 3. CARGA DEL DATASET
# -----------------------

@st.cache_data
def cargar_datos():
    """
    Carga el dataset final de dengue con fechas semanales.
    El uso de cache mejora el rendimiento de la aplicación.
    """
    df = pd.read_csv("dengue_departamental_semanal_con_fecha.csv")
    df["fecha"] = pd.to_datetime(df["fecha"])  # Conversión a formato fecha
    return df


# Ejecuta la función y guarda los datos en memoria
df = cargar_datos()


# -----------------------------------------
# 4. TÍTULO Y DESCRIPCIÓN DEL SISTEMA
# -----------------------------------------

st.title("🦟 Sistema Inteligente de Alerta Temprana de Dengue")

st.markdown("""
**Curso:** Uso de Tecnologías Emergentes en la Construcción de Sistemas Sociotécnicos  
**Tecnologías:** Machine Learning · Series Temporales · Streamlit  
**Fuente de datos:** Ministerio de Salud del Perú (MINSA)

El sistema permite **analizar datos históricos**, **predecir casos futuros**
y **emitir alertas epidemiológicas tempranas** a nivel departamental.
""")


# --------------------------------
# 5. PANEL LATERAL DE CONTROL
# --------------------------------

st.sidebar.header("⚙️ Panel de Control")

# Selector interactivo de departamento
departamento = st.sidebar.selectbox(
    "Seleccione el departamento",
    sorted(df["departamento"].unique())
)


# -----------------------------------------
# 6. PREPARACIÓN DE DATOS PARA EL MODELO
# -----------------------------------------

# Filtra los datos solo para el departamento seleccionado
df_dep = df[df["departamento"] == departamento].copy()

# Prophet requiere:
# ds -> fecha
# y  -> variable a predecir
df_prophet = df_dep.rename(
    columns={"fecha": "ds", "casos_dengue": "y"}
)[["ds", "y"]]


# -------------------------------
# 7. ENTRENAMIENTO DEL MODELO
# -------------------------------

# Se instancia el modelo Prophet con estacionalidad semanal y anual
modelo = Prophet(
    yearly_seasonality=True,
    weekly_seasonality=True,
    daily_seasonality=False
)

# Se entrena el modelo con los datos históricos
modelo.fit(df_prophet)


# -------------------------------
# 8. GENERACIÓN DE PREDICCIONES
# -------------------------------

# Se generan 4 semanas futuras (horizonte de predicción)
future = modelo.make_future_dataframe(periods=4, freq="W")

# Se calculan las predicciones
forecast = modelo.predict(future)


# -----------------------------------------
# 9. CÁLCULO DE INDICADORES EPIDEMIOLÓGICOS
# -----------------------------------------

# Promedio de casos reales en las últimas 12 semanas
promedio_reciente = df_prophet["y"].tail(12).mean()

# Promedio de los valores predichos para las próximas 4 semanas
prediccion_futura = forecast.tail(4)["yhat"].mean()


# -------------------------------
# 10. CLASIFICACIÓN DEL NIVEL DE ALERTA
# -------------------------------

# Se compara la predicción futura con el comportamiento reciente
if prediccion_futura < promedio_reciente * 1.1:
    nivel_alerta = "BAJO"
    recomendacion = "Monitoreo rutinario."
elif prediccion_futura < promedio_reciente * 1.3:
    nivel_alerta = "MEDIO"
    recomendacion = "Reforzar vigilancia epidemiológica."
elif prediccion_futura < promedio_reciente * 1.6:
    nivel_alerta = "ALTO"
    recomendacion = "Activar brigadas de control vectorial."
else:
    nivel_alerta = "CRÍTICO"
    recomendacion = "Declarar emergencia sanitaria y control intensivo."


# --------------------------------
# 11. VISUALIZACIÓN DE MÉTRICAS
# --------------------------------

st.subheader("📊 Indicadores Epidemiológicos")

# Se crean dos columnas para mostrar métricas clave
col1, col2 = st.columns(2)

col1.metric(
    "Promedio reciente (12 semanas)",
    f"{promedio_reciente:.2f} casos"
)

col2.metric(
    "Predicción próxima (4 semanas)",
    f"{prediccion_futura:.2f} casos"
)


# --------------------------------
# 12. MENSAJE DE ALERTA EPIDEMIOLÓGICA
# --------------------------------

st.subheader("🚨 Nivel de Alerta Epidemiológica")
st.markdown(f"**Departamento:** {departamento}")

# El color del mensaje depende del nivel de alerta
if nivel_alerta == "BAJO":
    st.success(f"🟢 **Nivel BAJO**\n\n{recomendacion}")
elif nivel_alerta == "MEDIO":
    st.warning(f"🟡 **Nivel MEDIO**\n\n{recomendacion}")
elif nivel_alerta == "ALTO":
    st.error(f"🟠 **Nivel ALTO**\n\n{recomendacion}")
else:
    st.error(f"🔴 **Nivel CRÍTICO**\n\n{recomendacion}")


# --------------------------------
# 13. GRÁFICO DE EVOLUCIÓN Y PREDICCIÓN
# --------------------------------

st.subheader("📈 Evolución y predicción semanal de casos de dengue")

fig, ax = plt.subplots(figsize=(13, 5))

# Línea negra: casos reales observados
ax.plot(
    df_prophet["ds"],
    df_prophet["y"],
    color="black",
    label="Casos reales"
)

# Línea azul discontinua: predicción del modelo
ax.plot(
    forecast["ds"],
    forecast["yhat"],
    linestyle="--",
    label="Predicción (Prophet)"
)

# Área celeste: intervalo de incertidumbre
ax.fill_between(
    forecast["ds"],
    forecast["yhat_lower"],
    forecast["yhat_upper"],
    alpha=0.25,
    label="Intervalo de confianza"
)

# Línea vertical roja: inicio de la predicción
fecha_inicio_pred = df_prophet["ds"].max()
ax.axvline(
    x=fecha_inicio_pred,
    color="darkred",     # Color distinto para evitar confusión
    linestyle=":",
    linewidth=2,
    label="Inicio de predicción"
)

ax.set_xlabel("Año")
ax.set_ylabel("Casos de dengue")
ax.legend()
ax.grid(True)

st.pyplot(fig)


# --------------------------------
# 14. EXPLICACIÓN DEL GRÁFICO
# --------------------------------

with st.expander("📘 Interpretación del gráfico"):
    st.markdown("""
    - **Línea negra:** casos reales reportados por el MINSA.
    - **Línea azul discontinua:** predicción generada por el modelo.
    - **Área sombreada:** rango de incertidumbre de la predicción.
    - **Línea roja vertical:** separación entre datos históricos y predicción futura.
    """)


# --------------------------------
# 15. PIE DE PÁGINA
# --------------------------------

st.markdown("---")
st.markdown("📍 *Proyecto académico – Ingeniería de Sistemas – 2025*")
