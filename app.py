import streamlit as st
import matplotlib.pyplot as plt
import distributie_turnuri as dist
import automatizare as auto
import nutrienti as nutr
import configuratie_sera as conf
import materiale_necesare as mat

# Configurare pagină
st.set_page_config(layout="wide", page_title="Aeroponic Optimizer Pro v2.0", page_icon="🌿")

# --- INITIALIZARE SESSION STATE ---
if 'active_auto' not in st.session_state:
    st.session_state.active_auto = False

# --- SIDEBAR: PARAMETRI DE INTRARE ---
st.sidebar.title("🍀 Setări Seră")
pagina = st.sidebar.radio("Navigare:", ["📐 Layout & Proiectare", "🤖 Automatizare Live", "🛒 Listă Materiale"])

st.sidebar.divider()
L = st.sidebar.number_input("Lungime totală seră (m)", value=20.0, step=0.5)
W = st.sidebar.number_input("Lățime totală seră (m)", value=11.0, step=0.5)
H = st.sidebar.number_input("Înălțime seră (m)", value=4.0, step=0.1)

st.sidebar.subheader("Configurație Turnuri")
dist_x = st.sidebar.slider("Spațiu între turnuri pe X (m)", 0.1, 0.6, 0.33)
dist_y = st.sidebar.slider("Spațiu între turnuri pe rând (m)", 0.1, 0.8, 0.5)
culoar_min = st.sidebar.slider("Lățime culoar lucru (m)", 0.8, 2.0, 1.2)

# --- CALCULE DE BAZĂ (PENTRU TOATE PAGINILE) ---
L_TECH = 2.5    # Zona rezervată IBC-urilor și panoului
D_BAZIN = 0.67  # Diametrul bazei turnului
L_UTILA = L - L_TECH

# Calcul layout folosind modulul avansat
nr_x, y_pos, mag_y, total_t = dist.calculeaza_layout(
    L_UTILA, W, D_BAZIN + dist_x, D_BAZIN, dist_y, culoar_min
)

# --- LOGICĂ PAGINI ---

if pagina == "📐 Layout & Proiectare":
    st.header(f"Plan Tehnic Distribuție: {total_t} Turnuri")
    
    # Afișare Grafică Detaliată (include IBC, Pompe, Retur)
    fig = dist.randeaza_2d(L, W, L_TECH, nr_x, y_pos, mag_y, D_BAZIN + dist_x, D_BAZIN, dist_y, total_t, culoar_min)
    st.pyplot(fig)
    
    # Informații Tehnice sub grafic
    st.divider()
    c1, c2, c3 = st.columns(3)
    dim_sera = conf.get_dimensiuni_sera(L, W, H, L_TECH)
    hidraulica = nutr.calcul_hidraulic(total_t, L_UTILA)
    
    with c1:
        st.subheader("📊 Capacitate")
        st.write(f"• Total plante: **{total_t * 40}**")
        st.write(f"• Turnuri: **{total_t}**")
        st.write(f"• Germinare: **{conf.zona_germinare(L_TECH, W)} tăvi**")
    
    with c2:
        st.subheader("🏠 Volum & Suprafață")
        st.write(f"• Volum aer: **{dim_sera['volum']:.1f} m³**")
        st.write(f"• Suprafață utilă: **{dim_sera['suprafata_utila']:.1f} m²**")
        
    with c3:
        st.subheader("💧 Sistem Hidraulic")
        st.write(f"• Magistrale active: **{len(mag_y)} linii**")
        st.write(f"• Debit necesar: **{hidraulica['debit_pompa_recomandat']:.2f} LPM**")

elif pagina == "🤖 Automatizare Live":
    st.header("🤖 Monitorizare și Dozare Preciză (700L)")
    
    col_senzor1, col_senzor2, col_senzor3, col_senzor4 = st.columns(4)
    ph_live = col_senzor1.number_input("📡 pH Actual", value=7.2, step=0.1)
    ec_live = col_senzor2.number_input("📡 EC Actual (mS/cm)", value=0.8, step=0.1)
    col_senzor3.metric("Volum Apă IBC", "700 L", "-300L Siguranță")
    col_senzor4.metric("Status Sistem", "ACTIV" if st.session_state.active_auto else "OFF")

    st.divider()

    s1, s2, s3 = st.columns([2, 2, 1])
    ph_target = s1.slider("Interval pH Dorit", 4.0, 9.0, (5.9, 6.5))
    ec_target = s2.slider("Interval EC Dorit", 0.5, 3.0, (1.2, 1.6))
    
    if s3.button("🚀 PORNEȘTE SISTEMUL", use_container_width=True): 
        st.session_state.active_auto = True
        st.rerun()
    if s3.button("🛑 OPRIRE URGENȚĂ", use_container_width=True): 
        st.session_state.active_auto = False
        st.rerun()

    inst_auto = auto.AutomatizareSera()
    timpi_calculati = nutr.calculeaza_dozare_precisa(ph_live, ec_live, ph_target, ec_target, 700)
    stari_relee = inst_auto.actualizeaza_stari(timpi_calculati, st.session_state.active_auto)
    mesaje, _ = inst_auto.proceseaza_automat(ph_live, ec_live, ph_target, ec_target, st.session_state.active_auto)

    st.subheader("⚙️ Status Relee (HPA & Peristaltice)")
    cols_act = st.columns(5)
    nume_relee = list(stari_relee.keys())
    
    for i, nume in enumerate(nume_relee):
        with cols_act[i]:
            activ = stari_relee[nume]
            t_exec = timpi_calculati.get(nume, 0.0)
            color = "#2ecc71" if activ else "#bdc3c7"
            # Etichetă dinamică: dacă e peristaltică și e activă, arată timpul
            label = f"ON ({t_exec}s)" if activ and t_exec > 0 else ("ACTIVE" if activ else "OFF")
            
            st.markdown(f"""
                <div style="background-color:{color}; color:white; padding:15px; 
                border-radius:10px; text-align:center; font-weight:bold;">
                {nume}<br>{label}
                </div>
                """, unsafe_allow_html=True)

    st.write("")
    for msg in mesaje:
        st.info(f"ℹ️ {msg}")

elif pagina == "🛒 Listă Materiale":
    st.header("🛒 Deviz General Materiale & Specificații")
    
    # Calcul deviz folosind funcția corectă cu 5 parametri (L, W, H, total_t, nr_mag)
    nr_mag = len(mag_y)
    deviz = mat.calculeaza_deviz_detaliat(total_t, nr_mag, L, W, H)
    
    # --- BUTON DOWNLOAD PROIECT ---
    st.subheader("📄 Export Documentație")
    # Generăm textul folosind toți parametrii necesari
    doc_txt = mat.genereaza_text_specificatii(deviz, total_t, L, W, H)
    
    st.download_button(
        label="📥 DESCARCĂ LISTA DE ACHIZIȚII (.txt)",
        data=doc_txt,
        file_name=f"plan_achizitii_sera_{total_t}turnuri.txt",
        mime="text/plain",
        use_container_width=True
    )
    
    st.divider()

    # Afișare pe coloane pentru lizibilitate maximă
    col_a, col_b = st.columns(2)
    categorii = list(deviz.keys())
    
    for i, cat in enumerate(categorii):
        # Distribuim categoriile egal pe cele două coloane
        target_col = col_a if i % 2 == 0 else col_b
        with target_col.expander(f"📦 {cat}", expanded=True):
            # Creăm un tabel simulat pentru claritate
            for nume, cant in deviz[cat].items():
                c_nume, c_val = st.columns([3, 1])
                c_nume.write(f"🔹 {nume}")
                c_val.write(f"**{cant}**")
    
    st.info("💡 **Sfat Tehnic:** Cantitățile de folie și cabluri includ o marjă de siguranță pentru montaj. Verificați conexiunile IP55 înainte de punerea sub tensiune a pompelor.")
