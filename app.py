import streamlit as st
import distributie_turnuri as dist
import automatizare as auto

st.set_page_config(layout="wide", page_title="HPA/LPA Greenhouse Optimizer")

# --- MENIU NAVIGARE ---
st.sidebar.title("🎮 Panou Control")
pagina = st.sidebar.radio("Selectează Vizualizarea:", ["📐 Proiectare Seră (Layout)", "🤖 Sistem Automatizare (Control)"])

# --- PARAMETRI GLOBALI (Sidebar) ---
st.sidebar.divider()
L = st.sidebar.number_input("Lungime Seră (m)", value=20.0)
W = st.sidebar.number_input("Lățime Seră (m)", value=11.0)
L_T = st.sidebar.number_input("Zonă Tehnică (m)", value=2.5)

# Calcule Distribuție (necesare în ambele pagini pentru date)
D_BAZIN = 0.67
dist_x = st.sidebar.slider("Spațiu între turnuri X (m)", 0.2, 0.6, 0.33)
dist_y = st.sidebar.slider("Spațiu între rânduri Y (m)", 0.4, 0.8, 0.5)
culoar_min = st.sidebar.slider("Culoar minim trecere (m)", 1.0, 2.0, 1.2)

PAS_X = D_BAZIN + dist_x
L_UTILA = L - L_T
nr_x, y_positions, magistrale_y, total_t = dist.calculeaza_layout(L_UTILA, W, PAS_X, D_BAZIN, dist_y, culoar_min)

# --- LOGICA DE AFIȘARE ---
if pagina == "📐 Proiectare Seră (Layout)":
    st.header(f"📐 Plan Tehnic Distribuție: {total_t} Turnuri")
    # Apelăm funcția ta de randare cu toate cotele și denumirile
    fig = dist.randeaza_2d(L, W, L_T, nr_x, y_positions, magistrale_y, PAS_X, D_BAZIN, dist_y, total_t, culoar_min)
    st.pyplot(fig)
    
    # Statistici rapide sub grafic
    c1, c2, c3 = st.columns(3)
    c1.metric("Total Turnuri", total_t)
    c2.metric("Rânduri", len(y_positions))
    c3.metric("Capacitate Plante (max)", total_t * 40)

else:
    st.header("🤖 Control și Monitorizare Automatizare")
    
    # Simulare Senzori (Inputs)
    col_s1, col_s2, col_s3 = st.columns(3)
    with col_s1:
        ph_val = st.number_input("Citire pH (Senzor Gravity)", 0.0, 14.0, 6.5)
        temp_apa = st.number_input("Temperatură Apă (°C)", 10.0, 35.0, 22.0)
    with col_s2:
        ec_val = st.number_input("Citire EC (ms/cm)", 0.0, 5.0, 1.8)
        co2_val = st.number_input("Nivel CO2 (ppm)", 300, 2000, 800)
    with col_s3:
        nivel_ibc2 = st.slider("Nivel IBC 2 (Stock) %", 0, 100, 60)
        nivel_ibc1 = st.slider("Nivel IBC 1 (Prep) %", 0, 100, 90)

    st.divider()

    # Logica din automatizare.py
    sistem = auto.AutomatizareSera()
    logica_n = sistem.logica_dozare(ph_val, ec_val)
    
    # Afișare Relee și Pompe
    c1, c2 = st.columns([2, 1])
    
    with c1:
        st.subheader("⚡ Stare Relee (Modul 8 Canale + MOSFET)")
        grid = st.columns(4)
        relee_nume = ["Pompă 120W (Alimentare)", "El.Valvă M1", "El.Valvă M2", "Pompă Transfer", 
                      "Peristaltică A", "Peristaltică B", "pH Down", "Ventilație"]
        
        for i, nume in enumerate(relee_nume):
            grid[i % 4].toggle(nume, value=(i==0 or i==7)) # Exemplu stare

    with c2:
        st.subheader("📝 Jurnal Acțiuni")
        for msg in logica_n:
            st.warning(msg)
        if nivel_ibc2 < 20:
            st.error("🚨 ALERTĂ: IBC 2 Aproape Gol!")
