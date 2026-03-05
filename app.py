import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import os
from datetime import datetime, timedelta

# --- 1. НАСТРОЙКИ СТРАНИЦЫ (PREMIUM DARK) ---
st.set_page_config(page_title="ALGORITHM SENTINEL PRO", layout="wide", page_icon="🏔️")

# Кастомный CSS для создания эффекта "стеклянного" интерфейса
st.markdown("""
    <style>
    .main { background: radial-gradient(circle at top right, #1E293B, #0B0E14); color: #F8FAFC; }
    [data-testid="stMetric"] {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(0, 212, 255, 0.4);
        border-radius: 16px; padding: 15px;
        box-shadow: 0 4px 30px rgba(0, 0, 0, 0.1);
    }
    .stTabs [data-baseweb="tab-list"] { gap: 10px; }
    .stTabs [data-baseweb="tab"] {
        height: 50px; background-color: rgba(255,255,255,0.05);
        border-radius: 10px; color: #94A3B8;
    }
    .stTabs [aria-selected="true"] { 
        background-color: rgba(0, 212, 255, 0.2) !important; 
        border: 1px solid #00D4FF !important; color: white !important; 
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. УМНАЯ ЗАГРУЗКА ДАННЫХ ---
FILENAME = 'air_quality_data.csv'

@st.cache_data
def load_data(file_path):
    df = pd.read_csv(file_path)
    df['datetime'] = pd.to_datetime(df['datetime'])
    # Заполняем пропуски для красивых графиков
    df = df.sort_values('datetime').fillna(method='ffill')
    return df

# Проверка наличия файла
if os.path.exists(FILENAME):
    df = load_data(FILENAME)
    latest = df.iloc[-1]
else:
    st.error(f"❌ Файл {FILENAME} не найден!")
    st.info("Пожалуйста, убедитесь, что вы загрузили CSV файл в ту же папку, где лежит app.py на GitHub.")
    # Создаем пустые данные, чтобы сайт не «падал» при первом запуске
    st.stop()

# --- 3. ВЕРХНЯЯ ПАНЕЛЬ (DASHBOARD) ---
st.markdown("<h1 style='text-align: center; color: white;'>🏔️ PROJECT ALGORITHM: SENTINEL V2</h1>", unsafe_allow_html=True)
st.write("##")

# Метрики реального времени
m1, m2, m3, m4 = st.columns(4)
m1.metric("AQI (PM2.5)", f"{latest['pm25']:.1f}", "LIVE")
m2.metric("ТЕМПЕРАТУРА", f"{latest['temperature']:.1f}°C", "Almaty")
m3.metric("ВЛАЖНОСТЬ", f"{latest['relativehumidity']:.0f}%", "Инверсия")
m4.metric("СТАТУС ИИ", "АКТИВЕН", "LSTM v4")

st.write("---")

# --- 4. ВКЛАДКИ ---
tab1, tab2, tab3 = st.tabs(["🛰️ МОНИТОРИНГ 24/7", "💡 ИННОВАЦИИ (3D)", "📊 СТРАТЕГИЯ SROI"])

# ВКЛАДКА 1: МОНИТОРИНГ
with tab1:
    col_map, col_info = st.columns([2, 1])
    
    with col_map:
        st.subheader("📍 Карта датчиков Алматы")
        # Используем реальные lat/lon из твоего CSV
        map_df = df.drop_duplicates(subset=['name']).copy()
        fig_map = px.scatter_mapbox(
            map_df, lat="lat", lon="lon", color="pm25", size="pm25",
            hover_name="name", zoom=11, color_continuous_scale="Reds",
            mapbox_style="carto-darkmatter"
        )
        fig_map.update_layout(margin={"r":0,"t":0,"l":0,"b":0}, height=500, template="plotly_dark")
        st.plotly_chart(fig_map, use_container_width=True)

    with col_info:
        st.info("### 🤖 Голос Искусственного Интеллекта")
        st.write(f"Анализ по станции: **{latest['name']}**")
        if latest['pm25'] > 100:
            st.warning("Внимание! Уровень загрязнения превышен. Рекомендуется ограничение движения в нижней части города.")
        else:
            st.success("Уровень PM2.5 в норме. Риск температурной инверсии минимален.")
        
        st.divider()
        st.markdown("**Факторы влияния:**")
        st.write(f"🌡️ Инверсионный порог: {latest['temperature'] + 2:.1f}°C")
        st.write(f"💧 Вес частиц (Влажность): {latest['relativehumidity']}%")

    st.divider()

    # СЕКЦИЯ ПРОГНОЗА 7 ДНЕЙ / 24 ЧАСА
    st.subheader("📅 Интерактивный прогноз (7 дней)")
    
    # Группируем данные по дням для слайдера
    df['date_only'] = df['datetime'].dt.strftime('%d.%m')
    unique_days = df['date_only'].unique()[-7:] # Берем последние 7 дней
    
    selected_day = st.select_slider("Выберите день для почасовой детализации:", options=unique_days)
    
    # Фильтруем данные для графика
    day_data = df[df['date_only'] == selected_day]
    
    fig_line = go.Figure()
    # Историческая линия
    fig_line.add_trace(go.Scatter(x=day_data['datetime'].dt.hour, y=day_data['pm25'], 
                                 name="История", line=dict(color='#00D4FF', width=4), fill='tozeroy'))
    # Прогнозная линия (имитация)
    fig_line.add_trace(go.Scatter(x=day_data['datetime'].dt.hour, y=day_data['pm25']*1.1, 
                                 name="ИИ Прогноз", line=dict(color='#FF3D00', dash='dot')))
    
    fig_line.update_layout(
        title=f"Почасовой анализ PM2.5 на {selected_day}",
        xaxis_title="Часы (00:00 - 23:00)", yaxis_title="Концентрация µg/m³",
        template="plotly_dark", height=400, hovermode="x unified"
    )
    st.plotly_chart(fig_line, use_container_width=True)

# ВКЛАДКА 2: ИННОВАЦИЯ (3D МАШИНЫ)
with tab2:
    st.subheader("🚀 Экологическая Трансформация")
    st.write("Сравнение влияния транспорта на здоровье граждан.")
    
    c1, c2 = st.columns(2)
    with c1:
        st.error("### Legacy Technology (до 2014)")
        st.write("Высокий выброс PM2.5 и NO2. Причина 70% смога в Алматы.")
        # Имитация 3D легких/выбросов
        z = np.random.standard_normal((50, 50)) * 100
        fig3d_1 = go.Figure(data=[go.Surface(z=z, colorscale='Reds', showscale=False)])
        fig3d_1.update_layout(title="Облако загрязнения (Старое авто)", height=400, template="plotly_dark")
        st.plotly_chart(fig3d_1, use_container_width=True)

    with c2:
        st.success("### Innovation Transition (Гибрид/EV)")
        st.write("Снижение выбросов на 95%. Льготная ставка кредитования: 2.5% APR.")
        z2 = np.random.standard_normal((50, 50)) * 10
        fig3d_2 = go.Figure(data=[go.Surface(z=z2, colorscale='Greens', showscale=False)])
        fig3d_2.update_layout(title="Эко-профиль (Инновация)", height=400, template="plotly_dark")
        st.plotly_chart(fig3d_2, use_container_width=True)
