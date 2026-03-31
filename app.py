import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as patches
 
# Configurare pagină
st.set_page_config(page_title="Aeroponic Pro Designer", layout="wide")

st.title("🌱 Proiectant Vizual Seră Aeroponică (HPA)")
st.markdown("Bazat pe unitatea logică: **Pereche de 2 turnuri cu magistrală centrală**")

# --- SIDEBAR: PARAMETRI TEHNICI ---
st.sidebar.header("📏 Dimensiuni Seră")
L_SERA = st.sidebar.number_input("Lungime Seră (m)", value=12.0)
W_SERA = st.sidebar.number_input("Lățime Seră (m)", value=6.0)

st.sidebar.header("🏗️ Zona de Lucru (Intrare)")
L_ZONA_LUCRU = st.sidebar.slider("Lungime zonă tehnică (m)", 1.5, 5.0, 2.5)

st.sidebar.header("📐 Parametri Turnuri")
D_BAZIN = 0.67 
DIST_INTRE_PERECHE = 0.7 # Spațiul dintre cele 2 turnuri din desen
LATIME_CULOAR = 1.5      # Culoar trecere

# --- LOGICA DE CALCUL ---
L_UTILA = L_SERA - L_ZONA_LUCRU
latime_unitate = (D_BAZIN * 2) + DIST_INTRE_PERECHE

# Calcul rânduri și coloane
nr_randuri = int((W_SERA) / (latime_unitate + 0.2)) # 0.2 buffer margini
nr_perechi_per_rand = int(L_UTILA / (D_BAZIN + 0.2))
total_turnuri = nr_randuri * nr_perechi_per_rand * 2

# --- GENERARE VIZUALIZARE (Matplotlib) ---
def generate_greenhouse_map():
    fig, ax = plt.subplots(figsize=(12, 8))
    
    # Contur Seră
    sera = patches.Rectangle((0, 0), L_SERA, W_SERA, linewidth=2, edgecolor='black', facecolor='none', label='Contur Seră')
    ax.add_patch(sera)
    
    # Zona de Lucru (Germinare + IBC)
    zona_lucru = patches.Rectangle((0, 0), L_ZONA_LUCRU, W_SERA, linewidth=1, edgecolor='gray', facecolor='#f0f0f0', hatch='/')
    ax.add_patch(zona_lucru)
    ax.text(L_ZONA_LUCRU/2, W_SERA/2, "ZONA TEHNICĂ\n(IBC 1 & 2, Germinare)", ha='center', va='center', fontweight='bold')

    # Desenare Turnuri și Magistrale
    current_x = L_ZONA_LUCRU + 0.5
    for c in range(nr_perechi_per_rand):
        current_y = 0.5
        for r in range(nr_randuri):
            # Centrul celor două turnuri
            y1 = current_y + D_BAZIN/2
            y2 = y1 + DIST_INTRE_PERECHE + D_BAZIN
            
            # Turn 1
            t1 = plt.Circle((current_x + D_BAZIN/2, y1), D_BAZIN/2, color='#2ecc71', alpha=0.7)
            # Turn 2
            t2 = plt.Circle((current_x + D_BAZIN/2, y2), D_BAZIN/2, color='#2ecc71', alpha=0.7)
            
            ax.add_patch(t1)
            ax.add_patch(t2)
            
            # Magistrala de apă (Linia albastră între ele)
            ax.plot([current_x - 0.2, current_x + D_BAZIN + 0.2], [y1 + (y2-y1)/2, y1 + (y2-y1)/2], color='blue', linewidth=1.5, linestyle='--')
            
            current_y += latime_unitate + 0.3
        current_x += D_BAZIN + 0.4

    ax.set_xlim(-1, L_SERA + 1)
    ax.set_ylim(-1, W_SERA + 1)
    ax.set_aspect('equal')
    plt.title(f"Configurație Optimizată: {total_turnuri} Turnuri")
    return fig

# --- AFIȘARE ÎN STREAMLIT ---
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("🗺️ Planimetrică Seră (Vedere de sus)")
    st.pyplot(generate_greenhouse_map())

with col2:
    st.subheader("📋 Sumar Proiect")
    st.metric("Total Turnuri", total_turnuri)
    st.metric("Capacitate Plante (10 niv/turn)", total_turnuri * 10 * 4) # Presupunem 4 plante/nivel
    st.info(f"Spațiu rămas culoar: {round(W_SERA - (nr_randuri * latime_unitate), 2)}m")

st.divider()

# --- LISTA DE PIESE (BOM) ---
st.subheader("📦 Listă Necesar Materiale")
data_piese = {
    "Componentă": [
        "Turnuri Aeroponice 2.21m", "Electrovalve (1 per pereche)", "Pompă Presiune 20 Bar",
        "Rezervor IBC 1000L (Nutrienți)", "Rezervor IBC 1000L (Apă/Agitator)", 
        "Țeavă Magistrală Ø25 (m)", "Țeavă Derivație Ø16 (m)", "Senzor pH/EC/Temp",
        "Controller ESP32 Central", "Senzor Nivel Apă (Ultrasonic)"
    ],
    "Cantitate": [
        total_turnuri, int(total_turnuri/2), 1, 
        1, 1, 
        round(nr_randuri * L_UTILA, 1), round(total_turnuri * 0.8, 1), 1,
        1, 2
    ]
}
st.table(pd.DataFrame(data_piese))
