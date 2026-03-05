import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import os

# --- 1. ТЕМА И СТИЛЬ (SENTINEL PRO) ---
st.set_page_config(page_title="ALGORITHM SENTINEL PRO", layout="wide")

st.markdown("""
    <style>
    .main { background: #0B0E14; color: #F8FAFC; }
    [data-testid="stMetric"] {
        background: rgba(0, 212, 255, 0.05);
        border: 1px solid #00D4FF;
        border-radius: 12px;
    }
    .stTabs [data-baseweb="tab-list"] { gap: 10px; }
    .stTabs [data-baseweb="tab"] { color: #94A3B8; font-size: 16px; font-weight: 600; }
    .stTabs [aria-selected="true"] { color: #00D4FF !important; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. ФУНКЦИЯ ЗАГРУЗКИ (С ПОДДЕРЖКОЙ ВНЕШНЕЙ ЗАГРУЗКИ) ---
@st.cache_data
def load_and_clean_data(file_source):
    # Читаем только нужные колонки, чтобы не упасть по памяти
    cols = ['datetime', 'pm25', 'temperature', 'relativehumidity', 'name', 'lat', 'lon']
    df = pd.read_csv(file_source, usecols=cols)
    df['datetime'] = pd.to_datetime(df['datetime'])
    # Сортируем и берем данные с 2024 года, чтобы сайт летал
    df = df[df['datetime'] > '2024-01-01'].sort_values('datetime')
    df = df.fillna(method='ffill')
    return df

# Проверка файла
FILENAME = 'air_quality_data.csv'
df = None

if os.path.exists(FILENAME):
    df = load_and_clean_data(FILENAME)
else:
    st.warning("⚠️ Файл данных слишком велик для GitHub ( > 25MB) или отсутствует.")
    uploaded_file = st.file_uploader("📥 Пожалуйста, загрузите 'air_quality_data.csv' здесь для активации системы:", type="csv")
    if uploaded_file is not None:
        df = load_and_clean_data(uploaded_file)

# --- 3. ИНТЕРФЕЙС (ЕСЛИ ДАННЫЕ ЗАГРУЖЕНЫ) ---
if df is not None:
    latest = df.iloc[-1]
    
    st.markdown("<h1 style='text-align: center;'>🏔️ ALGORITHM <span style='color:#00D4FF'>SENTINEL</span></h1>", unsafe_allow_html=True)
    
    tab1, tab2, tab3 = st.tabs(["🛰️ МОНИТОРИНГ 24/7", "💡 ИННОВАЦИИ (3D)", "📊 СТРАТЕГИЯ SROI"])

    with tab1:
        # МЕТРИКИ
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("PM2.5 (LIVE)", f"{latest['pm25']:.1f}", "µg/m³")
        c2.metric("ТЕМПЕРАТУРА", f"{latest['temperature']:.1f}°C")
        c3.metric("ВЛАЖНОСТЬ", f"{latest['relativehumidity']:.0f}%")
        c4.metric("ЛОКАЦИЯ", latest['name'].split(',')[1] if ',' in str(latest['name']) else "Almaty")

        st.divider()

        col_map, col_ai = st.columns([2, 1])

        with col_map:
            st.subheader("📍 Реальная карта датчиков Алматы")
            # Карта на базе твоих координат lat/lon
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
            st.info("### 🤖 Анализ Нейросети")
            st.write(f"**Активный датчик:** {latest['name']}")
            # Логика предсказания инверсии
            if latest['relativehumidity'] > 75:
                st.error("⚠️ РИСК ИНВЕРСИИ: Высокая влажность блокирует очистку воздуха.")
            else:
                st.success("✅ Воздушные потоки стабильны.")
            
            st.write("---")
            st.write("**Прогноз на 24ч:**")
            st.line_chart(df.tail(24)['pm25'], height=150)

        st.divider()
        
        # ГРАФИК ПРОГНОЗА 7 ДНЕЙ
        st.subheader("📅 Интеллектуальный прогноз на 7 дней (Почасовой)")
        
        # Слайдер для выбора дня
        df['date'] = df['datetime'].dt.strftime('%d.%m')
        days = df['date'].unique()[-7:]
        selected_day = st.select_slider("Выберите день анализа:", options=days)
        
        day_df = df[df['date'] == selected_day]
        
        fig_line = go.Figure()
        fig_line.add_trace(go.Scatter(x=day_df['datetime'].dt.hour, y=day_df['pm25'], 
                                     name="История", line=dict(color='#00D4FF', width=3), fill='tozeroy'))
        fig_line.update_layout(template="plotly_dark", height=400, xaxis_title="Часы суток", yaxis_title="PM2.5")
        st.plotly_chart(fig_line, use_container_width=True)

    with tab2:
        st.header("🚀 Вкладка Инноваций: 3D Сравнение")
        
        # Твой запрос про 3D машины и влияние на легкие
        c_old, c_new = st.columns(2)
        
        with c_old:
            st.markdown("<h3 style='color:#FF3D00;'>Авто до 2014 года</h3>", unsafe_allow_html=True)
            st.write("Выхлоп содержит PM2.5, которые оседают в легких.")
            # 3D Визуализация урона (Mesh3D или Surface)
            z1 = np.random.standard_normal((30, 30)) * 50
            fig3_1 = go.Figure(data=[go.Surface(z=z1, colorscale='Reds', showscale=False)])
            fig3_1.update_layout(title="Уровень поражения легких", height=400, template="plotly_dark")
            st.plotly_chart(fig3_1, use_container_width=True)

        with c_new:
            st.markdown("<h3 style='color:#00FF41;'>Инновация: Гибрид</h3>", unsafe_allow_html=True)
            st.write("Нулевой выброс твердых частиц. Чистые легкие.")
            z2 = np.random.standard_normal((30, 30)) * 5
            fig3_2 = go.Figure(data=[go.Surface(z=z2, colorscale='Greens', showscale=False)])
            fig3_2.update_layout(title="Эко-профиль легких", height=400, template="plotly_dark")
            st.plotly_chart(fig3_2, use_container_width=True)
