import streamlit as st
import automatizare as auto

# --- UI SIDEBAR PENTRU SENSORI (Simulare) ---
st.sidebar.header("📡 Date Senzori (Real-Time)")
ph_val = st.sidebar.number_input("Citire pH (Analog)", 0.0, 14.0, 6.8)
ec_val = st.sidebar.number_input("Citire EC (ms/cm)", 0.0, 5.0, 1.2)
temp_apa = st.sidebar.number_input("Temp Apă (DS18B20)", 10.0, 40.0, 22.5)
co2_val = st.sidebar.number_input("CO2 (ppm)", 300, 2000, 450)

# --- LOGICA DE CONTROL ---
sistem = auto.AutomatizareSera()
logica_nutritie = sistem.logica_dozare(ph_val, ec_val)
logica_mediu = sistem.monitorizare_mediu(25, 60, co2_val)

# --- AFIȘARE ÎN DASHBOARD ---
st.header("🎮 Centru de Comandă Automatizat")

c1, c2, c3 = st.columns(3)

with c1:
    st.subheader("🧪 Management Nutrienți")
    st.metric("pH", ph_val, delta=round(6.0 - ph_val, 2), delta_color="inverse")
    st.metric("EC", f"{ec_val} ms/cm")
    for msg in logica_nutritie:
        st.write(f"• {msg}")

with c2:
    st.subheader("⚡ Stare Relee (8 Ch)")
    relee = {
        "Ch1: Pompa 120W": sistem.pompa_120w,
        "Ch2: Electrovalvă M1": True,
        "Ch3: Peristaltică A": sistem.pompe_peristaltice["A"],
        "Ch4: Peristaltică B": sistem.pompe_peristaltice["B"],
        "Ch5: pH Down": sistem.pompe_peristaltice["pH_Down"],
        "Ch6: Ventilator": False,
        "Ch7: CO2 Valve": False,
        "Ch8: Lumină": True
    }
    for nume, stare in relee.items():
        st.toggle(nume, value=stare, disabled=True)

with c3:
    st.subheader("🌡️ Mediu & Siguranță")
    st.write(logica_mediu)
    st.progress(co2_val/2000, text=f"Concentrație CO2: {co2_val}ppm")
    st.info(f"Senzor IBC: {'Nivel Optim' if nivel_ibc2 > 20 else 'NECESAR TRANSFER'}")
