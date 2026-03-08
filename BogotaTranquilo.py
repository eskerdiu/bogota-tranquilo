import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
import random

st.set_page_config(page_title="Bogotá Tranquilo", layout="wide", page_icon="🚍")

st.title("Bogotá Tranquilo 🌿")
st.markdown("**Reduce estrés y ahorra tiempo en el tráfico bogotano.** App para estudiantes, trabajadores y familias: alertas, tips y tracking personal.")

# --- Sección 1: Calculadora de viaje ---
st.header("1. Calcula tu viaje hoy")
col1, col2 = st.columns(2)
with col1:
    origen = st.selectbox("Origen", ["Norte (Suba/Usaquén)", "Sur (Bosa/Kennedy)", "Occidente (Fontibón/Engativá)", "Centro (Chapinero/Santa Fe)", "Universidad o Trabajo"])
with col2:
    destino = st.selectbox("Destino", ["Universidad", "Trabajo Centro", "Casa Norte", "Casa Sur", "Aeropuerto El Dorado", "Otro"])
hora_salida = st.slider("Hora de salida (formato 24h)", 5, 22, 7)
minutos_base = 45 + random.randint(-10, 20)  # Variación realista

# Reglas pico Bogotá
if (6 <= hora_salida <= 9) or (16 <= hora_salida <= 19):
    minutos_extra = random.randint(40, 70)
    alerta = "¡Hora pico alta! Sal 15-25 min antes para evitar estrés."
elif (5 <= hora_salida <= 6) or (19 <= hora_salida <= 20):
    minutos_extra = random.randint(20, 40)
    alerta = "Tráfico moderado-alto – considera ruta alternativa."
else:
    minutos_extra = random.randint(0, 20)
    alerta = "Buen horario, tráfico bajo."

tiempo_total = minutos_base + minutos_extra
st.metric("Tiempo estimado en trancones", f"{tiempo_total} minutos", delta=f"+{minutos_extra} min por tráfico")
st.info(alerta)

# --- Sección 2: Consejos anti-estrés ---
st.header("2. Tips rápidos para calmarte en el camino")
tips = [
    "Respira 4-7-8: inhala 4 seg, retiene 7 seg, exhala 8 seg (reduce ansiedad en minutos).",
    "Pon música relajante o podcast (busca 'lo-fi Bogotá' o meditaciones guiadas en Spotify/YouTube).",
    "Si vas en TransMilenio o SITP, lee o escucha algo positivo para distraerte.",
    "Sal 10-20 min antes: evita la prisa y llega más tranquilo.",
    "Bebe agua y estira el cuello cada 15 min si estás manejando.",
    "Visualiza tu llegada relajado – cambia el enfoque mental."
]
st.success(random.choice(tips))

# --- Sección 3: Registro y progreso de estrés ---
st.header("3. Trackea tu estrés diario")
if 'stress_log' not in st.session_state:
    st.session_state.stress_log = pd.DataFrame(columns=["Fecha", "Estrés (1-10)", "Notas", "Tráfico percibido"])

fecha_hoy = datetime.now().date()
estres_hoy = st.slider("Nivel de estrés hoy por tráfico (1 = tranquilo, 10 = muy estresado)", 1, 10, 4)
trafico_hoy = st.select_slider("Tráfico percibido hoy", ["Bajo", "Moderado", "Alto", "Muy alto"])
notas_hoy = st.text_input("Notas (ej. 'Trancón eterno en Calle 80')")

if st.button("Guardar registro de hoy"):
    nuevo_reg = pd.DataFrame({
        "Fecha": [fecha_hoy],
        "Estrés (1-10)": [estres_hoy],
        "Notas": [notas_hoy],
        "Tráfico percibido": [trafico_hoy]
    })
    st.session_state.stress_log = pd.concat([st.session_state.stress_log, nuevo_reg], ignore_index=True)
    st.success("¡Registrado! Sigue usándolo para ver cómo mejoras.")

if not st.session_state.stress_log.empty:
    df_log = st.session_state.stress_log.sort_values("Fecha")
    fig = px.line(df_log, x="Fecha", y="Estrés (1-10)", markers=True, title="Tu progreso de estrés semanal/mensual")
    fig.update_traces(line_color='#00CC96')
    st.plotly_chart(fig)

    prom_estres = df_log["Estrés (1-10)"].mean()
    st.metric("Promedio de estrés", f"{prom_estres:.1f}/10", 
              delta=f"↓ Mejora" if prom_estres < 5 else f"↑ Sube un poco", 
              delta_color="normal")

st.markdown("**Dato real 2025**: En Bogotá perdemos **153 horas al año** en trancones (TomTom Traffic Index), y el **57%** de conductores sienten estrés diario (U. Manuela Beltrán). ¡Esta app te ayuda a combatirlo! 😌")

st.caption("Proyecto universitario - Primer corte. Hecho con Python + Streamlit.")
