import streamlit as st
import distributie_turnuri as dist
import automatizare as auto
import nutrienti as nutr
import configuratie_sera as conf

st.set_page_config(layout="wide", page_title="Greenhouse Control Center")

# --- STATE ---
if 'active_auto' not in st.session_state: st.session_state.active_auto = False

# --- SIDEBAR ---
st.sidebar.title("🍀 Control Panel")
pagina = st.sidebar.radio("Navigare:", ["📐 Proiectare & Layout", "🤖 Automatizare & Nutrienți"])

L = st.sidebar.number_input("Lungime Seră (m)", value=20.0)
W = st.sidebar.number_input("Lățime Seră (m)", value=11.0)
dist_x = st.sidebar.slider("Spațiu între turnuri (m)", 0.1, 0.6, 0.33)
dist_y = st.sidebar.slider("Spațiu între rânduri (m)", 0.1, 0.8, 0.5)
culoar_min = st.sidebar.slider("Culoar minim (m)", 0.8, 2.0, 1.2)

# Calcule Fundamentale
L_T = 2.5
D_B = 0.67
L_U = L - L_T
nr_x, y_pos, mag_y, total_t = dist.calculeaza_layout(L_U, W, D_B+dist_x, D_B, dist_y, culoar_min)
dim = conf.get_dimensiuni_sera(L, W, 4.0, L_T)

if pagina == "📐 Proiectare & Layout":
    st.header(f"Plan Tehnic: {total_t} Turnuri ({total_t*40} plante)")
    fig = dist.randeaza_2d(L, W, L_T, nr_x, y_pos, mag_y, D_B+dist_x, D_B, dist_y, total_t, culoar_min)
    st.pyplot(fig)
    st.json(dim)

else:
    st.header("🤖 Monitorizare Live & Dozare Preciză (700L Workload)")
    
    # 1. LIVE DATA
    c1, c2, c3, c4 = st.columns(4)
    ph_live = c1.number_input("📡 pH Actual", value=7.2, step=0.1)
    ec_live = c2.number_input("📡 EC Actual", value=0.8, step=0.1)
    c3.metric("Volum Apă", "700 L", delta="-300L Buffer")
    c4.metric("Status Sistem", "ACTIV" if st.session_state.active_auto else "OFF")

    # 2. SETARE LIMITE
    st.divider()
    s1, s2, s3 = st.columns([2, 2, 1])
    ph_lim = s1.slider("Interval pH", 4.0, 9.0, (5.9, 6.5))
    ec_lim = s2.slider("Interval EC", 0.5, 3.0, (1.1, 1.6))
    
    if s3.button("🚀 START AJUSTARE", use_container_width=True): st.session_state.active_auto = True
    if s3.button("🛑 STOP", use_container_width=True): st.session_state.active_auto = False

    # 3. MATEMATICA NUTRIENTI & LOGICA
    timpi = nutr.calculeaza_dozare_precisa(ph_live, ec_live, ph_lim, ec_lim, 700)
    stari = auto.AutomatizareSera().actualizeaza_stari(timpi, st.session_state.active_auto)

    # 4. AFISARE ACTUATORI
    st.subheader("⚙️ Stare Relee & Timpi Execuție")
    cols = st.columns(5)
    nume_afisaj = ["Peristaltică A", "Peristaltică B", "Peristaltică pH UP", "Peristaltică pH DOWN", "Pompă 120W"]
    chei_timp = ["A", "B", "p_UP", "p_DOWN", "Pompă 120W"]

    for i, nume in enumerate(nume_afisaj):
        with cols[i]:
            st.write(f"**{nume}**")
            manual = st.checkbox("Manual", key=f"man_{nume}")
            t_exec = timpi.get(chei_timp[i], 0.0) if i < 4 else 0.0
            
            st_auto = stari.get(nume, False)
            color = "#2ecc71" if (st_auto or manual) else "#bdc3c7"
            label = f"ON ({t_exec}s)" if st_auto else ("MANUAL" if manual else "OFF")
            
            st.markdown(f"<div style='background:{color}; color:white; padding:10px; border-radius:5px; text-align:center; font-weight:bold;'>{label}</div>", unsafe_allow_html=True)

    if st.session_state.active_auto:
        st.info(f"💡 Algoritmul a calculat o dozare de siguranță de 30% din deficit pentru a menține stabilitatea la 700L.")
