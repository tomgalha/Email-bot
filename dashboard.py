import streamlit as st
import threading
import pandas as pd
from main import run_bot
from database import cargar_datos, guardar_datos

st.set_page_config(page_title="Control de Bot IMAP", layout="centered")

if 'config' not in st.session_state:
    st.session_state.config = cargar_datos()

if 'logs' not in st.session_state:
    st.session_state.logs = []

# --- INTERFAZ DE STREAMLIT ---
st.title("🤖 Panel de Control: Bot mails")

st.sidebar.header("Estado del Sistema")
status_placeholder = st.sidebar.empty()
if st.session_state.config["ejecutando"]:
    status_placeholder.success("Bot en línea")
else:
    status_placeholder.warning("Bot detenido")

with st.sidebar:
    st.divider()
    st.subheader("📜 Registro de Actividad (Log)")

    if st.session_state.logs:
        log_texto = '\n'.join(st.session_state.logs)
        st.text_area("Eventos recientes", value=log_texto, height=300, disabled=True)
    else:
        st.info("No hay actividad registrada aun.")

# Métricas principales
col1, col2,col3 = st.columns(3)
col1.metric("Trabajos Hoy", st.session_state.config["aceptados_hoy"])
col2.metric("Límite Diario de trabajos ", st.session_state.config["limite_trabajos"])
col3.metric("Cantidad palabras maximas ", st.session_state.config["limite_palabras"])

st.divider()

# Controles de Configuración
st.subheader("Configuración de Reglas")
nuevo_limite_trabajos = st.number_input("Cantidad máxima de trabajos:", min_value=1, value=st.session_state.config["limite_trabajos"])
nuevo_limite_palabras = st.number_input("Cantidad maxima de palabras", min_value=50, value=st.session_state.config["limite_palabras"])
rango = st.slider("Rango horario de actividad:", 0, 23, (st.session_state.config["inicio"], st.session_state.config["fin"]))

if st.button("Actualizar y Guardar"):
    st.session_state.config["limite_trabajos"] = nuevo_limite_trabajos
    st.session_state.config["limite_palabras"] = nuevo_limite_palabras
    st.session_state.config["inicio"] = rango[0]
    st.session_state.config["fin"] = rango[1]
    guardar_datos(st.session_state.config)
    st.success("Configuración actualizada correctamente.")
    st.rerun()

# Botón para arrancar el bot (solo una vez)
if not st.session_state.config["ejecutando"]:
    if st.button("🚀 Arrancar Bot"):
        st.session_state.config["ejecutando"] = True
        # Pasamos el diccionario por referencia para que el hilo vea los cambios
        t = threading.Thread(target=run_bot, args=(st.session_state.config,st.session_state.logs), daemon=True)
        t.start()
        st.rerun()


st.divider()
if st.button("🔄 Refrescar Pantalla"):
    st.rerun()