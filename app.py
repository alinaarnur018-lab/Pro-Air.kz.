import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import os
from sklearn.preprocessing import MinMaxScaler

# --- 1. ДИЗАЙН IQAIR (PIXEL PERFECT) ---
st.set_page_config(page_title="Воздух Алматы - IQAir Style", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;700&display=swap');
    html, body, [class*="css"] { font-family: 'Roboto', sans-serif; background-color: #f2f4f7; }
    
    .iq-card {
        background: white; padding: 25px; border-radius: 12px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.05); margin-bottom: 20px;
        border-top: 10px solid #ddd;
    }
    .aqi-value {
        color: white; padding: 10px 25px; border-radius: 8px;
        font-size: 52px; font-weight: 700; display: inline-block;
    }
    .status-text { font-size: 26px; font-weight: 700; margin-top: 10px; }
    .recommend-box { background: #f8f9fa; border-left: 5px solid #ddd; padding: 15px; border-radius: 4px; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. ЦВЕТОВАЯ ШКАЛА IQAIR ---
def get_aqi_theme(pm25):
    if pm25 <= 12: return "#00E400", "Хорошо", "👤", "Воздух отличный. Идеально для прогулок."
    elif pm25 <= 35: return "#FFFF00", "Умеренно", "😐", "Чувствительным группам стоит ограничить нагрузки."
    elif pm25 <= 55: return "#FF7E00", "Вредно для чувств. групп", "😷", "Наденьте маску на улице."
    elif pm25 <= 150: return "#FF0000", "Вредно", "🚱", "Закройте окна, включите очиститель воздуха."
    else: return "#8F3F97", "Очень вредно", "☣️", "Оставайтесь дома, избегайте нагрузок."

# --- 3. ЗАГРУЗКА ДАННЫХ ---
@st.cache_data
def load_and_fix_data(source):
    df = pd.read_csv(source)
    df['datetime'] = pd.to_datetime(df['datetime'])
    # Убираем пустые значения как в твоем Colab
    df = df.sort_values('datetime').fillna(method='ffill')
    return df

# Проверка наличия файла
df = None
if os.path.exists('air_quality_data.csv'):
    df = load_and_fix_data('air_quality_data.csv')
else:
    st.info("👋 Привет! Файл 'air_quality_data.csv' не найден автоматически (возможно, из-за размера >25МБ).")
    uploaded_file = st.file_uploader("📥 Загрузи CSV файл здесь, чтобы сайт ожил:", type="csv")
    if uploaded_file:
        df = load_and_fix_data(uploaded_file)

# --- 4. ОСНОВНОЙ ЭКРАН (ТОЧНО КАК IQAIR) ---
if df is not None:
    latest = df.iloc[-1]
    color, status, icon, advice = get_aqi_theme(latest['pm25'])

    st.markdown(f"<p style='color:#666;'>Казахстан > Алматы > {latest['name']}</p>", unsafe_allow_html=True)
    st.title(f"Качество воздуха в Алматы сейчас")

    col1, col2 = st.columns([1, 1.5])

    with col1:
        st.markdown(f"""
            <div class="iq-card" style="border-top-color: {color}; text-align: center;">
                <p style="font-weight: bold; color: #888;">AQI (PM2.5)</p>
                <div class="aqi-value" style="background: {color};">{int(latest['pm25'])}</div>
                <div class="status-text" style="color: {color if color != '#FFFF00' else '#c2b100'};">{status}</div>
                <hr>
                <p>Темп: <b>{latest['temperature']:.1f}°C</b> | Влажность: <b>{latest['relativehumidity']:.0f}%</b></p>
            </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
            <div class="iq-card">
                <h4 style="margin-top:0;">Рекомендации по здоровью</h4>
                <div style="display: flex; justify-content: space-around; text-align: center; padding: 20px 0;">
                    <div><span style="font-size:35px;">🏠</span><br><small>Окна закрыты</small></div>
                    <div><span style="font-size:35px;">😷</span><br><small>Носите маску</small></div>
                    <div><span style="font-size:35px;">🏠</span><br><small>Очиститель</small></div>
                    <div><span style="font-size:35px;">🚫</span><br><small>Без спорта</small></div>
                </div>
                <div class="recommend-box" style="border-left-color: {color};">
                    <b>Совет от Algorithm AI:</b> {advice}
                </div>
            </div>
        """, unsafe_allow_html=True)

    # Карта как у IQAir (Светлая)
    st.markdown("### 📍 Карта мониторинга Алматы")
    fig_map = px.scatter_mapbox(
        df.drop_duplicates(subset=['name']).tail(12), 
        lat="lat", lon="lon", color="pm25", size="pm25",
        color_continuous_scale=[[0, "#00E400"], [0.2, "#FFFF00"], [0.4, "#FF7E00"], [1, "#FF0000"]],
        zoom=11, mapbox_style="carto-positron"
    )
    fig_map.update_layout(margin={"r":0,"t":0,"l":0,"b":0}, height=450)
    st.plotly_chart(fig_map, use_container_width=True)

    # Почасовая сетка (Фишка IQAir)
    st.markdown("### Прогноз на ближайшие часы")
    forecast_df = df.tail(12)
    f_cols = st.columns(12)
    for i, (idx, row) in enumerate(forecast_df.iterrows()):
        f_color, _, _, _ = get_aqi_theme(row['pm25'])
        with f_cols[i]:
            st.markdown(f"""
                <div style="background:white; padding:10px; border-radius:8px; border-bottom: 5px solid {f_color}; text-align:center;">
                    <small>{row['datetime'].strftime('%H:00')}</small><br>
                    <b style="font-size:18px;">{int(row['pm25'])}</b>
                </div>
            """, unsafe_allow_html=True)

    # Недельный график
    st.markdown("### График загрязнения за неделю")
    st.area_chart(df.set_index('datetime')['pm25'].tail(168), color="#00D4FF")

else:
    st.warning("Ожидание загрузки данных...")
