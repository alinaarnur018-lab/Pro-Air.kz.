import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px

# --- НАСТРОЙКИ СТИЛЯ (CYBER DARK) ---
st.set_page_config(page_title="ALGORITHM SENTINEL", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
    <style>
    .main { background-color: #0B0E14; color: #ffffff; }
    [data-testid="stHeader"] { background: rgba(0,0,0,0); }
    .stTabs [data-baseweb="tab-list"] { gap: 24px; background-color: #0B0E14; }
    .stTabs [data-baseweb="tab"] { height: 50px; background-color: #161B22; border-radius: 10px 10px 0 0; color: white; }
    .stMetric { background: #161B22; border: 1px solid #30363D; border-radius: 15px; padding: 20px; }
    </style>
    """, unsafe_allow_html=True)

# --- ВЕРХНЯЯ ПАНЕЛЬ ---
st.title("🏔️ ALGORITHM SENTINEL")
st.caption("Autonomous Logistic Global Observation & Real-time Integrated Thermal Monitoring")

# --- СОЗДАНИЕ ВКЛАДОК ---
tab1, tab2, tab3 = st.tabs(["🛰️ MONITORING", "💡 INNOVATION", "📊 STRATEGY"])

# --- ВКЛАДКА 1: МОНИТОРИНГ ---
with tab1:
    col_map, col_ctrl = st.columns([3, 1])
    
    with col_ctrl:
        st.subheader("AI Agent Console")
        pm_val = st.slider("Simulated PM2.5", 0, 250, 45)
        risk = "HIGH" if pm_val > 100 else "STABLE"
        st.error(f"STATUS: {risk}")
        st.info("PREDICTION: Inversion risk 87% within 4h")
        
    with col_map:
        # Имитация карты Алматы через Heatmap
        map_data = np.random.rand(10, 10) * pm_val
        fig_map = px.imshow(map_data, color_continuous_scale='Turbo', origin='lower')
        fig_map.update_layout(template="plotly_dark", height=450, margin=dict(l=0,r=0,t=0,b=0))
        st.plotly_chart(fig_map, use_container_width=True)

# --- ВКЛАДКА 2: ИННОВАЦИЯ (3D СРАВНЕНИЕ) ---
with tab2:
    st.header("Innovation Spotlight: Mobility Transition")
    c1, c2 = st.columns(2)
    
    with c1:
        st.markdown("### 🚗 Old Tech (Pre-2014)")
        st.warning("Respiratory Stress: HIGH [92%]")
        # Здесь мы имитируем 3D-модель через график (пока нет .glb файла)
        st.image("https://img.icons8.com/plasticine/200/car--v1.png") # Заглушка
        st.write("**Eco-Levy Cost:** $15/Day")
        
    with c2:
        st.markdown("### 🔋 Hybrid/Electric")
        st.success("Respiratory Relief: ACTIVE [95%]")
        st.image("https://img.icons8.com/fluency/200/electric-car.png") # Заглушка
        st.write("**Green Loan Rate:** 2.5% APR")

    st.divider()
    st.subheader("Interactive Health Impact")
    health_val = st.progress(pm_val / 250 if pm_val < 250 else 1.0)
    st.caption(f"Lung Particle Saturation: {pm_val//2}%")

# --- ВКЛАДКА 3: СТРАТЕГИЯ ---
with tab3:
    st.subheader("SROI: Social Return on Investment")
    st.write("Каждый 1 тенге, вложенный в субсидии, экономит 5.4 тенге в бюджете здравоохранения.")
    
    # График распределения средств
    fund_data = pd.DataFrame({
        'Sector': ['EV Subsidies', 'Urban Forestry', 'Infrastructure'],
        'Amount': [45, 30, 25]
    })
    fig_fund = px.pie(fund_data, values='Amount', names='Sector', hole=.3, color_discrete_sequence=px.colors.sequential.Teal)
    fig_fund.update_layout(template="plotly_dark")
    st.plotly_chart(fig_fund)
