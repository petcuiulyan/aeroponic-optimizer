# app.py
import streamlit as st
import configuratie_sera as cfg
import distributie_turnuri as dist
import nutrienti as nut
import automatizare as auto

st.set_page_config(page_title="Master Aeroponic Control", layout="wide")

# --- INPUTURI GENERALE ---
st.sidebar.header("⚙️ Configurare Generală")
L = st.sidebar.number_input("Lungime Seră", value=12.0)
W = st.sidebar.number_input("Lățime Seră", value=6.0)
L_T = st.sidebar.number_input("Zonă Tehnică", value=2.0)

# --- CALCUL LOGIC ÎN CASCADĂ ---
dim = cfg.get_dimensiuni_sera(L, W, 3.0, L_T)
nr_x, y_pos = dist.calcul_pozitii(dim["L_utila"], W, L_T, 1.0, 0.6, 0.67, 1.5)
total_t = nr_x * 4
hidraulica = nut.calcul_hidraulic(total_t, dim["L_utila"])
electronica = auto_necesar = auto.necesar_senzori(total_t)

# --- INTERFAȚĂ TABURI ---
tab1, tab2, tab3, tab4 = st.tabs(["📐 Layout 2D", "💧 Sistem Nutrienți", "🔌 Automatizare", "❄️ Climatizare"])

with tab1:
    fig = dist.randeaza_2d(L, W, L_T, nr_x, y_pos, 0.67, 1.0, 1.5)
    st.pyplot(fig)
    st.metric("Total Turnuri", total_t)

with tab2:
    st.write(f"Necesari {hidraulica['ibc_count']} IBC-uri de 1000L.")
    st.write(f"Debit pompă minim: {hidraulica['debit_pompa_recomandat']} LPM")

with tab3:
    st.write(f"Electrovalve necesare: {electronica['electrovalve']}")
    st.write(f"Puncte de monitorizare ESP32: {electronica['esp32_count']}")
