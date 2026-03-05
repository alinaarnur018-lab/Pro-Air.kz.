import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px

# Данные для карты (пример координат районов Алматы)
# В реальном коде сюда полетят данные из твоего API
locations = pd.DataFrame({
    'Район': ['Медеуский', 'Алмалинский', 'Бостандыкский', 'Алатауский', 'Жетысуский'],
    'lat': [43.238, 43.255, 43.220, 43.280, 43.300],
    'lon': [76.945, 76.910, 76.920, 76.850, 76.930],
    'PM25': [120, 160, 110, 210, 195] # Пример уровня загрязнения
})

def show_tab1():
    st.markdown("## 🛰️ МОНИТОРИНГ: АЛМАТЫ LIVE")
    
    # 1. СТАТИСТИКА (Метрики)
    col1, col2, col3, col4 = st.columns(4)
    with col1: st.metric("PM2.5 СРЕДНИЙ", "158", "⚠ Опасно")
    with col2: st.metric("ИНВЕРСИЯ", "ЕСТЬ", "89%", delta_color="inverse")
    with col3: st.metric("ВЕТЕР", "0.5 м/с", "ШТИЛЬ")
    with col4: st.metric("ВЛАЖНОСТЬ", "68%", "СРЕДНЯЯ")

    st.write("---")

    # 2. РЕАЛЬНАЯ КАРТА (MAPBOX)
    st.subheader("📍 Интерактивная карта районов")
    
    # Создаем карту через Plotly Mapbox (профессиональный темный стиль)
    fig_map = px.scatter_mapbox(
        locations, lat="lat", lon="lon", 
        color="PM25", size="PM25",
        color_continuous_scale="Reds", 
        hover_name="Район", 
        zoom=11, height=600
    )
    
    fig_map.update_layout(
        mapbox_style="carto-darkmatter", # Тот самый "черный" профессиональный стиль
        margin={"r":0,"t":0,"l":0,"b":0},
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )
    
    st.plotly_chart(fig_map, use_container_width=True)

    # 3. ГРАФИК ПРОГНОЗА (7 ДНЕЙ / 24 ЧАСА)
    st.write("---")
    st.subheader("📅 Прогноз ALGORITHM AI (7 дней)")
    
    # Создаем выбор дня
    days = ["Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Вс"]
    selected_day = st.select_slider("Выберите день для детального анализа:", options=days)
    
    # Генерация почасового графика (твоя логика из Colab)
    hours = list(range(24))
    # Пример: ночью смог выше (инверсия), днем чуть ниже
    values = [180, 190, 200, 210, 190, 150, 120, 100, 90, 110, 130, 140, 150, 160, 170, 160, 150, 160, 180, 200, 210, 220, 200, 190]
    
    fig_line = go.Figure()
    fig_line.add_trace(go.Scatter(
        x=hours, y=values, 
        mode='lines+markers', 
        name='Прогноз PM2.5',
        line=dict(color='#00f2ff', width=4),
        fill='tozeroy', # Заливка под графиком для красоты
        fillcolor='rgba(0, 242, 255, 0.1)'
    ))
    
    fig_line.update_layout(
        title=f"Почасовая детализация: {selected_day}",
        template="plotly_dark",
        xaxis=dict(title="Час суток", gridcolor="#30363d"),
        yaxis=dict(title="PM2.5", gridcolor="#30363d"),
        height=400
    )
    
    st.plotly_chart(fig_line, use_container_width=True)

show_tab1()
