# app.py
import streamlit as st
import distributie_turnuri as dist
import automatizare as auto
import nutrienti as nutr
import configuratie_sera as conf

st.set_page_config(layout="wide", page_title="Sistem Aeroponic v2.0")

if 'active_auto' not in st.session_state:
    st.session_state.active_auto = False

st.sidebar.title("🍀 Control Panel")
pagina = st.sidebar.radio("Navigare:", ["📐 Layout Seră", "🤖 Automatizare Live"])

L = st.sidebar.number_input("Lungime (m)", value=20.0)
W = st.sidebar.number_input("Lățime (m)", value=11.0)
dist_x = st.sidebar.slider("Spațiu X (m)", 0.1, 0.6, 0.33)
dist_y = st.sidebar.slider("Spațiu Y (m)", 0.1, 0.8, 0.5)
culoar_min = st.sidebar.slider("Culoar (m)", 0.8, 2.0, 1.2)

# Calcule Fundamentale
L_T = 2.5
D_B = 0.67
nr_x, y_pos, mag_y, total_t = dist.calculeaza_layout(L-L_T, W, D_B+dist_x, D_B, dist_y, culoar_min)

if pagina == "📐 Layout Seră":
    st.header(f"Plan Distribuție: {total_t} Turnuri")
    fig = dist.randeaza_2d(L, W, L_T, nr_x, y_pos, mag_y, D_B+dist_x, D_B, dist_y, total_t, culoar_min)
    st.pyplot(fig)
    
    # Afișare info din configuratie_sera și nutrienti (păstrare info)
    dim = conf.get_dimensiuni_sera(L, W, 4.0, L_T)
    hidraulic = nutr.calcul_hidraulic(total_t, L-L_T)
    st.json({"Dimensiuni": dim, "Hidraulic": hidraulic})

else:
    st.header("🤖 Măsurători Live & Ajustare Automată (700L)")
    
    c1, c2, c3, c4 = st.columns(4)
    ph_live = c1.number_input("pH Senzor", value=7.2, step=0.1)
    ec_live = c2.number_input("EC Senzor", value=0.8, step=0.1)
    c3.metric("Temp. Apă", "23°C")
    c4.metric("Volum Lucru", "700 L")

    st.divider()

    s1, s2, s3 = st.columns([2, 2, 1])
    ph_lim = s1.slider("Limite pH", 4.0, 9.0, (5.9, 6.5))
    ec_lim = s2.slider("Limite EC", 0.5, 3.0, (1.1, 1.6))
    
    if s3.button("🚀 START AJUSTARE", use_container_width=True): st.session_state.active_auto = True
    if s3.button("🛑 STOP", use_container_width=True): st.session_state.active_auto = False

    # LOGICA INTEGRATA
    inst_auto = auto.AutomatizareSera()
    # Calculăm timpii preciși din nutrienti.py (700L)
    timpi_dozare = nutr.calculeaza_dozare_precisa(ph_live, ec_live, ph_lim, ec_lim, 700)
    # Actualizăm stările pompelor în automatizare.py
    stari = inst_auto.actualizeaza_stari(timpi_dozare, st.session_state.active_auto)
    mesaje, _ = inst_auto.proceseaza_automat(ph_live, ec_live, ph_lim, ec_lim, st.session_state.active_auto)

    st.divider()

    cols = st.columns(5)
    for i, (nume, stare_activa) in enumerate(stari.items()):
        with cols[i]:
            st.write(f"**{nume}**")
            manual = st.checkbox("Manual", key=f"m_{nume}")
            t_exec = timpi_dozare.get(nume, 0.0)
            
            color = "#2ecc71" if (stare_activa or manual) else "#bdc3c7"
            label = f"ON ({t_exec}s)" if stare_activa else ("MANUAL" if manual else "OFF")
            st.markdown(f"<div style='background:{color}; color:white; padding:10px; border-radius:5px; text-align:center;'>{label}</div>", unsafe_allow_html=True)

    for m in mesaje: st.write(f"• {m}")
