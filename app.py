import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import os

# --- 1. ТЕМА IQAir (СВЕТЛАЯ И ЧИСТАЯ) ---
st.set_page_config(page_title="Air Quality in Almaty", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;700&display=swap');
    html, body, [class*="css"] { font-family: 'Roboto', sans-serif; background-color: #f2f4f7; }
    
    /* Основной контейнер как у IQAir */
    .reportview-container { background: #f2f4f7; }
    
    /* Карточки */
    .iq-card {
        background: white;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.05);
        margin-bottom: 20px;
    }
    
    .aqi-value { font-size: 48px; font-weight: 700; color: white; padding: 10px 20px; border-radius: 8px; display: inline-block; }
    .status-text { font-size: 24px; font-weight: 700; margin-top: 10px; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. ЛОГИКА ЦВЕТОВ AQI ---
def get_aqi_info(pm25):
    if pm25 <= 12: return "#00E400", "Хорошо", "👤", "Можно гулять"
    elif pm25 <= 35: return "#FFFF00", "Умеренно", "😐", "Чувствительным группам стоит быть осторожнее"
    elif pm25 <= 55: return "#FF7E00", "Вредно для чувствительных", "😷", "Наденьте маску на улице"
    elif pm25 <= 150: return "#FF0000", "Вредно", "🚱", "Закройте окна, включите очиститель"
    else: return "#8F3F97", "Очень вредно", "☣️", "Избегайте выхода на улицу"

# --- 3. ЗАГРУЗКА ДАННЫХ ---
@st.cache_data
def load_data():
    if os.path.exists('air_quality_data.csv'):
        df = pd.read_csv('air_quality_data.csv')
        df['datetime'] = pd.to_datetime(df['datetime'])
        return df.sort_values('datetime')
    return None

df = load_data()

if df is not None:
    # Берем данные с 2024 года и последнюю запись
    df_recent = df[df['datetime'] > '2024-01-01']
    latest = df_recent.iloc[-1]
    color, status, icon, advice = get_aqi_info(latest['pm25'])

    # --- ВЕРХНЯЯ ПАНЕЛЬ (HEADER) ---
    st.markdown(f"<p style='color:#666;'>Казахстан > Алматы</p>", unsafe_allow_html=True)
    st.title(f"Качество воздуха в Алматы: {status}")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown(f"""
            <div class="iq-card" style="text-align: center; border-top: 8px solid {color};">
                <p style="color: #666; font-weight: bold;">LIVE AQI</p>
                <div class="aqi-value" style="background-color: {color};">{int(latest['pm25'])}</div>
                <div class="status-text" style="color: {color if color != '#FFFF00' else '#b5a300'};">{status}</div>
                <hr>
                <p style="font-size: 14px; color: #444;">Основной загрязнитель: <b>PM2.5</b></p>
            </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
            <div class="iq-card">
                <h3>Рекомендации по защите</h3>
                <div style="display: flex; justify-content: space-around; padding: 20px 0;">
                    <div style="text-align:center;">{icon}<br><small>Окна закрыты</small></div>
                    <div style="text-align:center;">😷<br><small>Маска</small></div>
                    <div style="text-align:center;">🏠<br><small>Очиститель</small></div>
                    <div style="text-align:center;">🚫<br><small>Без спорта</small></div>
                </div>
                <p style="background: #f8f9fa; padding: 10px; border-radius: 8px; font-size: 14px;">{advice}</p>
            </div>
        """, unsafe_allow_html=True)

    # --- КАРТА ---
    st.markdown("### Интерактивная карта")
    fig_map = px.scatter_mapbox(
        df_recent.drop_duplicates(subset=['name']), 
        lat="lat", lon="lon", color="pm25",
        color_continuous_scale=[[0, "#00E400"], [0.2, "#FFFF00"], [0.4, "#FF7E00"], [0.6, "#FF0000"], [1, "#8F3F97"]],
        zoom=11, mapbox_style="carto-positron" # Светлая карта как у IQAir
    )
    fig_map.update_layout(margin={"r":0,"t":0,"l":0,"b":0}, height=400)
    st.plotly_chart(fig_map, use_container_width=True)

    # --- ТАБЛИЦА ПРОГНОЗА (ПО ЧАСАМ) ---
    st.markdown("### Почасовой прогноз")
    
    # Берем последние 24 часа
    forecast_df = df_recent.tail(24).copy()
    
    # Рисуем горизонтальную таблицу
    cols = st.columns(12) # Первые 12 часов
    for i, (idx, row) in enumerate(forecast_df.iloc[:12].iterrows()):
        f_color, _, _, _ = get_aqi_info(row['pm25'])
        with cols[i]:
            st.markdown(f"""
                <div style="text-align:center; padding: 5px; background: white; border-radius: 5px; border-bottom: 5px solid {f_color};">
                    <small>{row['datetime'].strftime('%H:00')}</small><br>
                    <b>{int(row['pm25'])}</b>
                </div>
            """, unsafe_allow_html=True)

    # --- ГРАФИК ---
    st.markdown("### Изменение уровня загрязнения")
    st.line_chart(df_recent.set_index('datetime')['pm25'].tail(168))

else:
    st.error("Файл 'air_quality_data.csv' не найден.")
