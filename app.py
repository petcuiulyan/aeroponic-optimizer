import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as patches

st.set_page_config(page_title="Aeroponic Pro Configurator", layout="wide")

st.title("📐 Optimizare Dinamică: Magistrală Centrală per Pereche")

# --- SIDEBAR: VARIABILE DE CONTROL ---
st.sidebar.header("📏 Dimensiuni Seră")
L_SERA = st.sidebar.number_input("Lungime Totală (m)", value=12.0)
W_SERA = st.sidebar.number_input("Lățime Totală (m)", value=6.0)
L_ZONA_LUCRU = st.sidebar.number_input("Zonă Tehnică / Germinare (m)", value=2.0)

st.sidebar.header("⚙️ Distanțe Variabile (m)")
dist_x = st.sidebar.slider("Distanță între turnuri pe aceeasi linie (X)", 0.2, 0.8, 0.4)
dist_y_pereche = st.sidebar.slider("Distanță între linii (Y) - spațiu magistrală", 0.5, 0.9, 0.6)
CULOAR_CENTRAL = st.sidebar.slider("Lățime Culoar Central (m)", 1.0, 2.0, 1.5)

D_BAZIN = 0.67

# --- LOGICA MATEMATICĂ ---
L_UTILA = L_SERA - L_ZONA_LUCRU
# Pasul pe lungime: diametru + spațiul variabil ales
pas_x = D_BAZIN + dist_x
nr_turnuri_lungime = int(L_UTILA / pas_x)

# Calculăm dacă încap cele 2 perechi pe lățime (W)
# Structura: [Turn-SpațiuMagistrală-Turn] -- Culoar -- [Turn-SpațiuMagistrală-Turn]
latime_pereche = (D_BAZIN * 2) + dist_y_pereche
latime_totala_necesara = (latime_pereche * 2) + CULOAR_CENTRAL

total_turnuri = nr_turnuri_lungime * 4
total_plante = total_turnuri * 40

# --- VIZUALIZARE ---
def generate_dynamic_map():
    fig, ax = plt.subplots(figsize=(14, 7))
    
    # 1. Contur Seră & Zonă Tehnică
    ax.add_patch(patches.Rectangle((0, 0), L_SERA, W_SERA, linewidth=3, edgecolor='black', facecolor='none'))
    ax.add_patch(patches.Rectangle((0, 0), L_ZONA_LUCRU, W_SERA, alpha=0.1, facecolor='blue'))
    ax.text(L_ZONA_LUCRU/2, W_SERA/2, "ZONA\nTEHNICĂ", ha='center', fontweight='bold')

    # 2. Culoar Central (Vizual)
    ax.add_patch(patches.Rectangle((L_ZONA_LUCRU, W_SERA/2 - CULOAR_CENTRAL/2), L_SERA - L_ZONA_LUCRU, CULOAR_CENTRAL, alpha=0.05, facecolor='orange'))

    # 3. Calcul Poziții Y (Centrate pe culoar)
    # Perechea de Jos
    y1 = (W_SERA / 2) - (CULOAR_CENTRAL / 2) - D_BAZIN
    y2 = y1 - dist_y_pereche - D_BAZIN
    
    # Perechea de Sus
    y3 = (W_SERA / 2) + (CULOAR_CENTRAL / 2)
    y4 = y3 + dist_y_pereche + D_BAZIN

    y_linii = [y1, y2, y3, y4]

    # 4. Desenare Turnuri și Magistrale
    for i in range(nr_turnuri_lungime):
        x_pos = L_ZONA_LUCRU + (i * pas_x)
        
        for y in y_linii:
            # Turn
            ax.add_patch(plt.Circle((x_pos + D_BAZIN/2, y + D_BAZIN/2), D_BAZIN/2, color='#2ecc71', ec='darkgreen', alpha=0.8))
        
        # Linie de cotă între turnuri (X)
        if i == 0:
            ax.plot([x_pos + D_BAZIN, x_pos + pas_x], [y1 + D_BAZIN/2, y1 + D_BAZIN/2], color='red', lw=1)
            ax.text(x_pos + D_BAZIN + dist_x/2, y1 + D_BAZIN/2 + 0.1, f"{dist_x}m", color='red', fontsize=8, ha='center')

    # 5. Magistrale Apă/Curent (Prin mijlocul perechilor)
    # Magistrala Jos
    mag_y_jos = y1 - (dist_y_pereche / 2)
    ax.plot([L_ZONA_LUCRU, L_SERA], [mag_y_jos, mag_y_jos], color='blue', lw=2, linestyle='--', label='Magistrală Apă/Curent')
    ax.text(L_SERA - 0.5, mag_y_jos + 0.1, f"Magistrală (Gap: {dist_y_pereche}m)", color='blue', fontsize=7, ha='right')
    
    # Magistrala Sus
    mag_y_sus = y3 + D_BAZIN + (dist_y_pereche / 2)
    ax.plot([L_ZONA_LUCRU, L_SERA], [mag_y_sus, mag_y_sus], color='blue', lw=2, linestyle='--')

    # Ajustări grafic
    ax.set_xlim(-0.5, L_SERA + 0.5)
    ax.set_ylim(-0.5, W_SERA + 0.5)
    ax.set_aspect('equal')
    ax.grid(True, which='both', linestyle=':', alpha=0.3)
    plt.title(f"Configurație: {total_turnuri} Turnuri | Pas X: {round(pas_x, 2)}m | Spațiu Magistrală: {dist_y_pereche}m")
    
    return fig

# --- UI INTERFACE ---
col_map, col_stats = st.columns([3, 1])

with col_map:
    st.pyplot(generate_dynamic_map())

with col_stats:
    st.subheader("📊 Rezultate")
    st.metric("Total Turnuri", total_turnuri)
    st.metric("Total Răsaduri", total_plante)
    st.write(f"**Turnuri pe rând:** {nr_turnuri_lungime}")
    st.write(f"**Lățime necesară:** {round(latime_totala_necesara, 2)} m")
    
    if latime_totala_necesara > W_SERA:
        st.error("⚠️ Atenție: Configurația depășește lățimea serei!")
    else:
        st.success("✅ Configurația încape în spațiu.")

st.divider()

# --- TABEL PIESE ---
st.subheader("📦 Lista de materiale optimizată")
df_piese = pd.DataFrame({
    "Articol": ["Turnuri Aeroponice", "Plante (Răsaduri)", "Magistrală Ø25", "Electrovalve", "Senzori EC/pH", "Cablaj ESP32"],
    "Cantitate": [total_turnuri, total_plante, f"2 x {round(L_UTILA, 1)} m", f"{nr_turnuri_lungime * 2} buc", "1 buc (IBC1)", f"~{total_turnuri * 2} m"],
    "Rol": ["Producție", "Biomasă", "Alimentare rânduri", "Control udare pereche", "Monitorizare nutrienți", "Senzori + Valve"]
})
st.table(df_piese)
