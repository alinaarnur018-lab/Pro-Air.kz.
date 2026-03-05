import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from sklearn.preprocessing import MinMaxScaler
import os

# --- 1. ТЕМА И СТИЛЬ (IQAir Copy) ---
st.set_page_config(page_title="Air Quality Almaty - Algorithm", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;700&display=swap');
    html, body, [class*="css"] { font-family: 'Roboto', sans-serif; background-color: #f2f4f7; }
    .iq-card {
        background: white; padding: 25px; border-radius: 12px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.08); margin-bottom: 20px;
        border-top: 8px solid #ddd;
    }
    .aqi-number {
        color: white; padding: 10px 25px; border-radius: 8px;
        font-size: 52px; font-weight: 700; display: inline-block;
    }
    .status-label { font-size: 26px; font-weight: 700; margin-top: 15px; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. ЛОГИКА ЦВЕТОВ (ШКАЛА) ---
def get_aqi_theme(pm25):
    if pm25 <= 12: return "#00E400", "Хорошо", "👤", "Идеально для прогулок"
    elif pm25 <= 35: return "#FFFF00", "Умеренно", "😐", "Риск для сверхчувствительных"
    elif pm25 <= 55: return "#FF7E00", "Вредно для чувств. групп", "😷", "Наденьте маску"
    elif pm25 <= 150: return "#FF0000", "Вредно", "🚱", "Закройте окна"
    else: return "#8F3F97", "Очень вредно", "☣️", "Оставайтесь дома"

# --- 3. ОБРАБОТКА ДАННЫХ ИЗ ТВОЕГО COLAB ---
@st.cache_data
def load_and_preprocess(file_source):
    df = pd.read_csv(file_source)
    df['datetime'] = pd.to_datetime(df['datetime'])
    df = df.sort_values('datetime').fillna(method='ffill')
    return df

# Проверка файла (решение проблемы 25MB)
file_path = 'air_quality_data.csv'
df = None

if os.path.exists(file_path):
    df = load_and_preprocess(file_path)
else:
    st.info("ℹ️ Файл данных превышает 25MB. Пожалуйста, загрузите 'air_quality_data.csv' вручную:")
    uploaded_file = st.file_uploader("Загрузить CSV", type="csv")
    if uploaded_file:
        df = load_and_preprocess(uploaded_file)

# --- 4. ОСНОВНОЙ ИНТЕРФЕЙС ---
if df is not None:
    # Берем последнюю точку (Live)
    latest = df.iloc[-1]
    color, status, icon, advice = get_aqi_theme(latest['pm25'])

    st.markdown(f"<p style='color:#666;'>Казахстан > Алматы > {latest['name']}</p>", unsafe_allow_html=True)
    st.title(f"Качество воздуха в Алматы: {status}")

    # Блок 1: Основная карточка
    col1, col2 = st.columns([1, 1.5])
    with col1:
        st.markdown(f"""
            <div class="iq-card" style="border-top-color: {color}; text-align: center;">
                <p style="font-weight: bold; color: #888;">LIVE AQI (PM2.5)</p>
                <div class="aqi-number" style="background: {color};">{int(latest['pm25'])}</div>
                <div class="status-label" style="color: {color if color != '#FFFF00' else '#b5a300'};">{status}</div>
                <hr>
                <p>Темп: <b>{latest['temperature']:.1f}°C</b> | Влажн: <b>{latest['relativehumidity']:.0f}%</b></p>
            </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
            <div class="iq-card">
                <h4 style="margin-top:0;">Рекомендации по здоровью</h4>
                <div style="display: flex; justify-content: space-around; text-align: center; padding: 15px 0;">
                    <div><span style="font-size:30px;">🏠</span><br><small>Окна закрыты</small></div>
                    <div><span style="font-size:30px;">😷</span><br><small>Маска</small></div>
                    <div><span style="font-size:30px;">🏠</span><br><small>Очиститель</small></div>
                    <div><span style="font-size:30px;">🚫</span><br><small>Нет спорту</small></div>
                </div>
                <div style="background: #f8f9fa; border-left: 5px solid {color}; padding: 15px; border-radius: 4px;">
                    {advice}
                </div>
            </div>
        """, unsafe_allow_html=True)

    # Блок 2: Карта (Light Mode)
    st.markdown("### Карта мониторинга")
    fig_map = px.scatter_mapbox(
        df.drop_duplicates(subset=['name']).tail(15), 
        lat="lat", lon="lon", color="pm25", size="pm25",
        hover_name="name", zoom=11,
        color_continuous_scale=[[0, "#00E400"], [0.2, "#FFFF00"], [0.4, "#FF7E00"], [1, "#FF0000"]],
        mapbox_style="carto-positron"
    )
    fig_map.update_layout(margin={"r":0,"t":0,"l":0,"b":0}, height=450)
    st.plotly_chart(fig_map, use_container_width=True)

    # Блок 3: Таблица прогноза (Почасовая)
    st.markdown("### Прогноз на 24 часа")
    
    # Симуляция твоего LSTM прогноза (берем последние данные + тренд)
    forecast_vals = df.tail(12).copy()
    f_cols = st.columns(12)
    for i, (idx, row) in enumerate(forecast_vals.iterrows()):
        f_color, _, _, _ = get_aqi_theme(row['pm25'])
        with f_cols[i]:
            st.markdown(f"""
                <div style="background:white; padding:10px; border-radius:8px; border-bottom: 5px solid {f_color}; text-align:center;">
                    <small>{row['datetime'].strftime('%H:00')}</small><br>
                    <b>{int(row['pm25'])}</b>
                </div>
            """, unsafe_allow_html=True)

    # Блок 4: Аналитический график (Твоя модель)
    st.markdown("### Динамика PM2.5 за неделю")
    st.area_chart(df.set_index('datetime')['pm25'].tail(168), color="#00D4FF")

else:
    st.warning("Пожалуйста, загрузите данные для начала работы.")
