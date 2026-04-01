import streamlit as st
import distributie_turnuri as dist
import automatizare as auto

st.set_page_config(layout="wide", page_title="Sistem Aeroponic v2.0")

# --- INITIALIZARE SESSION STATE ---
if 'active_auto' not in st.session_state:
    st.session_state.active_auto = False

# --- SIDEBAR ---
st.sidebar.title("🍀 Control Panel")
pagina = st.sidebar.radio("Navigare:", ["📐 Layout Seră", "🤖 Automatizare Live"])

L = st.sidebar.number_input("Lungime (m)", value=20.0)
W = st.sidebar.number_input("Lățime (m)", value=11.0)
dist_x = st.sidebar.slider("Spațiu X (m)", 0.1, 0.6, 0.33)
dist_y = st.sidebar.slider("Spațiu Y (m)", 0.1, 0.8, 0.5)
culoar_min = st.sidebar.slider("Culoar (m)", 0.8, 2.0, 1.2)

# Calcule Layout
L_T = 2.5
D_B = 0.67
nr_x, y_pos, mag_y, total_t = dist.calculeaza_layout(L-L_T, W, D_B+dist_x, D_B, dist_y, culoar_min)

if pagina == "📐 Layout Seră":
    st.header(f"Plan Distribuție: {total_t} Turnuri")
    fig = dist.randeaza_2d(L, W, L_T, nr_x, y_pos, mag_y, D_B+dist_x, D_B, dist_y, total_t, culoar_min)
    st.pyplot(fig)

else:
    st.header("🤖 Măsurători Live & Ajustare Automată")
    
    # 1. MASURATORI LIVE
    c1, c2, c3, c4 = st.columns(4)
    ph_live = c1.number_input("pH Senzor", value=7.2, step=0.1)
    ec_live = c2.number_input("EC Senzor", value=0.8, step=0.1)
    c3.metric("Temp. Apă", "23°C")
    c4.metric("Nivel IBC 2", "60%")

    st.divider()

    # 2. LIMITE & START
    s1, s2, s3 = st.columns([2, 2, 1])
    ph_lim = s1.slider("Limite pH", 4.0, 9.0, (5.9, 6.5))
    ec_lim = s2.slider("Limite EC", 0.5, 3.0, (1.1, 1.6))
    
    if s3.button("🚀 START AJUSTARE", use_container_width=True): st.session_state.active_auto = True
    if s3.button("🛑 STOP", use_container_width=True): st.session_state.active_auto = False

    # 3. LOGICA
    inst = auto.AutomatizareSera()
    mesaje, status_pompe = inst.proceseaza_automat(ph_live, ec_live, ph_lim, ec_lim, st.session_state.active_auto)

    st.divider()

    # 4. AFISARE POMPE & MANUAL OVERWRITE
    cols = st.columns(5)
    for i, (nume, stare_auto) in enumerate(status_pompe.items()):
        with cols[i]:
            st.write(f"**{nume}**")
            manual = st.checkbox("Manual ON", key=f"m_{nume}")
            
            # Culoare status
            if st.session_state.active_auto:
                color = "#2ecc71" if stare_auto else "#bdc3c7"
                txt = "AUTO ON" if stare_auto else "IDLE"
            else:
                color = "#e67e22" if manual else "#bdc3c7"
                txt = "MANUAL" if manual else "OFF"
            
            st.markdown(f"<div style='background:{color}; color:white; padding:10px; border-radius:5px; text-align:center;'>{txt}</div>", unsafe_allow_html=True)

    for m in mesaje: st.write(f"• {m}")
