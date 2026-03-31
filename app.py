import streamlit as st
import distributie_turnuri as dist

st.set_page_config(layout="wide")

# SIDEBAR - Parametrii tăi variabili
st.sidebar.header("📏 Configurație Generală")
L = st.sidebar.number_input("Lungime Seră", value=12.0)
W = st.sidebar.number_input("Lățime Seră", value=6.0)
L_T = st.sidebar.number_input("Zonă Tehnică", value=2.0)

st.sidebar.header("📐 Distanțe Optimizare")
dist_x = st.sidebar.slider("Distanță între turnuri (X)", 0.2, 0.6, 0.4)
dist_y = st.sidebar.slider("Spațiu Magistrală (Y)", 0.4, 0.8, 0.6)
culoar = st.sidebar.slider("Culoar Central", 1.0, 2.0, 1.5)

D_BAZIN = 0.67
PAS_X = D_BAZIN + dist_x

# LOGICA
L_UTILA = L - L_T
nr_x, total_t = dist.calculeaza_layout(L_UTILA, PAS_X)

# AFIȘARE
st.header("🗺️ Layout 2D Detaliat")
fig = dist.randeaza_2d(L, W, L_T, nr_x, PAS_X, dist_y, D_BAZIN, culoar)
st.pyplot(fig)

st.success(f"Configurație generată: {nr_x} coloane x 4 rânduri = {total_t} turnuri.")
