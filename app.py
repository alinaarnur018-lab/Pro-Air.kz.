import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import os
from sklearn.preprocessing import MinMaxScaler

# --- 1. НАСТРОЙКИ СТИЛЯ IQAIR ---
st.set_page_config(page_title="Air Quality in Almaty", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&display=swap');
    html, body, [class*="css"] { font-family: 'Roboto', sans-serif; background-color: #f2f4f7; }
    
    .iq-card {
        background: white; padding: 25px; border-radius: 12px;
        box-shadow: 0 2px 12px rgba(0,0,0,0.06); margin-bottom: 20px;
        border-top: 8px solid #ddd;
    }
    .aqi-box {
        color: white; padding: 12px 30px; border-radius: 8px;
        font-size: 54px; font-weight: 700; display: inline-block;
    }
    .status-text { font-size: 28px; font-weight: 700; margin-top: 10px; }
    .recommend-item { text-align: center; font-size: 13px; color: #555; }
    .icon-circle { font-size: 30px; margin-bottom: 5px; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. ЛОГИКА ЦВЕТОВ И РЕКОМЕНДАЦИЙ ---
def get_aqi_data(pm25):
    if pm25 <= 12: return "#00E400", "Хорошо", "👤", "Наслаждайтесь активным отдыхом."
    elif pm25 <= 35: return "#FFFF00", "Умеренно", "😐", "Чувствительным группам стоит ограничить нагрузки."
    elif pm25 <= 55: return "#FF7E00", "Вредно для чувствительных", "😷", "Наденьте маску на улице."
    elif pm25 <= 150: return "#FF0000", "Вредно", "🚱", "Закройте окна и включите очиститель."
    else: return "#8F3F97", "Очень вредно", "☣️", "Избегайте выхода на улицу."

# --- 3. ЗАГРУЗКА И ОБРАБОТКА (ТВОЯ ЛОГИКА) ---
@st.cache_data
def load_and_scale_data():
    file_path = 'air_quality_data.csv'
    if not os.path.exists(file_path): return None
    
    df = pd.read_csv(file_path)
    df['datetime'] = pd.to_datetime(df['datetime'])
    df = df.sort_values('datetime').fillna(method='ffill')
    
    # MinMaxScaler как в твоем Colab
    scaler = MinMaxScaler()
    df['pm25_scaled'] = scaler.fit_transform(df[['pm25']])
    return df

df = load_and_scale_data()

# --- 4. ВИЗУАЛИЗАЦИЯ ---
if df is not None:
    latest = df.iloc[-1]
    color, status, icon, advice = get_aqi_data(latest['pm25'])

    # Хлебные крошки
    st.markdown(f"<p style='color:#777; font-size:14px; margin-bottom:5px;'>Казахстан > Алматы > {latest['name']}</p>", unsafe_allow_html=True)
    st.title(f"Качество воздуха в Алматы: {status}")

    col_main, col_side = st.columns([1, 1.3])

    with col_main:
        st.markdown(f"""
            <div class="iq-card" style="border-top-color: {color}; text-align: center;">
                <p style="font-weight: 700; color: #888; letter-spacing: 1px;">LIVE AQI</p>
                <div class="aqi-box" style="background-color: {color};">{int(latest['pm25'])}</div>
                <div class="status-text" style="color: {color if color != '#FFFF00' else '#b5a300'};">{status}</div>
                <hr style="margin: 20px 0; border: 0; border-top: 1px solid #eee;">
                <p style="font-size: 15px;">Загрязнитель: <b>PM2.5</b> | Темп: <b>{latest['temperature']:.1f}°C</b></p>
            </div>
        """, unsafe_allow_html=True)

    with col_side:
        st.markdown(f"""
            <div class="iq-card">
                <h3 style="margin-top:0; font-size:20px;">Рекомендации по защите</h3>
                <div style="display: flex; justify-content: space-around; margin: 20px 0;">
                    <div class="recommend-item"><div class="icon-circle">🏠</div>Закрыть окна</div>
                    <div class="recommend-item"><div class="icon-circle">😷</div>Маска</div>
                    <div class="recommend-item"><div class="icon-circle">🏠</div>Очиститель</div>
                    <div class="recommend-item"><div class="icon-circle">🚫</div>Без спорта</div>
                </div>
                <div style="background: #f8f9fa; border-left: 5px solid {color}; padding: 15px; border-radius: 4px; font-size: 14px;">
                    <b>Совет Algorithm AI:</b> {advice}
                </div>
            </div>
        """, unsafe_allow_html=True)

    # КАРТА (Светлая как в IQAir)
    st.markdown("### 📍 Карта мониторинга")
    fig_map = px.scatter_mapbox(
        df.drop_duplicates(subset=['name']).tail(12), 
        lat="lat", lon="lon", color="pm25", size="pm25",
        color_continuous_scale=[[0, "#00E400"], [0.2, "#FFFF00"], [0.4, "#FF7E00"], [1, "#FF0000"]],
        zoom=11, mapbox_style="carto-positron"
    )
    fig_map.update_layout(margin={"r":0,"t":0,"l":0,"b":0}, height=400)
    st.plotly_chart(fig_map, use_container_width=True)

    # ТАБЛИЦА ПРОГНОЗА (СЕТКА)
    st.markdown("### 📅 Прогноз на 12 часов")
    forecast_df = df.tail(12)
    f_cols = st.columns(12)
    for i, (idx, row) in enumerate(forecast_df.iterrows()):
        f_color, _, _, _ = get_aqi_data(row['pm25'])
        with f_cols[i]:
            st.markdown(f"""
                <div style="text-align:center; background:white; padding:10px; border-radius:8px; border-bottom: 5px solid {f_color};">
                    <small style="color:#888;">{row['datetime'].strftime('%H:00')}</small><br>
                    <b style="font-size:18px;">{int(row['pm25'])}</b>
                </div>
            """, unsafe_allow_html=True)

    # ГРАФИК
    st.markdown("### Изменение уровня за неделю")
    st.area_chart(df.set_index('datetime')['pm25'].tail(168), color="#00D4FF")

else:
    st.error("❌ Файл 'air_quality_data.csv' не найден.")
    st.info("Загрузите CSV файл в репозиторий GitHub для запуска мониторинга.")
