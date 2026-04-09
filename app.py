import streamlit as st
import matplotlib.pyplot as plt
import distributie_turnuri as dist
import automatizare as auto
import nutrienti as nutr
import configuratie_sera as conf
import materiale_necesare as mat

# 1. Configurare Pagină
st.set_page_config(layout="wide", page_title="Aeroponic Optimizer Pro v2.1", page_icon="🌿")

# 2. Inițializare State (Păstrăm starea automatizării și a modificărilor manuale)
if 'active_auto' not in st.session_state:
    st.session_state.active_auto = False
if 'ajustari_manuale' not in st.session_state:
    st.session_state.ajustari_manuale = {}

# 3. Sidebar - Parametri de Intrare
st.sidebar.title("🍀 Control Proiect")
pagina = st.sidebar.radio("Navigare:", ["📐 Layout & Proiectare", "🤖 Automatizare Live", "🛒 Listă Materiale"])

st.sidebar.divider()
L = st.sidebar.number_input("Lungime totală seră (m)", value=20.0, step=0.5)
W = st.sidebar.number_input("Lățime totală seră (m)", value=11.0, step=0.5)
H = st.sidebar.number_input("Înălțime seră (m)", value=4.0, step=0.1)

st.sidebar.subheader("Configurație Turnuri")
dist_x = st.sidebar.slider("Spațiu între turnuri pe X (m)", 0.1, 0.6, 0.33)
dist_y = st.sidebar.slider("Spațiu între turnuri pe rând (m)", 0.1, 0.8, 0.5)
culoar_min = st.sidebar.slider("Lățime culoar lucru (m)", 0.8, 2.0, 1.2)

# 4. Calcule Globale (Layout)
L_TECH = 2.5
D_BAZIN = 0.67
L_UTILA = L - L_TECH
nr_x, y_pos, mag_y, total_t = dist.calculeaza_layout(L_UTILA, W, D_BAZIN + dist_x, D_BAZIN, dist_y, culoar_min)

# --- LOGICĂ PAGINI ---

if pagina == "📐 Layout & Proiectare":
    st.header(f"📐 Plan Tehnic Distribuție: {total_t} Turnuri")
    
    # Randare Grafică
    fig = dist.randeaza_2d(L, W, L_TECH, nr_x, y_pos, mag_y, D_BAZIN + dist_x, D_BAZIN, dist_y, total_t, culoar_min)
    st.pyplot(fig)
    
    # Info Panou Tehnic
    st.divider()
    c1, c2, c3 = st.columns(3)
    dim_sera = conf.get_dimensiuni_sera(L, W, H, L_TECH)
    hidraulica = nutr.calcul_hidraulic(total_t, L_UTILA)
    
    with c1:
        st.subheader("📊 Capacitate")
        st.write(f"• Total plante: **{total_t * 112}**")
        st.write(f"• Turnuri: **{total_t}**")
        st.write(f"• Germinare: **{conf.zona_germinare(total_t, L_TECH, W)} tăvi**")
    with c2:
        st.subheader("🏠 Volum & Suprafață")
        st.write(f"• Volum aer: **{dim_sera['volum']:.1f} m³**")
        st.write(f"• Suprafață utilă: **{dim_sera['suprafata_utila']:.1f} m²**")
    with c3:
        st.subheader("💧 Hidraulică")
        st.write(f"• Magistrale: **{len(mag_y)} linii**")
        st.write(f"• Debit pompă: **{hidraulica['debit_pompa_recomandat']:.2f} LPM**")

elif pagina == "🤖 Automatizare Live":
    st.header("🤖 Control Automatizare (700L)")
    
    col1, col2, col3 = st.columns(3)
    ph_live = col1.number_input("📡 pH Actual", value=7.2, step=0.1)
    ec_live = col2.number_input("📡 EC Actual", value=0.8, step=0.1)
    status_text = "ACTIV" if st.session_state.active_auto else "SISTEM OPRIT"
    col3.metric("Status Sistem", status_text)

    st.divider()
    s1, s2, s3 = st.columns([2, 2, 1])
    ph_target = s1.slider("Interval pH", 4.0, 9.0, (5.9, 6.5))
    ec_target = s2.slider("Interval EC", 0.5, 3.0, (1.2, 1.6))
    
    if s3.button("🚀 START", use_container_width=True): 
        st.session_state.active_auto = True
        st.rerun()
    if s3.button("🛑 STOP", use_container_width=True): 
        st.session_state.active_auto = False
        st.rerun()

    # Logica de procesare
    inst_auto = auto.AutomatizareSera()
    timpi = nutr.calculeaza_dozare_precisa(ph_live, ec_live, ph_target, ec_target, 700)
    stari_relee = inst_auto.actualizeaza_stari(timpi, st.session_state.active_auto)
    
    st.subheader("⚙️ Status Relee")
    cols = st.columns(len(stari_relee))
    for i, (nume, activ) in enumerate(stari_relee.items()):
        color = "#2ecc71" if activ else "#bdc3c7"
        cols[i].markdown(f"<div style='background:{color};color:white;padding:10px;border-radius:5px;text-align:center;'>{nume}</div>", unsafe_allow_html=True)

elif pagina == "🛒 Listă Materiale":
    st.header("🛒 Deviz Materiale și Ajustări Manuale")
    st.info("Ajustează cantitățile folosind butoanele +/- de pe fiecare piesă.")

    # Calcul inițial din modul
    deviz_calc = mat.calculeaza_deviz_detaliat(total_t, len(mag_y), L, W, H)
    deviz_final = {}

    col_m1, col_m2 = st.columns(2)
    categorii = list(deviz_calc.keys())

    for idx, cat in enumerate(categorii):
        target = col_m1 if idx % 2 == 0 else col_m2
        with target.expander(f"📦 {cat}", expanded=True):
            deviz_final[cat] = {}
            for piesa, cant_init in deviz_calc[cat].items():
                # Buton de ajustare manuală pentru fiecare piesă
                ajustata = st.number_input(
                    f"{piesa}", 
                    value=float(cant_init), 
                    step=1.0, 
                    key=f"adj_{cat}_{piesa}"
                )
                deviz_final[cat][piesa] = ajustata

    st.divider()
    
    # Export TXT
    st.subheader("📄 Generare Documentație Finală")
    continut_txt = mat.genereaza_text_specificatii(deviz_final, total_t, L, W, H)
    st.download_button(
        label="📥 DESCARCĂ LISTA ACTUALIZATĂ (.txt)",
        data=continut_txt,
        file_name=f"deviz_sera_{total_t}turnuri.txt",
        mime="text/plain",
        use_container_width=True
    )
