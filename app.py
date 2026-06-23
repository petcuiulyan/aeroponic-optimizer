import streamlit as st
import plotly.graph_objects as go
import numpy as np
import sys
import os

import distributie_turnuri as dist
import configuratie_sera as conf
import materiale_necesare as mat
import config

st.write("Fisiere in folder:", os.listdir())
st.set_page_config(layout="wide", page_title="Greenhouse Designer")

# ===== SIDEBAR =====

st.sidebar.title("Setări Seră")

pagina = st.sidebar.radio("Meniu", [
    "Layout & Proiectare",
    "Automatizare",
    "Materiale"
])

L = st.sidebar.number_input("Lungime (m)", value=20.0)
W = st.sidebar.number_input("Lățime (m)", value=11.0)

dist_x = st.sidebar.slider("Distanță X", 0.1, 0.6, 0.33)
dist_y = st.sidebar.slider("Distanță Y", 0.1, 0.8, 0.5)
culoar = st.sidebar.slider("Culoar", 0.8, 2.0, 1.2)

# ===== CALCULE =====

dim = conf.get_dimensiuni_sera(L, W)
H = dim["H"]
L_utila = dim["L_utila"]
D = config.DEFAULT_DIMENSIONS["basin_diameter"]

nr_x, y_pos, mag, total = dist.calculeaza_layout(
    L_utila, W, D + dist_x, D, dist_y, culoar
)

# ===== 3D =====

def sera_3d(L, W, H):
    fig = go.Figure()

    x = np.linspace(0, L, 30)

    for y in np.linspace(0, W, 6):
        z = H * np.sin(np.pi * x / L)
        fig.add_trace(go.Scatter3d(x=x, y=[y]*len(x), z=z, mode='lines'))

    fig.update_layout(margin=dict(l=0, r=0, t=0, b=0))
    return fig


# ===== PAGINI =====

if pagina == "Layout & Proiectare":

    st.title("Layout Seră")

    col1, col2 = st.columns([2, 1])

    with col1:
        fig2d = dist.randeaza_2d(L, W, dim["L_utila"], nr_x, y_pos, dist_x, D)
        st.pyplot(fig2d)

        st.markdown(f"""
        ### Dimensiuni:
        - Lungime: {L} m
        - Lățime: {W} m
        - Înălțime calculată: {H} m
        - Turnuri: {total}
        """)

    with col2:
        st.plotly_chart(sera_3d(L, W, H), use_container_width=True)

# ===== MATERIALE =====

if pagina == "Materiale":
    st.title("Materiale")

    materiale = mat.calculeaza_materiale(total, L, W, H)

    st.json(materiale)

# ===== AUTOMATIZARE =====

if pagina == "Automatizare":
    st.title("Automatizare")
    st.info("Mod automatizare în dezvoltare")
