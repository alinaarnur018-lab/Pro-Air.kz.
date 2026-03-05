import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import os

# --- 1. СТИЛИЗАЦИЯ ПОД IQAir (PIXEL PERFECT) ---
st.set_page_config(page_title="Качество воздуха в Алматы", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;700&display=swap');
    html, body, [class*="css"] { font-family: 'Roboto', sans-serif; background-color: #f2f4f7; }
    
    /* Карточки как на IQAir */
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
    .recommendation-text { background: #f8f9fa; padding: 15px; border-radius: 8px; font-size: 14px; margin-top: 10px; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. ЛОГИКА ШКАЛЫ IQAir ---
def get_aqi_theme(pm25):
    if pm25 <= 12: return "#00E400", "Хорошо", "👤", "Воздух чистый, идеальное время для прогулок."
    elif pm25 <= 35: return "#FFFF00", "Умеренно", "😐", "Качество воздуха приемлемое. Чувствительным людям стоит меньше быть на улице."
    elif pm25 <= 55: return "#FF7E00", "Вредно для чувствительных групп", "😷", "Наденьте маску. Сократите время пребывания на открытом воздухе."
    elif pm25 <= 150: return "#FF0000", "Вредно для здоровья", "🚱", "Закройте окна. Избегайте физических нагрузок на улице."
    else: return "#8F3F97", "Очень вредно", "☣️", "Оставайтесь дома. Используйте очистители воздуха."

# --- 3. ОБРАБОТКА ДАННЫХ (С ЗАЩИТОЙ ОТ ОШИБОК) ---
@st.cache_data
def process_data(file_obj):
    # Читаем только нужные колонки для экономии памяти
    df = pd.read_csv(file_source)
    df['datetime'] = pd.to_datetime(df['datetime'])
    # Берем данные только последних лет, чтобы сайт не тормозил
    df = df.sort_values('datetime')
    return df

# Поиск файла
file_path = 'air_quality_data.csv'
file_source = None

if os.path.exists(file_path):
    file_source = file_path
else:
    st.info("ℹ️ Файл данных превышает 25MB и ограничен GitHub. Загрузите его вручную ниже:")
    file_source = st.file_uploader("Загрузите air_quality_data.csv", type="csv")

# --- 4. ОТРИСОВКА ИНТЕРФЕЙСА ---
if file_source:
    try:
        df = process_data(file_source)
        latest = df.iloc[-1] # Последняя запись из твоего CSV
        color, status, icon, advice = get_aqi_theme(latest['pm25'])

        # Шапка
        st.markdown(f"<p style='color:#666;'>Казахстан > Алматы > {latest['name']}</p>", unsafe_allow_html=True)
        st.title(f"Качество воздуха в г. Алматы: {status}")

        col1, col2 = st.columns([1, 1.5])

        with col1:
            st.markdown(f"""
                <div class="iq-card" style="border-top-color: {color}; text-align: center;">
                    <p style="font-weight: bold; color: #888;">LIVE AQI (PM2.5)</p>
                    <div class="aqi-number" style="background: {color};">{int(latest['pm25'])}</div>
                    <div class="status-label" style="color: {color if color != '#FFFF00' else '#b5a300'};">{status}</div>
                    <hr>
                    <p>Температура: <b>{latest['temperature']:.1f}°C</b><br>Влажность: <b>{latest['relativehumidity']:.0f}%</b></p>
                </div>
            """, unsafe_allow_html=True)

        with col2:
            st.markdown(f"""
                <div class="iq-card">
                    <h4 style="margin-top:0;">Рекомендации IQAir</h4>
                    <div style="display: flex; justify-content: space-around; text-align: center; padding: 15px 0;">
                        <div><span style="font-size:30px;">🏠</span><br><small>Закрыть окна</small></div>
                        <div><span style="font-size:30px;">😷</span><br><small>Маска</small></div>
                        <div><span style="font-size:30px;">🏠</span><br><small>Очиститель</small></div>
                        <div><span style="font-size:30px;">🚫</span><br><small>Без спорта</small></div>
                    </div>
                    <div class="recommendation-text" style="border-left: 5px solid {color};">
                        <b>Совет дня:</b> {advice}
                    </div>
                </div>
            """, unsafe_allow_html=True)

        # Карта Алматы (Светлая как у IQAir)
        st.markdown("### 📍 Карта мониторинга")
        # Берем уникальные датчики из твоего CSV
        map_data = df.drop_duplicates(subset=['name']).tail(15)
        fig_map = px.scatter_mapbox(
            map_data, lat="lat", lon="lon", color="pm25", size="pm25",
            hover_name="name", zoom=11,
            color_continuous_scale=[[0, "#00E400"], [0.2, "#FFFF00"], [0.4, "#FF7E00"], [1, "#FF0000"]],
            mapbox_style="carto-positron"
        )
        fig_map.update_layout(margin={"r":0,"t":0,"l":0,"b":0}, height=450)
        st.plotly_chart(fig_map, use_container_width=True)

        # Почасовой прогноз (как сетка IQAir)
        st.markdown("### Прогноз на ближайшие часы")
        forecast = df.tail(10)
        f_cols = st.columns(10)
        for i, (idx, row) in enumerate(forecast.iterrows()):
            f_color, _, _, _ = get_aqi_theme(row['pm25'])
            with f_cols[i]:
                st.markdown(f"""
                    <div style="background:white; padding:10px; border-radius:8px; border-bottom: 5px solid {f_color}; text-align:center;">
                        <small>{row['datetime'].strftime('%H:00')}</small><br>
                        <b>{int(row['pm25'])}</b>
                    </div>
                """, unsafe_allow_html=True)

    except Exception as e:
        st.error(f"Ошибка при чтении данных: {e}")
else:
    st.info("Ожидание загрузки файла air_quality_data.csv...")
