import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
import random
import folium
from streamlit_folium import st_folium

# Configuración de la página (diseño pro)
st.set_page_config(
    page_title="Bogotá Tranquilo 3.0",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Sidebar lateral
with st.sidebar:
    st.title("Bogotá Tranquilo 🌿")
    st.markdown("Reduce estrés por tráfico en Bogotá")
    st.markdown("**Proyecto universitario – Versión 3.0**")
    st.info("¡Registra tu estrés diario y ve cómo mejoras!")
    st.markdown("---")
    st.markdown("**Demo online:** esta página")
    st.markdown("**Repo GitHub:** [github.com/eskerdiu/bogota-tranquilo](https://github.com/eskerdiu/bogota-tranquilo)")
    st.caption("Hecho con Python + Streamlit + Folium + Plotly")
    st.caption("Daniel – Bogotá, 2026")

# Mensaje de bienvenida / intro
st.title("Bogotá Tranquilo 3.0 🌿")
st.success("""
¡Bienvenido! Esta app te ayuda a reducir el estrés por tráfico en Bogotá.  
Calcula tu tiempo de viaje, recibe alertas de hora pico, tips para calmarte y trackea tu estrés diario.  
¡Prueba registrando tu día y ve tu progreso! 😌
""")
st.markdown("---")

# Sección 1: Calcula tu viaje hoy
st.header("1. Calcula tu viaje hoy")
col1, col2 = st.columns(2)
with col1:
    origen = st.selectbox("Origen", ["Norte (Suba/Usaquén)", "Sur (Bosa/Kennedy)", "Occidente (Fontibón/Engativá)", "Centro (Chapinero/Santa Fe)", "Universidad o Trabajo"])
with col2:
    destino = st.selectbox("Destino", ["Universidad", "Trabajo Centro", "Casa Norte", "Casa Sur", "Aeropuerto El Dorado", "Otro"])

hora_salida = st.slider("Hora de salida (formato 24h)", 5, 22, 7)
minutos_base = 45 + random.randint(-10, 20)

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
st.metric("Tiempo estimado en trancones", f"{tiempo_total} minutos", delta=f"+{minutos_extra} min por tráfico", delta_color="inverse" if minutos_extra > 40 else "normal")
st.info(alerta)

# Mapa interactivo
st.subheader("Mapa aproximado de tu ruta")
ubicaciones = {
    "Norte (Suba/Usaquén)": [4.75, -74.05],
    "Sur (Bosa/Kennedy)": [4.55, -74.12],
    "Occidente (Fontibón/Engativá)": [4.68, -74.13],
    "Centro (Chapinero/Santa Fe)": [4.61, -74.07],
    "Universidad o Trabajo": [4.60, -74.07],
    "Trabajo Centro": [4.61, -74.07],
    "Casa Norte": [4.75, -74.05],
    "Casa Sur": [4.55, -74.12],
    "Aeropuerto El Dorado": [4.70, -74.13],
    "Otro": [4.61, -74.07]
}

coord_origen = ubicaciones.get(origen, [4.61, -74.07])
coord_destino = ubicaciones.get(destino, [4.61, -74.07])

m = folium.Map(location=[(coord_origen[0] + coord_destino[0])/2, (coord_origen[1] + coord_destino[1])/2], zoom_start=12, tiles="OpenStreetMap")
folium.Marker(coord_origen, popup=f"Origen: {origen}", icon=folium.Icon(color="green", icon="home")).add_to(m)
folium.Marker(coord_destino, popup=f"Destino: {destino}", icon=folium.Icon(color="red", icon="flag")).add_to(m)
folium.PolyLine([coord_origen, coord_destino], color="blue", weight=5, opacity=0.7).add_to(m)

st_folium(m, width=700, height=400)

# Sección 2: Tips
st.header("2. Tips rápidos para calmarte en el camino")
tips = [
    "Respira 4-7-8: inhala 4 seg, retiene 7 seg, exhala 8 seg (reduce ansiedad rápido).",
    "Escucha playlist relajante: [Lo-fi beats en Spotify](https://open.spotify.com/playlist/37i9dQZF1DX8Uebhn9wzrS)",
    "Meditación guiada de 5 min: [YouTube – Calma rápida](https://www.youtube.com/watch?v=1zyq8PSzRBw)",
    "Si vas en TransMilenio, lee o escucha podcast positivo.",
    "Sal 10-20 min antes: evita la prisa y llega más tranquilo.",
    "Bebe agua y estira el cuello cada 15 min si estás manejando.",
    "Visualiza tu llegada relajado – cambia el enfoque mental."
]
st.success(random.choice(tips))

# Sección 3: Trackeo
st.header("3. Trackea tu estrés diario")
if 'stress_log' not in st.session_state:
    st.session_state.stress_log = pd.DataFrame(columns=["Fecha", "Estrés (1-10)", "Notas", "Tráfico percibido"])

fecha_hoy = datetime.now().date()
estres_hoy = st.slider("Nivel de estrés hoy por tráfico (1 = tranquilo, 10 = muy estresado)", 1, 10, 4)
trafico_hoy = st.select_slider("Tráfico percibido hoy", ["Bajo", "Moderado", "Alto", "Muy alto"])
notas_hoy = st.text_input("Notas (ej. 'Trancón eterno en Calle 80')")

col_btn1, col_btn2 = st.columns(2)
with col_btn1:
    if st.button("Guardar registro de hoy", type="primary"):
        nuevo_reg = pd.DataFrame({
            "Fecha": [fecha_hoy],
            "Estrés (1-10)": [estres_hoy],
            "Notas": [notas_hoy],
            "Tráfico percibido": [trafico_hoy]
        })
        st.session_state.stress_log = pd.concat([st.session_state.stress_log, nuevo_reg], ignore_index=True)
        st.success("¡Registrado! Sigue trackeando para ver mejoras.")

with col_btn2:
    if st.button("Limpiar mis registros", type="secondary"):
        st.session_state.stress_log = pd.DataFrame(columns=["Fecha", "Estrés (1-10)", "Notas", "Tráfico percibido"])
        st.success("Registros limpiados. ¡Empieza de nuevo!")

if not st.session_state.stress_log.empty:
    df_log = st.session_state.stress_log.sort_values("Fecha")
    fig = px.line(df_log, x="Fecha", y="Estrés (1-10)", markers=True, title="Tu progreso de estrés semanal/mensual")
    fig.update_traces(line_color='#00CC96', marker=dict(size=10))
    st.plotly_chart(fig, use_container_width=True)

    prom_estres = df_log["Estrés (1-10)"].mean()
    st.metric("Promedio de estrés", f"{prom_estres:.1f}/10", 
              delta=f"↓ Mejora" if prom_estres < 5 else f"↑ Sube un poco", 
              delta_color="normal")

# Footer
st.markdown("---")
st.caption("**Dato real 2025**: En Bogotá perdemos **153 horas al año** en trancones (TomTom Traffic Index), y el **57%** de conductores sienten estrés diario (U. Manuela Beltrán). ¡Esta app te ayuda a combatirlo! 😌")
st.caption("Proyecto universitario – Primer corte. Hecho con Python + Streamlit + Folium + Plotly. Versión 3.0 – Daniel 2026")
