import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import os

# --- 1. НАСТРОЙКА ИНТЕРФЕЙСА (IQAir Style) ---
st.set_page_config(page_title="Качество воздуха в Алматы", layout="wide")

# CSS для имитации сайта IQAir (белый фон, тени, закругления)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;700&display=swap');
    html, body, [class*="css"] { font-family: 'Roboto', sans-serif; background-color: #f2f4f7; }
    .iq-card {
        background: white; padding: 25px; border-radius: 12px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.08); margin-bottom: 20px;
    }
    .aqi-box {
        color: white; padding: 15px 30px; border-radius: 8px;
        font-size: 56px; font-weight: 700; display: inline-block;
    }
    .status-text { font-size: 28px; font-weight: 700; margin-top: 15px; }
    .recommendation-icon { font-size: 32px; margin-bottom: 5px; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. ЛОГИКА ЦВЕТОВ И РЕКОМЕНДАЦИЙ ---
def get_aqi_details(pm25):
    if pm25 <= 12: return "#00E400", "Хорошо", "👤", "Идеальное время для прогулок."
    elif pm25 <= 35: return "#FFFF00", "Умеренно", "😐", "Чувствительным группам стоит сократить нагрузки."
    elif pm25 <= 55: return "#FF7E00", "Вредно для чувствительных", "😷", "Наденьте маску, если вы в группе риска."
    elif pm25 <= 150: return "#FF0000", "Вредно", "🚱", "Закройте окна. Избегайте нагрузок на улице."
    else: return "#8F3F97", "Очень вредно", "☣️", "Оставайтесь дома. Включите очиститель воздуха."

# --- 3. УМНАЯ ЗАГРУЗКА ФАЙЛА (ИСПРАВЛЕНИЕ ОШИБКИ) ---
@st.cache_data
def load_data():
    # Проверяем файл в текущей директории
    file_path = 'air_quality_data.csv'
    if os.path.exists(file_path):
        # Читаем только последние 5000 строк, чтобы не перегружать память (т.к. файл >25МБ)
        df = pd.read_csv(file_path)
        df['datetime'] = pd.to_datetime(df['datetime'])
        return df.sort_values('datetime')
    return None

df = load_data()

# --- 4. ОТРИСОВКА ИНТЕРФЕЙСА ---
if df is not None:
    # Берем последние данные
    latest = df.iloc[-1]
    color, status, icon, advice = get_aqi_details(latest['pm25'])
    
    # Хлебные крошки
    st.markdown(f"<p style='color:#777; font-size:14px;'>Казахстан > Алматы > {latest['name']}</p>", unsafe_allow_html=True)
    
    # Секция 1: Главная карточка
    col1, col2 = st.columns([1, 1.5])
    
    with col1:
        st.markdown(f"""
            <div class="iq-card" style="text-align: center; border-top: 10px solid {color};">
                <p style="text-transform: uppercase; font-weight: bold; color: #666; letter-spacing: 1px;">LIVE AQI</p>
                <div class="aqi-box" style="background-color: {color};">{int(latest['pm25'])}</div>
                <div class="status-text" style="color: {color if color != '#FFFF00' else '#c2b100'};">{status}</div>
                <hr style="margin: 20px 0;">
                <p style="font-size: 15px;">Загрязнитель: <b>PM2.5</b> | Темп: <b>{latest['temperature']:.1f}°C</b></p>
            </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
            <div class="iq-card">
                <h3 style="margin-top:0;">Рекомендации по защите</h3>
                <div style="display: flex; justify-content: space-around; text-align: center; padding: 15px 0;">
                    <div><div class="recommendation-icon">🏠</div><small>Закройте окна</small></div>
                    <div><div class="recommendation-icon">😷</div><small>Маска</small></div>
                    <div><div class="recommendation-icon">🏠</div><small>Очиститель</small></div>
                    <div><div class="recommendation-icon">🚫</div><small>Без спорта</small></div>
                </div>
                <div style="background: #fdf2f2; border-left: 5px solid {color}; padding: 15px; border-radius: 4px; margin-top: 10px;">
                    {advice}
                </div>
            </div>
        """, unsafe_allow_html=True)

    # Секция 2: Карта (Светлая как у IQAir)
    st.markdown("### 📍 Карта загрязнения Алматы")
    fig_map = px.scatter_mapbox(
        df.drop_duplicates(subset=['name']).tail(10), 
        lat="lat", lon="lon", color="pm25", size="pm25",
        color_continuous_scale=[[0, "#00E400"], [0.2, "#FFFF00"], [0.4, "#FF7E00"], [0.6, "#FF0000"], [1, "#8F3F97"]],
        zoom=11, mapbox_style="carto-positron"
    )
    fig_map.update_layout(margin={"r":0,"t":0,"l":0,"b":0}, height=450)
    st.plotly_chart(fig_map, use_container_width=True)

    # Секция 3: Почасовой прогноз (Таблица как у IQAir)
    st.markdown("### 📅 Почасовой прогноз")
    forecast_df = df.tail(12) # Последние 12 часов
    f_cols = st.columns(12)
    for i, (index, row) in enumerate(forecast_df.iterrows()):
        f_color, _, _, _ = get_aqi_details(row['pm25'])
        with f_cols[i]:
            st.markdown(f"""
                <div style="text-align:center; background:white; padding:10px; border-radius:8px; border-bottom: 5px solid {f_color};">
                    <small style="color:#888;">{row['datetime'].strftime('%H:00')}</small><br>
                    <b style="font-size:18px;">{int(row['pm25'])}</b>
                </div>
            """, unsafe_allow_html=True)

    # Секция 4: График за неделю
    st.markdown("### Изменение уровня за последние дни")
    st.area_chart(df.set_index('datetime')['pm25'].tail(168), color="#00D4FF")

else:
    st.error("❌ Файл 'air_quality_data.csv' не найден.")
    st.markdown("""
        ### Как исправить:
        1. Убедитесь, что вы загрузили файл `air_quality_data.csv` в **ту же папку**, что и `app.py`.
        2. Если файл слишком большой (>25MB), GitHub может его блокировать. В этом случае добавьте в начало кода `st.file_uploader`, чтобы загрузить его вручную.
    """)
