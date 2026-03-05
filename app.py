import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import requests
from datetime import datetime, timedelta

# --- КОНФИГУРАЦИЯ СТРАНИЦЫ ---
st.set_page_config(page_title="ALGORITHM | Система Прогнозирования", layout="wide")

# Твой API KEY (Вставь свой ключ из Colab сюда)
API_KEY = "ТВОЙ_API_KEY_ИЗ_КОЛАБА" 
CITY = "Almaty"

# --- СТИЛИЗАЦИЯ (PREMIUM DARK UI) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700&display=swap');
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; background-color: #0F172A; color: #F8FAFC; }
    .stMetric { background: rgba(30, 41, 59, 0.7); border: 1px solid #334155; border-radius: 16px; padding: 20px; }
    .main { background: radial-gradient(circle at top right, #1e293b, #0f172a); }
    </style>
    """, unsafe_allow_html=True)

# --- ФУНКЦИЯ ПОЛУЧЕНИЯ РЕАЛЬНЫХ ДАННЫХ (ТВОЯ ЛОГИКА) ---
def get_weather_data():
    # Здесь используется твоя логика из Colab для запроса к API
    # Для примера создаем структуру, которую ты наполняешь своими вызовами:
    try:
        # url = f"http://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={API_KEY}&units=metric"
        # res = requests.get(url).json()
        return {
            "temp": 12, "wind": 1.2, "hum": 65, "press": 1020
        }
    except:
        return {"temp": 0, "wind": 0, "hum": 0, "press": 0}

weather = get_weather_data()

# --- ШАПКА САЙТА ---
st.markdown("# 🏔️ PROJECT A.L.G.O.R.I.T.H.M.")
st.markdown("### Ситуационный центр контроля воздушного бассейна Алматы")
st.write("---")

# --- ВКЛАДКИ ---
tab1, tab2, tab3 = st.tabs(["🛰️ ОПЕРАТИВНЫЙ ПРОГНОЗ", "💡 ИННОВАЦИИ И 3D", "📊 СТРАТЕГИЯ SROI"])

# --- ВКЛАДКА 1: МОНИТОРИНГ ---
with tab1:
    # 1. Метрики реального времени
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("PM2.5 (ТЕКУЩИЙ)", "148 µg/m³", "⚠ Опасно")
    with col2:
        st.metric("ВЕРОЯТНОСТЬ ИНВЕРСИИ", "92%", "КРИТИЧЕСКИ", delta_color="inverse")
    with col3:
        st.metric("СКОРОСТЬ ВЕТРА", f"{weather['wind']} м/с", "ШТИЛЬ")
    with col4:
        st.metric("ВЛАЖНОСТЬ", f"{weather['hum']}%", "ВЫСОКАЯ")

    st.write("##")

    # 2. Основная 3D Карта и AI Консоль
    c_map, c_ai = st.columns([2, 1])
    
    with c_map:
        st.subheader("📍 3D Рельеф Загрязнения (Алматы)")
        # Создаем реальный 3D рельеф через Mesh-сетку
        x = np.linspace(-5, 5, 50)
        y = np.linspace(-5, 5, 50)
        X, Y = np.meshgrid(x, y)
        Z = np.exp(-(X**2 + Y**2)/10) * 100 # Имитация концентрации в низине
        
        fig_3d = go.Figure(data=[go.Surface(z=Z, colorscale='Inferno', showscale=False)])
        fig_3d.update_layout(
            scene=dict(bgcolor='#0F172A', xaxis_title="Запад-Восток", yaxis_title="Север-Юг"),
            margin=dict(l=0, r=0, t=0, b=0), height=500, template="plotly_dark"
        )
        st.plotly_chart(fig_3d, use_container_width=True)

    with c_ai:
        st.info("### 🤖 Голос Искусственного Интеллекта")
        st.markdown(f"""
        **Анализ данных:**
        - Температура: **{weather['temp']}°C**
        - Давление: **{weather['press']} hPa**
        
        **Вердикт системы:**
        Температурный градиент отрицательный. Воздушные массы заблокированы в нижней части города. 
        Прогноз на 24 часа: **Ухудшение на 15%** из-за отсутствия ветра.
        """)
        st.warning("🎯 Рекомендация: Ввести ограничение на въезд транспорта Euro-3 в квадрат улиц Аль-Фараби - Саина.")

    # 3. Прогноз на 7 дней с детализацией по часам
    st.write("---")
    st.subheader("📅 Интерактивный прогноз на 7 дней (Почасовой)")
    
    days = [(datetime.now() + timedelta(days=i)).strftime("%d.%m") for i in range(7)]
    selected_day = st.select_slider("Перемещайте ползунок для выбора дня:", options=days)

    # Генерация данных прогноза (Тут работает твоя LSTM модель)
    hours = list(range(24))
    prediction = [40 + np.sin(h/4)*30 + 50 for h in hours] # Имитация работы твоей нейросети
    
    fig_line = go.Figure()
    fig_line.add_trace(go.Scatter(x=hours, y=prediction, fill='tozeroy', 
                                 line=dict(color='#00D4FF', width=3), name="Прогноз PM2.5"))
    fig_line.update_layout(
        title=f"Детальный анализ на {selected_day} (24 часа)",
        xaxis=dict(title="Часы суток", tickmode='linear'),
        yaxis=dict(title="µg/m³"),
        template="plotly_dark", height=350, margin=dict(l=20, r=20, t=40, b=20)
    )
    st.plotly_chart(fig_line, use_container_width=True)

# --- ОСТАЛЬНЫЕ ВКЛАДКИ (ЗАГЛУШКИ ДЛЯ ТВОЕГО ЗАПОЛНЕНИЯ) ---
with tab2:
    st.header("В разработке: 3D сравнение технологий...")
    st.write("Здесь будет твой блок с машинами и легкими.")

with tab3:
    st.header("В разработке: Экономическая стратегия...")
    st.write("Здесь будут расчеты SROI и налогов.")
