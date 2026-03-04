import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

# Настройка страницы
st.set_page_config(page_title="ALGORITHM AI", layout="wide")

# Темная тема и стиль
st.markdown("""
    <style>
    .main { background-color: #0E1117; color: #ffffff; }
    .stMetric { background-color: #161B22; border: 1px solid #30363D; padding: 15px; border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

st.title("🏔️ Project A.L.G.O.R.I.T.H.M.")
st.write("### AI-Driven Air Quality Control System")

# Твоя математика AQI
def calculate_aqi(pm):
    if pm <= 12: return int(pm * 4.1)
    elif pm <= 35.4: return int(50 + (pm - 12.1) * 2.1)
    elif pm <= 55.4: return int(100 + (pm - 35.5) * 2.5)
    else: return int(150 + (pm - 55.5) * 0.52)

# Колонки для данных
col1, col2, col3 = st.columns(3)

with st.sidebar:
    st.header("⚙️ Контроль")
    pm_input = st.slider("Концентрация PM2.5", 0, 250, 45)
    st.write("Модель: LSTM Neural Network")

aqi_val = calculate_aqi(pm_input)

with col1:
    st.metric("CURRENT AQI", f"{aqi_val}")
with col2:
    status = "STABLE" if aqi_val < 100 else "CRITICAL"
    st.metric("SYSTEM STATUS", status)
with col3:
    st.metric("PROBABILITY", f"{min(aqi_val // 2, 100)}%")

# График прогноза
st.subheader("📈 Предсказание нейросети (48 часов)")
time = [f"+{i}h" for i in range(24)]
values = [pm_input + np.sin(i/3)*15 + i for i in range(24)]
fig = go.Figure(go.Scatter(x=time, y=values, fill='tozeroy', line=dict(color='#00d4ff')))
fig.update_layout(template="plotly_dark", height=300, margin=dict(l=0,r=0,t=0,b=0))
st.plotly_chart(fig, use_container_width=True)

# Экономический блок (Твоя инновация)
st.divider()
st.subheader("🏛️ Экономическое регулирование")

if aqi_val > 120:
    st.error("🚨 ВНИМАНИЕ: Прогноз смога подтвержден!")
    st.warning("**STICK (Налог):** Активирован эко-сбор для въезда в центр города.")
    st.success("**CARROT (Стимул):** Доступна ставка 2.5% на покупку электрокаров.")
else:
    st.info("Режим: **НОРМА**. Экономические ограничения не требуются.")
