import streamlit as st
import matplotlib.pyplot as plt
import logging

# Local imports
import distributie_turnuri as dist
import automatizare as auto
import nutrienti as nutr
import configuratie_sera as conf
import materiale_necesare as mat
import config
import utils

# Setup logging
logger = logging.getLogger(__name__)

# ===== PAGE CONFIGURATION =====
st.set_page_config(
    layout="wide",
    page_title="Aeroponic Optimizer Pro v2.1",
    page_icon="🌿"
)

# ===== SESSION STATE INITIALIZATION =====
utils.initialize_session_state()

# ===== SIDEBAR - INPUT PARAMETERS =====
st.sidebar.title("🍀 Control Proiect")
pagina = st.sidebar.radio(
    "Navigare:",
    ["📐 Layout & Proiectare", "🤖 Automatizare Live", "🛒 Listă Materiale"]
)

st.sidebar.divider()

# Greenhouse dimensions
L = st.sidebar.number_input(
    "Lungime totală seră (m)",
    value=config.DEFAULT_DIMENSIONS["length"],
    step=0.5,
    min_value=0.1
)
W = st.sidebar.number_input(
    "Lățime totală seră (m)",
    value=config.DEFAULT_DIMENSIONS["width"],
    step=0.5,
    min_value=0.1
)
H = st.sidebar.number_input(
    "Înălțime seră (m)",
    value=config.DEFAULT_DIMENSIONS["height"],
    step=0.1,
    min_value=0.1
)

# Validate dimensions
if not utils.validate_greenhouse_params(L, W, H):
    st.stop()

# Tower configuration
st.sidebar.subheader("Configurație Turnuri")
dist_x = st.sidebar.slider(
    "Spațiu între turnuri pe X (m)",
    config.SPACING_RANGES["dist_x"]["min"],
    config.SPACING_RANGES["dist_x"]["max"],
    config.SPACING_RANGES["dist_x"]["default"]
)
dist_y = st.sidebar.slider(
    "Spațiu între turnuri pe rând (m)",
    config.SPACING_RANGES["dist_y"]["min"],
    config.SPACING_RANGES["dist_y"]["max"],
    config.SPACING_RANGES["dist_y"]["default"]
)
culoar_min = st.sidebar.slider(
    "Lățime culoar lucru (m)",
    config.SPACING_RANGES["corridor"]["min"],
    config.SPACING_RANGES["corridor"]["max"],
    config.SPACING_RANGES["corridor"]["default"]
)

# ===== GLOBAL LAYOUT CALCULATIONS =====
L_TECH = config.DEFAULT_DIMENSIONS["tech_zone"]
D_BAZIN = config.DEFAULT_DIMENSIONS["basin_diameter"]
L_UTILA = L - L_TECH

nr_x, y_pos, mag_y, total_t = dist.calculeaza_layout(
    L_UTILA, W, D_BAZIN + dist_x, D_BAZIN, dist_y, culoar_min
)

# ===== PAGE RENDERING FUNCTIONS =====

def render_layout_page():
    """Render layout & design page"""
    st.header(f"📐 Plan Tehnic Distribuție: {total_t} Turnuri")
    
    # Render graphics
    fig = dist.randeaza_2d(
        L, W, L_TECH, nr_x, y_pos, mag_y,
        D_BAZIN + dist_x, D_BAZIN, dist_y,
        total_t, culoar_min
    )
    st.pyplot(fig)
    plt.close(fig)  # Free memory
    
    # Technical info panel
    st.divider()
    c1, c2, c3 = st.columns(3)
    
    dim_sera = conf.get_dimensiuni_sera(L, W, H, L_TECH)
    hidraulica = nutr.calcul_hidraulic(total_t, L_UTILA)
    so_value = conf.calcul_so(L, W)
    
    with c1:
        st.subheader("📊 Capacitate")
        st.write(f"• Total plante: **{total_t * config.PLANTS_PER_TOWER}**")
        st.write(f"• Turnuri: **{total_t}**")
        st.write(f"• Germinare: **{conf.zona_germinare(total_t, L_TECH, W)} tăvi**")
        st.write(f"• SO (Producție Specifică): **{so_value:.2f}**")
    
    with c2:
        st.subheader("🏠 Volum & Suprafață")
        st.write(f"• Volum aer: **{dim_sera['volum']:.1f} m³**")
        st.write(f"• Suprafață utilă: **{dim_sera['suprafata_utila']:.1f} m²**")
    
    with c3:
        st.subheader("💧 Hidraulică")
        st.write(f"• Magistrale: **{len(mag_y)} linii**")
        st.write(f"• Debit pompă: **{hidraulica['debit_pompa_recomandat']:.2f} LPM**")


def render_automation_page():
    """Render automation control page"""
    st.header("🤖 Control Automatizare (700L)")
    
    # Live sensor inputs
    col1, col2, col3 = st.columns(3)
    ph_live = col1.number_input(
        "📡 pH Actual",
        value=config.PH_EC_DEFAULTS["ph_live"],
        step=0.1,
        min_value=0.0,
        max_value=14.0
    )
    ec_live = col2.number_input(
        "📡 EC Actual",
        value=config.PH_EC_DEFAULTS["ec_live"],
        step=0.1,
        min_value=0.0
    )
    
    status_text = "✅ ACTIV" if st.session_state.active_auto else "🔴 OPRIT"
    col3.metric("Status Sistem", status_text)
    
    st.divider()
    
    # Target parameters and controls
    s1, s2, s3 = st.columns([2, 2, 1])
    ph_target = s1.slider(
        "Interval pH",
        config.PH_EC_DEFAULTS["ph_range"]["min"],
        config.PH_EC_DEFAULTS["ph_range"]["max"],
        config.PH_EC_DEFAULTS["ph_target"]
    )
    ec_target = s2.slider(
        "Interval EC",
        config.PH_EC_DEFAULTS["ec_range"]["min"],
        config.PH_EC_DEFAULTS["ec_range"]["max"],
        config.PH_EC_DEFAULTS["ec_target"]
    )
    
    col_btn1, col_btn2 = s3.columns(2)
    if col_btn1.button("🚀 START", use_container_width=True):
        st.session_state.active_auto = True
        utils.log_system_event("info", "Sistem automat pornit")
        st.rerun()
    
    if col_btn2.button("🛑 STOP", use_container_width=True):
        st.session_state.active_auto = False
        utils.log_system_event("info", "Sistem automat oprit")
        st.rerun()
    
    # Process automation logic
    inst_auto = auto.AutomatizareSera()
    timpi = nutr.calculeaza_dozare_precisa(
        ph_live, ec_live, ph_target, ec_target,
        config.PH_EC_DEFAULTS["tank_volume"]
    )
    stari_relee = inst_auto.actualizeaza_stari(timpi, st.session_state.active_auto)
    
    # Display relay status
    st.subheader("⚙️ Status Relee")
    cols = st.columns(len(stari_relee))
    for i, (nume, activ) in enumerate(stari_relee.items()):
        color = config.COLOR_SCHEME["active"] if activ else config.COLOR_SCHEME["inactive"]
        cols[i].markdown(
            f"<div style='background:{color};color:white;padding:10px;border-radius:5px;text-align:center;font-weight:bold;'>{nume}</div>",
            unsafe_allow_html=True
        )


def render_materials_page():
    """Render materials list & purchase page"""
    st.header("🛒 Deviz Materiale și Ajustări Manuale")
    st.info("ℹ️ Ajustează cantitățile pentru fiecare componentă după necesități.")
    
    # Calculate initial bill
    deviz_calc = mat.calculeaza_deviz_detaliat(total_t, len(mag_y), L, W, H)
    deviz_final = {}
    
    # Organize in 2 columns
    col_m1, col_m2 = st.columns(2)
    columns = [col_m1, col_m2]
    
    for idx, (cat, items) in enumerate(deviz_calc.items()):
        target_col = columns[idx % 2]
        with target_col.expander(f"📦 {cat}", expanded=True):
            deviz_final[cat] = {}
            for piesa, cant_init in items.items():
                ajustata = st.number_input(
                    piesa,
                    value=float(cant_init),
                    step=1.0,
                    key=f"adj_{cat}_{piesa}"
                )
                deviz_final[cat][piesa] = ajustata
    
    st.divider()
    
    # Generate documentation
    st.subheader("📄 Generare Documentație Finală")
    continut_txt = mat.genereaza_text_specificatii(deviz_final, total_t, L, W, H)
    st.download_button(
        label="📥 DESCARCĂ LISTA ACTUALIZATĂ (.txt)",
        data=continut_txt,
        file_name=f"deviz_sera_{total_t}turnuri.txt",
        mime="text/plain",
        use_container_width=True
    )


# ===== PAGE ROUTING =====
if pagina == "📐 Layout & Proiectare":
    render_layout_page()
elif pagina == "🤖 Automatizare Live":
    render_automation_page()
elif pagina == "🛒 Listă Materiale":
    render_materials_page()
