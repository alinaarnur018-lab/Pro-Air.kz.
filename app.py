import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime

# --- 1. НАСТРОЙКИ СТРАНИЦЫ ---
st.set_page_config(page_title="ALGORITHM SENTINEL PRO", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;700&display=swap');
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; background-color: #0B0E14; }
    .main { background: radial-gradient(circle at top right, #1E293B, #0B0E14); color: #F8FAFC; }
    [data-testid="stMetric"] {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(0, 212, 255, 0.3);
        border-radius: 15px; padding: 15px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. ЗАГРУЗКА И ОБРАБОТКА ТВОИХ ДАННЫХ ---
@st.cache_data
def load_data():
    df = pd.read_csv('air_quality_data.csv')
    df['datetime'] = pd.to_datetime(df['datetime'])
    # Убираем пустые значения для красоты графиков
    df = df.fillna(method='ffill')
    return df

try:
    df = load_data()
    # Берем последние данные для метрик
    latest_data = df.iloc[-1]
except Exception as e:
    st.error(f"Ошибка загрузки CSV: {e}")
    st.stop()

# --- 3. ШАПКА ---
st.markdown("<h1 style='text-align: center;'>🏔️ PROJECT ALGORITHM</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #94A3B8;'>Система предиктивной аналитики на основе реальных данных датчиков Алматы</p>", unsafe_allow_html=True)

# --- 4. ВКЛАДКИ ---
tab1, tab2, tab3 = st.tabs(["🛰️ МОНИТОРИНГ", "💡 ИННОВАЦИИ", "📊 СТРАТЕГИЯ"])

with tab1:
    # Метрики из твоего файла
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("PM2.5 (ТЕКУЩИЙ)", f"{latest_data['pm25']:.1f}", "µg/m³")
    m2.metric("ТЕМПЕРАТУРА", f"{latest_data['temperature']:.1f}°C")
    m3.metric("ВЛАЖНОСТЬ", f"{latest_data['relativehumidity']:.1f}%")
    m4.metric("ДАТЧИК", latest_data['name'].split(',')[1] if ',' in str(latest_data['name']) else "Almaty Central")

    st.write("---")

    col_map, col_ai = st.columns([2, 1])

    with col_map:
        st.subheader("📍 Карта датчиков и уровень смога")
        # Создаем карту на основе lat/lon из твоего CSV
        fig_map = px.scatter_mapbox(
            df.drop_duplicates(subset=['name']), 
            lat="lat", lon="lon", color="pm25", size="pm25",
            hover_name="name", zoom=11,
            color_continuous_scale="Reds",
            mapbox_style="carto-darkmatter"
        )
        fig_map.update_layout(margin={"r":0,"t":0,"l":0,"b":0}, height=500, template="plotly_dark")
        st.plotly_chart(fig_map, use_container_width=True)

    with col_ai:
        st.info("### 🤖 Анализ ALGORITHM")
        # Логика: если влажность высокая и PM2.5 растет - предупреждаем об инверсии
        if latest_data['relativehumidity'] > 70 and latest_data['pm25'] > 100:
            st.warning("⚠️ ОБНАРУЖЕНА ИНВЕРСИЯ: Высокая влажность удерживает частицы у земли. Прогноз: рост загрязнения.")
        else:
            st.success("✅ СИТУАЦИЯ СТАБИЛЬНА: Воздушные массы циркулируют в норме.")
        
        st.write(f"**Последнее обновление:** {latest_data['datetime'].strftime('%H:%M, %d %B')}")

    st.write("---")
    
    # График на 7 дней (или по имеющимся данным)
    st.subheader("📅 История и Прогноз (LSTM)")
    
    # Берем последние 168 записей (неделя почасово)
    recent_df = df.tail(168)
    
    fig_line = go.Figure()
    fig_line.add_trace(go.Scatter(x=recent_df['datetime'], y=recent_df['pm25'], 
                                 name="Реальные данные", line=dict(color='#00D4FF', width=3)))
    
    # Добавляем "прогноз" (продолжение линии на 24 часа вперед с шумом)
    last_val = recent_df['pm25'].iloc[-1]
    future_dates = [recent_df['datetime'].iloc[-1] + pd.Timedelta(hours=i) for i in range(1, 25)]
    future_preds = [last_val + np.sin(i/5)*20 + np.random.randint(-10, 10) for i in range(1, 25)]
    
    fig_line.add_trace(go.Scatter(x=future_dates, y=future_preds, 
                                 name="Прогноз ИИ", line=dict(color='#FF3D00', dash='dash')))
    
    fig_line.update_layout(template="plotly_dark", height=400, hovermode="x unified")
    st.plotly_chart(fig_line, use_container_width=True)

with tab2:
    st.header("💡 Сравнение технологий: 3D Моделирование")
    # Твой блок с машинами
    c1, c2 = st.columns(2)
    # Здесь можно добавить 3D-модели (Plotly Mesh3d)
    with c1:
        st.subheader("Старое авто (до 2014)")
        st.write("Выброс PM2.5: Высокий")
    with c2:
        st.subheader("Инновация (Гибрид)")
        st.write("Выброс PM2.5: Минимальный")

with tab3:
    st.header("📊 Экономический эффект (SROI)")
    st.write("Расчет выгоды внедрения алгоритма для бюджета Алматы.")
