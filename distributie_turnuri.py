
import matplotlib.pyplot as plt
import matplotlib.patches as patches

def calculeaza_layout(L_utila, pas_x):
    # Calculăm câte coloane de turnuri încap pe lungime
    nr_x = int(L_utila / pas_x)
    return nr_x, nr_x * 4 # 4 rânduri total

def randeaza_2d(L_sera, W_sera, L_tech, nr_x, pas_x, dist_y, D_bazin, culoar):
    fig, ax = plt.subplots(figsize=(14, 7))
    
    # --- 1. CONTUR SERĂ & ZONĂ TEHNICĂ ---
    ax.add_patch(patches.Rectangle((0, 0), L_sera, W_sera, linewidth=3, edgecolor='black', facecolor='none'))
    ax.add_patch(patches.Rectangle((0, 0), L_tech, W_sera, alpha=0.15, facecolor='gray', hatch='//'))
    ax.text(L_tech/2, W_sera/2, "ZONA TEHNICĂ\n(IBC, Germinare)", ha='center', va='center', fontweight='bold', rotation=90)

    # --- 2. CULOAR CENTRAL ---
    ax.add_patch(patches.Rectangle((L_tech, W_sera/2 - culoar/2), L_sera - L_tech, culoar, alpha=0.1, facecolor='orange'))
    ax.text(L_sera - 0.5, W_sera/2, f"CULOAR {culoar}m", color='orange', fontweight='bold', ha='right')

    # --- 3. CALCUL POZIȚII Y (Perechi cu magistrală pe mijloc) ---
    # Perechea de JOS
    y_jos_ext = (W_sera / 2) - (culoar / 2) - D_bazin - dist_y - D_bazin
    y_jos_int = (W_sera / 2) - (culoar / 2) - D_bazin
    
    # Perechea de SUS
    y_sus_int = (W_sera / 2) + (culoar / 2)
    y_sus_ext = (W_sera / 2) + (culoar / 2) + D_bazin + dist_y

    y_linii = [y_jos_ext, y_jos_int, y_sus_int, y_sus_ext]
    mag_y_jos = y_jos_int - (dist_y / 2)
    mag_y_sus = y_sus_int + D_bazin + (dist_y / 2)

    # --- 4. DESENARE TURNURI ---
    for i in range(nr_x):
        x_pos = L_tech + (i * pas_x) + 0.1 # 0.1 mic buffer de la peretele zonei tehnice
        
        for y in y_linii:
            # Turnul (bazinul)
            circle = plt.Circle((x_pos + D_bazin/2, y + D_bazin/2), D_bazin/2, 
                                color='#2ecc71', ec='darkgreen', lw=1.5, alpha=0.9)
            ax.add_patch(circle)
            # Centrul turnului (pentru precizie)
            ax.plot(x_pos + D_bazin/2, y + D_bazin/2, 'w+', markersize=4)

    # --- 5. MAGISTRALE DE APĂ/CURENT (Printre rânduri) ---
    ax.plot([L_tech, L_sera], [mag_y_jos, mag_y_jos], color='blue', lw=2.5, ls='--', label='Magistrală')
    ax.plot([L_tech, L_sera], [mag_y_sus, mag_y_sus], color='blue', lw=2.5, ls='--')

    # --- 6. COTE ȘI GRID ---
    ax.set_xticks(range(int(L_sera) + 1))
    ax.set_yticks(range(int(W_sera) + 1))
    ax.grid(True, linestyle=':', alpha=0.4)
    ax.set_aspect('equal')
    
    plt.title(f"Plan General: {nr_x * 4} Turnuri | Magistrale Centrale pe Pereche", fontsize=14, pad=20)
    return fig
