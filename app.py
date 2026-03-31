import streamlit as st
import pandas as pd

st.set_page_config(page_title="Optimizator Sera Aeroponica", layout="wide")

st.title("🌱 Aeroponic Space & Hardware Optimizer")
st.markdown("Instrument de proiectare pentru sisteme de înaltă presiune (HPA)")

# --- SIDEBAR: INPUT DATE SERA ---
st.sidebar.header("Dimensiuni Seră (metri)")
L = st.sidebar.number_input("Lungime Seră (m)", min_value=1.0, value=10.0)
W = st.sidebar.number_input("Lățime Seră (m)", min_value=1.0, value=5.0)
H = st.sidebar.number_input("Înălțime Seră (m)", min_value=1.0, value=3.0)

st.sidebar.header("Configurație Module")
mod_l = st.sidebar.slider("Lungime Modul (m)", 0.5, 5.0, 2.0)
mod_w = st.sidebar.slider("Lățime Modul (m)", 0.3, 2.0, 0.6)
culoar = st.sidebar.slider("Lățime Culoar Acces (m)", 0.4, 1.5, 0.8)

# --- LOGICA DE CALCUL ---
# Calculăm câte rânduri și coloane de module încap
nr_randuri = int(W / (mod_w + culoar))
nr_module_per_rand = int(L / mod_l)
total_module = nr_randuri * nr_module_per_rand

# Parametri Aeroponici (Standard: 4 duze pe metru liniar de modul)
duze_per_modul = int(mod_l * 2) # presupunem două linii de pulverizare
total_duze = total_module * duze_per_modul
debit_duza_lpm = 0.065 # litri pe minut la 70 PSI
debit_total_necesar = total_duze * debit_duza_lpm

# --- INTERFAȚA REZULTATE ---
col1, col2, col3 = st.columns(3)
col1.metric("Total Module", total_module)
col2.metric("Total Duze", total_duze)
col3.metric("Debit Pompă Necesar", f"{round(debit_total_necesar, 2)} LPM")

st.divider()

# --- GENERARE LISTĂ DE PIESE (BOM) ---
st.subheader("📦 Listă Automată de Piese (BOM)")

piese = {
    "Categorie": ["Hidraulică", "Hidraulică", "Hidraulică", "Structură", "Senzori", "Senzori", "Control"],
    "Articol": [
        "Pompă Diagrafmă Înaltă Presiune (70-100 PSI)",
        "Duze Ceață (Misting Nozzles) 0.3mm",
        "Țeavă Polietilenă/PPR (metri liniari)",
        "Profile Aluminiu/PVC Susținere",
        "Senzor Presiune (Pressure Switch)",
        "Senzori Umiditate/Temp (DHT22)",
        "Controller ESP32 + Modul Relee"
    ],
    "Cantitate": [
        1 if debit_total_necesar < 5 else 2,
        total_duze,
        round((total_module * mod_l) * 1.2, 1), # +20% rezervă
        total_module,
        1,
        max(2, int(total_module / 4)),
        1
    ],
    "Unitate": ["buc", "buc", "m", "set", "buc", "buc", "set"]
}

df_piese = pd.DataFrame(piese)
st.table(df_piese)

# --- ANALIZĂ ENERGETICĂ ---
st.subheader("💡 Estimare Consum Lumini (LED)")
putere_led_mp = 150 # wați per mp pentru creștere intensă
suprafata_utila = total_module * (mod_l * mod_w)
consum_total_led = suprafata_utila * putere_led_mp
st.info(f"Putere instalată estimată pentru iluminat: {round(consum_total_led / 1000, 2)} kW")
