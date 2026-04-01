import streamlit as st
import distributie_turnuri as dist

st.set_page_config(layout="wide")

L = st.sidebar.number_input("Lungime Seră (m)", value=20.0)
W = st.sidebar.number_input("Lățime Seră (m)", value=12.0)
L_T = st.sidebar.number_input("Zonă Tehnică (m)", value=2.5)

D_BAZIN = 0.67
dist_x = st.sidebar.slider("Spațiu între turnuri pe lungime (m)", 0.2, 0.6, 0.33)
dist_y = st.sidebar.slider("Spațiu între rânduri pereche (m)", 0.4, 0.8, 0.5)
culoar_min = st.sidebar.slider("Culoar minim de trecere (m)", 1.0, 2.0, 1.2)

PAS_X = D_BAZIN + dist_x
L_UTILA = L - L_T

# Calcul Cascadă
nr_x, y_positions, magistrale_y, total_t = dist.calculeaza_layout(L_UTILA, W, PAS_X, D_BAZIN, dist_y, culoar_min)

# Afișare
st.header(f"🚀 Configurație Maximă Detectată: {total_t} Turnuri")
fig = dist.randeaza_2d(L, W, L_T, nr_x, y_positions, magistrale_y, PAS_X, D_BAZIN, total_t)
st.pyplot(fig)

# Statistici
st.write(f"S-au instalat **{len(y_positions)} rânduri** de turnuri.")
st.info(f"Capacitate totală plante: **{total_t * 40}** (la 40 plante/turn)")
