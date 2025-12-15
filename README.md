# 🦟 Sistema Inteligente de Predicción y Alerta Temprana de Brotes de Dengue

## 📌 Descripción del Proyecto

Este proyecto implementa un **sistema sociotécnico inteligente** para la **predicción y alerta temprana de brotes de dengue en el Perú**, utilizando técnicas de **Machine Learning**, **análisis de series temporales** y **visualización geoespacial**.

El sistema permite anticipar el comportamiento de los casos de dengue con **2 a 4 semanas de anticipación**, apoyando la **toma de decisiones preventivas** por parte de autoridades del sector salud.

El desarrollo se realizó como **Trabajo Final del curso Taller de Ingeniería de sistemas**:

> *Uso de Tecnologías Emergentes en la Construcción de Sistemas Sociotécnicos*

---

## 🎯 Objetivo General

Desarrollar e implementar un sistema inteligente basado en Machine Learning y análisis geoespacial que permita predecir brotes de dengue a nivel departamental, generando alertas epidemiológicas tempranas para la intervención oportuna.

---

## ⚙️ Tecnologías Utilizadas

* **Python 3.10+**
* **Streamlit** (visualización y despliegue web)
* **Pandas / NumPy** (procesamiento de datos)
* **Matplotlib** (visualización)
* **Prophet** (modelado de series temporales)
* **Scikit-learn** (soporte analítico)
* **GitHub + Streamlit Cloud** (despliegue gratuito)

---

## 🗂️ Estructura del Proyecto

```text
Sistema_Prediccion_Dengue/
│
├── app.py                         # Aplicación principal Streamlit
├── requirements.txt               # Dependencias del proyecto
├── README.md                      # Documentación
├── .gitignore                     # Archivos ignorados por Git
│
├── data/
│   └── processed/
│       └── dengue_departamental_semanal_con_fecha.csv
│
└── notebooks/ (ignorado en Git)
```

---

## 📊 Fuente de Datos

* **MINSA – Perú**
  Dataset de notificación semanal de casos de dengue por departamento (2018–2023).

Los datos fueron:

* Limpiados
* Agregados por semana epidemiológica
* Transformados a series temporales

---

## 🧠 Funcionamiento del Sistema

1. **Carga de datos epidemiológicos**
2. **Selección del departamento** por el usuario
3. **Entrenamiento automático del modelo Prophet**
4. **Predicción de casos futuros (4 semanas)**
5. **Comparación con promedio histórico reciente**
6. **Clasificación del nivel de alerta epidemiológica**
7. **Visualización interactiva y recomendación automática**

---

## 🚨 Niveles de Alerta

| Nivel   | Condición                | Recomendación             |
| ------- | ------------------------ | ------------------------- |
| BAJO    | Predicción < promedio    | Monitoreo rutinario       |
| MEDIO   | Leve incremento          | Vigilancia reforzada      |
| ALTO    | Incremento significativo | Activar control vectorial |
| CRÍTICO | Brote severo             | Emergencia sanitaria      |

---

## 🌐 Despliegue

El sistema se encuentra desplegado gratuitamente en **Streamlit Cloud**, permitiendo el acceso desde cualquier dispositivo con conexión a internet.

---

## 📈 Alcances y Limitaciones

### Alcances

* Predicción a nivel departamental
* Sistema funcional 24/7
* Uso de tecnologías emergentes

### Limitaciones

* No incluye aún variables climáticas
* No es un sistema oficial del MINSA
* Uso académico

---

## 📌 Trabajo Futuro

* Integración de datos climáticos (SENAMHI)
* Incorporación de mapas geoespaciales
* Uso de modelos ensemble (XGBoost)
* Sistema multi-enfermedad

---

## 👨‍💻 Autor

**Franklin Campos guillen**

Estudiante de Ingeniería de Sistemas - UNSCH
Perú 🇵🇪

---

> Proyecto académico con fines educativos. No sustituye sistemas oficiales de vigilancia epidemiológica.
