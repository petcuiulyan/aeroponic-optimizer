import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as patches

st.set_page_config(page_title="Aeroponic Precision Optimizer", layout="wide")

st.title("📐 Optimizare Exactă: 10 Turnuri / Linie")

# --- SIDEBAR ---
st.sidebar.header("📏 Configurație Seră")
L_SERA = st.sidebar.number_input("Lungime Totală Seră (m)", value=12.0)
W_SERA = st.sidebar.number_input("Lățime Totală Seră (m)", value=6.0)
L_ZONA_LUCRU = st.sidebar.number_input("Lungime Zonă Tehnică (m)", value=2.0)

st.sidebar.header("⚙️ Setări Turn (Calcul Fix)")
D_BAZIN = 0.67
SPATIU_MINIM = 0.33 # Spațiul care completează până la 1 metru
PAS_TURN = D_BAZIN + SPATIU_MINIM # Rezultă fix 1.0m

# --- LOGICA MATEMATICĂ ---
L_UTILA = L_SERA - L_ZONA_LUCRU
# Calculăm numărul de turnuri pe lungime (strict)
nr_turnuri_lungime = int(L_UTILA / PAS_TURN)

# Avem 4 linii de turnuri conform schiței tale (două perechi cu culoar între ele)
total_turnuri = nr_turnuri_lungime * 4
total_plante = total_turnuri * 40

# --- VIZUALIZARE ---
def generate_exact_map():
    fig, ax = plt.subplots(figsize=(14, 7))
    
    # 1. Contur Seră
    ax.add_patch(patches.Rectangle((0, 0), L_SERA, W_SERA, linewidth=3, edgecolor='black', facecolor='none'))
    
    # 2. Zona Tehnică (2m)
    ax.add_patch(patches.Rectangle((0, 0), L_ZONA_LUCRU, W_SERA, alpha=0.2, facecolor='red', label='Zonă Tehnică'))
    ax.text(L_ZONA_LUCRU/2, W_SERA/2, f"ZONA TEHNICĂ\n{L_ZONA_LUCRU}m", ha='center', va='center', fontweight='bold')

    # 3. Culoar Central (1.5m)
    ax.add_patch(patches.Rectangle((L_ZONA_LUCRU, (W_SERA/2 - 0.75)), L_SERA - L_ZONA_LUCRU, 1.5, alpha=0.1, facecolor='orange'))
    ax.text(L_SERA - 1, W_SERA/2, "CULOAR 1.5m", color='orange', fontweight='bold', ha='right')

    # 4. Poziționare Rânduri (Y)
    # Rândurile sunt grupate câte două lângă pereți
    distanta_perete = 0.4
    y_pos = [
        distanta_perete, 
        distanta_perete + D_BAZIN + 0.3, # Grupul de jos
        W_SERA - distanta_perete - D_BAZIN - 0.3 - D_BAZIN, # Grupul de sus
        W_SERA - distanta_perete - D_BAZIN # Grupul de sus
    ]

    # 5. Desenare Turnuri
    for i in range(nr_turnuri_lungime):
        x_center = L_ZONA_LUCRU + (i * PAS_TURN) + (D_BAZIN / 2)
        
        # Desenăm pe cele 4 rânduri
        for y in y_pos:
            circle = plt.Circle((x_center, y + D_BAZIN/2), D_BAZIN/2, color='#2ecc71', ec='black', lw=1)
            ax.add_patch(circle)
            
        # Adăugăm cota de 1 metru la primul element
        if i == 0:
            ax.annotate('', xy=(L_ZONA_LUCRU, -0.3), xytext=(L_ZONA_LUCRU + PAS_TURN, -0.3),
                        arrowprops=dict(arrowstyle='<->'))
            ax.text(L_ZONA_LUCRU + 0.5, -0.6, "Pas 1.0m\n(0.67+0.33)", ha='center', fontsize=9)

    # 6. Magistrale (Linii Apă)
    ax.plot([L_ZONA_LUCRU, L_SERA], [distanta_perete/2, distanta_perete/2], color='blue', lw=3, label='Magistrală Laterală')
    ax.plot([L_ZONA_LUCRU, L_SERA], [W_SERA - distanta_perete/2, W_SERA - distanta_perete/2], color='blue', lw=3)

    # Setări axă
    ax.set_xticks(range(int(L_SERA) + 1))
    ax.set_yticks(range(int(W_SERA) + 1))
    ax.grid(True, linestyle=':', alpha=0.5)
    ax.set_aspect('equal')
    plt.title(f"Plan de Amplasament: {nr_turnuri_lungime} Turnuri/Linie | Total: {total_turnuri} Turnuri", fontsize=14)
    
    return fig

# --- AFIȘARE REZULTATE ---
c1, c2 = st.columns([3, 1])

with c1:
    st.pyplot(generate_exact_map())

with c2:
    st.subheader("📊 Date Proiect")
    st.metric("Lungime Utilă", f"{L_UTILA} m")
    st.metric("Turnuri / Linie", nr_turnuri_lungime)
    st.metric("Total Turnuri", total_turnuri)
    st.metric("Total Plante", total_plante)
    
    st.divider()
    st.info(f"Fiecare linie de {L_UTILA}m este acum optimizată pentru un pas de fix {PAS_TURN}m.")

st.subheader("📦 Listă Materiale (BOM)")
df_bom = pd.DataFrame({
    "Articol": ["Turnuri Hidroponice", "Răsaduri necesare", "Magistrală Principală", "Cablaj Senzori (estimat)", "Electrovalve"],
    "Cantitate": [total_turnuri, total_plante, f"2 x {L_UTILA}m", f"{L_SERA * 2}m", nr_turnuri_lungime * 2],
    "Observații": ["10 nivele/turn", "40 plante/turn", "Amplasată lateral", "Conexiune ESP32", "1 per pereche turnuri"]
})
st.table(df_bom)
