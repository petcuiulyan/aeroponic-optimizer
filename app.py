import streamlit as st
import distributie_turnuri as dist

st.set_page_config(layout="wide")

st.sidebar.header("📏 Configurație Seră")
L = st.sidebar.number_input("Lungime Seră", value=20.0)
W = st.sidebar.number_input("Lățime Seră", value=12.0)
L_T = st.sidebar.number_input("Zonă Tehnică", value=2.5)

st.sidebar.header("📐 Parametri Turn")
D_BAZIN = 0.67
dist_x = st.sidebar.slider("Distanță X între turnuri", 0.2, 0.6, 0.33)
dist_y = st.sidebar.slider("Spațiu Magistrală (Y)", 0.4, 0.8, 0.5)
culoar_min = st.sidebar.slider("Culoar MINIM de lucru (m)", 1.2, 2.5, 1.5)

PAS_X = D_BAZIN + dist_x

# LOGICA SMART ITERATIVĂ
L_UTILA = L - L_T
nr_x, y_positions, magistrale_y, total_t = dist.calculeaza_layout(L_UTILA, W, PAS_X, D_BAZIN, dist_y, culoar_min)

# AFIȘARE
st.header(f"🗺️ Layout Smart Automat: {total_t} Turnuri")
fig = dist.randeaza_2d(L, W, L_T, nr_x, y_positions, magistrale_y, PAS_X, D_BAZIN, total_t)
st.pyplot(fig)

st.success(f"Configurația generată automat: {len(y_positions)} rânduri. Numărul de rânduri a crescut dinamic pe lățimea de {W}m.")
