import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as patches

st.set_page_config(page_title="Aeroponic Pro Designer", layout="wide")

st.title("🌱 Optimizator Seră: Culoar Central & Distribuție Laterală")

# --- SIDEBAR: PARAMETRI ---
st.sidebar.header("📏 Dimensiuni Seră")
L_SERA = st.sidebar.number_input("Lungime Seră (m)", value=12.0)
W_SERA = st.sidebar.number_input("Lățime Seră (m)", value=6.0)

st.sidebar.header("🏗️ Zona Tehnică (Intrare)")
L_ZONA_LUCRU = st.sidebar.slider("Lungime zonă tehnică (m)", 1.5, 5.0, 2.5)

st.sidebar.header("📐 Specificații Turn")
D_BAZIN = 0.67 
CULOAR_CENTRAL = 1.5
DIST_INTRE_TURNURI_Y = 0.7 # Distanța în cadrul perechii (pe verticală în desen)

# --- LOGICA DE CALCUL OPTIMIZATĂ ---
L_UTILA = L_SERA - L_ZONA_LUCRU

# Calculăm câte turnuri încap pe lungime (cu un buffer de 0.1m între ele ca să nu se atingă)
nr_turnuri_lungime = int(L_UTILA / (D_BAZIN + 0.1))

# Calculăm dispunerea pe lățime (2 rânduri de perechi, cu culoar pe mijloc)
# Rând Sus: Pereche de 2 turnuri
# CULOAR CENTRAL
# Rând Jos: Pereche de 2 turnuri
total_turnuri = nr_turnuri_lungime * 4 

# --- GENERARE VIZUALIZARE ---
def generate_greenhouse_map():
    fig, ax = plt.subplots(figsize=(12, 6))
    
    # Contur Seră
    ax.add_patch(patches.Rectangle((0, 0), L_SERA, W_SERA, linewidth=2, edgecolor='black', facecolor='none'))
    
    # Zona Tehnică
    ax.add_patch(patches.Rectangle((0, 0), L_ZONA_LUCRU, W_SERA, linewidth=1, edgecolor='gray', facecolor='#f0f0f0', hatch='/'))
    ax.text(L_ZONA_LUCRU/2, W_SERA/2, "ZONA TEHNICĂ", ha='center', va='center', rotation=90)

    # Coordonate Y pentru rânduri (împinse spre margini)
    # Rândul de jos (pereche 1 și 2)
    y_rand_jos_1 = 0.4
    y_rand_jos_2 = y_rand_jos_1 + D_BAZIN + 0.2
    
    # Rândul de sus (pereche 3 și 4)
    y_rand_sus_2 = W_SERA - 0.4 - D_BAZIN
    y_rand_sus_1 = y_rand_sus_2 - D_BAZIN - 0.2

    # Desenare Turnuri
    for i in range(nr_turnuri_lungime):
        x = L_ZONA_LUCRU + 0.2 + i * (D_BAZIN + 0.1)
        
        # Verificare limită lungime
        if x + D_BAZIN > L_SERA: break
            
        # Turnuri Jos
        ax.add_patch(plt.Circle((x + D_BAZIN/2, y_rand_jos_1 + D_BAZIN/2), D_BAZIN/2, color='#2ecc71'))
        ax.add_patch(plt.Circle((x + D_BAZIN/2, y_rand_jos_2 + D_BAZIN/2), D_BAZIN/2, color='#2ecc71'))
        
        # Turnuri Sus
        ax.add_patch(plt.Circle((x + D_BAZIN/2, y_rand_sus_1 + D_BAZIN/2), D_BAZIN/2, color='#2ecc71'))
        ax.add_patch(plt.Circle((x + D_BAZIN/2, y_rand_sus_2 + D_BAZIN/2), D_BAZIN/2, color='#2ecc71'))

    # Magistrale laterale (Linii albastre de apă)
    ax.plot([L_ZONA_LUCRU, L_SERA], [y_rand_jos_1 - 0.2, y_rand_jos_1 - 0.2], color='blue', linewidth=2, label='Magistrală Apă')
    ax.plot([L_ZONA_LUCRU, L_SERA], [y_rand_sus_2 + D_BAZIN + 0.2, y_rand_sus_2 + D_BAZIN + 0.2], color='blue', linewidth=2)

    # Culoar Central (Săgeată)
    ax.annotate('', xy=(L_SERA, W_SERA/2), xytext=(L_ZONA_LUCRU, W_SERA/2),
                arrowprops=dict(arrowstyle='<->', color='orange', lw=3))
    ax.text((L_ZONA_LUCRU + L_SERA)/2, W_SERA/2 + 0.2, "CULOAR CENTRAL (1.5m)", ha='center', color='orange', fontweight='bold')

    ax.set_xlim(-0.5, L_SERA + 0.5)
    ax.set_ylim(-0.5, W_SERA + 0.5)
    ax.set_aspect('equal')
    return fig

# --- UI ---
col1, col2 = st.columns([3, 1])
with col1:
    st.pyplot(generate_greenhouse_map())

with col2:
    st.metric("Total Turnuri", nr_turnuri_lungime * 4)
    st.metric("Total Plante", nr_turnuri_lungime * 4 * 40)
    st.success(f"Configurație: 4 rânduri de câte {nr_turnuri_lungime} turnuri")

st.subheader("📦 Necesar Materiale Corectat")
piese = {
    "Articol": ["Turnuri 10 niv", "Plante", "Magistrală Apă Laterală", "Electrovalve", "Senzori"],
    "Cantitate": [nr_turnuri_lungime * 4, nr_turnuri_lungime * 4 * 40, f"2 x {round(L_UTILA, 1)}m", nr_turnuri_lungime * 2, "1 Set ESP32"]
}
st.table(pd.DataFrame(piese))
