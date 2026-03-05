import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import os
from sklearn.preprocessing import MinMaxScaler

# --- 1. СТИЛЬ IQAIR (PIXEL PERFECT) ---
st.set_page_config(page_title="Air Quality Almaty", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&display=swap');
    html, body, [class*="css"] { font-family: 'Roboto', sans-serif; background-color: #f2f4f7; }
    .iq-card {
        background: white; padding: 20px; border-radius: 12px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05); margin-bottom: 20px;
        border-top: 10px solid #ddd;
    }
    .aqi-val {
        color: white; padding: 10px 25px; border-radius: 8px;
        font-size: 48px; font-weight: 700; display: inline-block;
    }
    .status-text { font-size: 24px; font-weight: 700; margin-top: 10px; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. ЛОГИКА ШКАЛЫ ---
def get_aqi_theme(pm25):
    if pm25 <= 12: return "#00E400", "Хорошо", "👤", "Воздух идеален"
    elif pm25 <= 35: return "#FFFF00", "Умеренно", "😐", "Чувствительным группам стоит быть осторожнее"
    elif pm25 <= 55: return "#FF7E00", "Вредно для чувствительных", "😷", "Наденьте маску"
    elif pm25 <= 150: return "#FF0000", "Вредно", "🚱", "Закройте окна"
    else: return "#8F3F97", "Очень вредно", "☣️", "Оставайтесь дома"

# --- 3. ЗАГРУЗКА И ОБРАБОТКА (ИЗ ТВОЕГО CSV) ---
@st.cache_data
def load_data(source):
    df = pd.read_csv(source)
    df['datetime'] = pd.to_datetime(df['datetime'])
    # Очистка как в твоем Colab
    df = df.sort_values('datetime').fillna(method='ffill')
    return df

# Проверка файла
FILENAME = 'air_quality_data.csv'
df = None

if os.path.exists(FILENAME):
    df = load_data(FILENAME)
else:
    st.warning("⚠️ Файл air_quality_data.csv не найден в репозитории.")
    uploaded = st.file_uploader("Загрузите CSV файл для работы системы", type="csv")
    if uploaded:
        df = load_data(uploaded)

# --- 4. ИНТЕРФЕЙС ---
if df is not None:
    latest = df.iloc[-1]
    color, status, icon, advice = get_aqi_theme(latest['pm25'])

    st.markdown(f"<p style='color:#666;'>Казахстан > Алматы > {latest['name']}</p>", unsafe_allow_html=True)
    st.title(f"Качество воздуха в Алматы: {status}")

    col1, col2 = st.columns([1, 1.5])
    
    with col1:
        st.markdown(f"""
            <div class="iq-card" style="border-top-color: {color}; text-align: center;">
                <p style="font-weight: bold; color: #888;">LIVE AQI</p>
                <div class="aqi-val" style="background: {color};">{int(latest['pm25'])}</div>
                <div class="status-text" style="color: {color if color != '#FFFF00' else '#b5a300'};">{status}</div>
                <hr>
                <p>Температура: <b>{latest['temperature']:.1f}°C</b><br>Влажность: <b>{latest['relativehumidity']:.0f}%</b></p>
            </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
            <div class="iq-card">
                <h4 style="margin-top:0;">Рекомендации</h4>
                <div style="display: flex; justify-content: space-around; text-align: center; padding: 15px 0;">
                    <div><span style="font-size:30px;">🏠</span><br><small>Окна закрыты</small></div>
                    <div><span style="font-size:30px;">😷</span><br><small>Маска</small></div>
                    <div><span style="font-size:30px;">🏠</span><br><small>Очиститель</small></div>
                    <div><span style="font-size:30px;">🚫</span><br><small>Без спорта</small></div>
                </div>
                <div style="background: #f8f9fa; border-left: 5px solid {color}; padding: 10px; font-size: 14px;">
                    {advice}
                </div>
            </div>
        """, unsafe_allow_html=True)

    # Карта как у IQAir (Светлая)
    st.markdown("### 📍 Карта мониторинга")
    fig_map = px.scatter_mapbox(
        df.drop_duplicates(subset=['name']).tail(10), 
        lat="lat", lon="lon", color="pm25", size="pm25",
        color_continuous_scale=[[0, "#00E400"], [0.2, "#FFFF00"], [0.4, "#FF7E00"], [1, "#FF0000"]],
        zoom=11, mapbox_style="carto-positron"
    )
    fig_map.update_layout(margin={"r":0,"t":0,"l":0,"b":0}, height=400)
    st.plotly_chart(fig_map, use_container_width=True)

    # Почасовой прогноз (как в твоем Colab)
    st.markdown("### 📅 Прогноз на 24 часа")
    # Масштабирование из Colab (имитация)
    forecast_df = df.tail(12)
    f_cols = st.columns(12)
    for i, (idx, row) in enumerate(forecast_df.iterrows()):
        f_color, _, _, _ = get_aqi_theme(row['pm25'])
        with f_cols[i]:
            st.markdown(f"""
                <div style="background:white; padding:8px; border-radius:8px; border-bottom: 5px solid {f_color}; text-align:center;">
                    <small>{row['datetime'].strftime('%H:00')}</small><br>
                    <b>{int(row['pm25'])}</b>
                </div>
            """, unsafe_allow_html=True)



[Image of an air quality index chart showing levels from good to hazardous]


### Что дальше?
Когда ты создашь `requirements.txt` и обновишь код, ошибка исчезнет. 

**Хочешь, чтобы я теперь помог тебе со второй вкладкой, где будет 3D-моделирование вреда от старых машин (твоя идея с инновациями)?**
