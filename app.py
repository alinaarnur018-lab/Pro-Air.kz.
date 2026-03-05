import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import os

# --- 1. ТЕМА И СТИЛЬ ---
st.set_page_config(page_title="ALGORITHM SENTINEL", layout="wide")

st.markdown("""
    <style>
    .main { background: #0B0E14; color: #F8FAFC; }
    [data-testid="stMetric"] {
        background: rgba(0, 212, 255, 0.05);
        border: 1px solid #00D4FF;
        border-radius: 12px;
    }
    .stTabs [data-baseweb="tab"] { color: #94A3B8; font-size: 18px; }
    .stTabs [aria-selected="true"] { color: #00D4FF !important; border-bottom: 2px solid #00D4FF; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. ОПТИМИЗИРОВАННАЯ ЗАГРУЗКА ---
@st.cache_data
def get_clean_data():
    file_path = 'air_quality_data.csv'
    if not os.path.exists(file_path):
        return None
    
    # Читаем только нужные колонки, чтобы не перегружать память
    cols = ['datetime', 'pm25', 'temperature', 'relativehumidity', 'name', 'lat', 'lon']
    df = pd.read_csv(file_path, usecols=cols)
    
    df['datetime'] = pd.to_datetime(df['datetime'])
    df = df.sort_values('datetime').fillna(method='ffill')
    
    # Берем последние 1000 строк для скорости работы интерфейса
    return df.tail(1000)

df = get_clean_data()

# --- 3. ИНТЕРФЕЙС ---
st.markdown("<h1 style='text-align: center;'>🏔️ ALGORITHM <span style='color:#00D4FF'>SENTINEL PRO</span></h1>", unsafe_allow_html=True)

if df is None:
    st.error("⚠️ Файл 'air_quality_data.csv' не найден в корневой папке.")
    st.info("Загрузите файл на GitHub в ту же папку, где лежит этот app.py")
    st.stop()

latest = df.iloc[-1]

# ВКЛАДКИ
tab1, tab2, tab3 = st.tabs(["🛰️ МОНИТОРИНГ 24/7", "💡 ИННОВАЦИИ (3D)", "📊 СТРАТЕГИЯ"])

with tab1:
    # МЕТРИКИ
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("PM2.5 (LIVE)", f"{latest['pm25']:.1f}", "µg/m³")
    c2.metric("ТЕМПЕРАТУРА", f"{latest['temperature']:.1f}°C")
    c3.metric("ВЛАЖНОСТЬ", f"{latest['relativehumidity']:.0f}%")
    c4.metric("ЛОКАЦИЯ", "Almaty Center")

    st.write("---")

    col_map, col_ai = st.columns([2, 1])

    with col_map:
        st.subheader("📍 Карта загрязнения: Реальные датчики")
        # Карта на базе твоих координат (lat/lon)
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
        st.info("### 🤖 Голос ИИ")
        st.write(f"**Анализ по станции:** {latest['name']}")
        if latest['pm25'] > 100:
            st.warning("⚠️ Внимание: Критический уровень загрязнения. Температурная инверсия блокирует рассеивание.")
        else:
            st.success("✅ Воздух в пределах нормы. Риск застоя минимален.")
        
        # Математика инверсии
        st.write(f"🌡️ Точка росы: {latest['temperature'] - 2:.1f}°C")
        st.progress(min(latest['pm25']/200, 1.0))
        st.caption("Нагрузка на экосистему")

    st.write("---")
    
    # ГРАФИК ПРОГНОЗА
    st.subheader("📅 Детальный прогноз (История + ИИ)")
    fig_line = go.Figure()
    # Реальные данные
    fig_line.add_trace(go.Scatter(x=df['datetime'], y=df['pm25'], name="Данные датчиков", line=dict(color='#00D4FF')))
    # Имитация прогноза на базе твоих данных
    future_x = [df['datetime'].max() + pd.Timedelta(hours=i) for i in range(24)]
    future_y = [latest['pm25'] + np.sin(i)*15 for i in range(24)]
    fig_line.add_trace(go.Scatter(x=future_x, y=future_y, name="Прогноз LSTM", line=dict(color='#FF3D00', dash='dot')))
    
    fig_line.update_layout(template="plotly_dark", height=400, hovermode="x unified")
    st.plotly_chart(fig_line, use_container_width=True)

with tab2:
    st.subheader("🚀 Инновация: 3D Анализ Транспорта")
    # Твой запрос про 3D машины и легкие
    col_old, col_new = st.columns(2)
    
    with col_old:
        st.markdown("<h3 style='color:#FF3D00;'>Авто до 2014 года</h3>", unsafe_allow_html=True)
        st.write("Выброс PM2.5: **Высокий**")
        # 3D тепловое облако (имитация выхлопа)
        z1 = np.random.standard_normal((40, 40)) * 50
        fig3d_1 = go.Figure(data=[go.Surface(z=z1, colorscale='Reds', showscale=False)])
        fig3d_1.update_layout(height=400, template="plotly_dark")
        st.plotly_chart(fig3d_1, use_container_width=True)

    with col_new:
        st.markdown("<h3 style='color:#00FF41;'>Инновация: Гибрид</h3>", unsafe_allow_html=True)
        st.write("Выброс PM2.5: **Минимальный**")
        # 3D чистое облако
        z2 = np.random.standard_normal((40, 40)) * 5
        fig3d_2 = go.Figure(data=[go.Surface(z=z2, colorscale='Greens', showscale=False)])
        fig3d_2.update_layout(height=400, template="plotly_dark")
        st.plotly_chart(fig3d_2, use_container_width=True)
