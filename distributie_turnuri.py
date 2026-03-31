import matplotlib.pyplot as plt
import matplotlib.patches as patches

def calculeaza_layout(L_utila, pas_x):
    nr_x = int(L_utila / pas_x)
    return nr_x, nr_x * 4

def randeaza_2d(L_sera, W_sera, L_tech, nr_x, pas_x, dist_y, D_bazin, culoar):
    fig, ax = plt.subplots(figsize=(14, 7))
    
    # --- 1. CONTUR & ZONĂ TEHNICĂ ---
    ax.add_patch(patches.Rectangle((0, 0), L_sera, W_sera, lw=3, ec='black', fc='none'))
    ax.add_patch(patches.Rectangle((0, 0), L_tech, W_sera, alpha=0.15, fc='gray', hatch='//'))

    # --- 2. CALCUL COORDONATE Y ---
    y_jos_ext = (W_sera / 2) - (culoar / 2) - D_bazin - dist_y - D_bazin
    y_jos_int = (W_sera / 2) - (culoar / 2) - D_bazin
    y_sus_int = (W_sera / 2) + (culoar / 2)
    y_sus_ext = (W_sera / 2) + (culoar / 2) + D_bazin + dist_y

    mag_y_jos = y_jos_int - (dist_y / 2)
    mag_y_sus = y_sus_int + D_bazin + (dist_y / 2)

    # --- 3. DESENARE ELECTROVALVE (O singură pereche la intrare) ---
    # Desenăm un "X" sau un pătrat roșu la începutul magistralei
    ax.plot(L_tech, mag_y_jos, 'rs', markersize=10, label='Electrovalvă Generală')
    ax.plot(L_tech, mag_y_sus, 'rs', markersize=10)
    ax.text(L_tech, mag_y_jos - 0.3, "VALVĂ 1", color='red', fontweight='bold', ha='center')
    ax.text(L_tech, mag_y_sus + 0.3, "VALVĂ 2", color='red', fontweight='bold', ha='center')

    # --- 4. DESENARE TURNURI ȘI DERIVAȚII ---
    for i in range(nr_x):
        x_pos = L_tech + (i * pas_x) + 0.1
        
        # Desenăm turnurile pe cele 4 rânduri
        y_positions = [y_jos_ext, y_jos_int, y_sus_int, y_sus_ext]
        
        for idx, y in enumerate(y_positions):
            # Turnul
            ax.add_patch(plt.Circle((x_pos + D_bazin/2, y + D_bazin/2), D_bazin/2, 
                                color='#2ecc71', ec='darkgreen', lw=1, alpha=0.8))
            
            # Derivație apă (Linie subțire de la magistrală la centrul turnului)
            target_mag_y = mag_y_jos if idx < 2 else mag_y_sus
            ax.plot([x_pos + D_bazin/2, x_pos + D_bazin/2], [y + D_bazin/2, target_mag_y], 
                    color='blue', lw=0.8, alpha=0.5)

    # --- 5. MAGISTRALELE PRINCIPALE ---
    ax.plot([L_tech, L_sera], [mag_y_jos, mag_y_jos], color='blue', lw=3, ls='-', alpha=0.8)
    ax.plot([L_tech, L_sera], [mag_y_sus, mag_y_sus], color='blue', lw=3, ls='-', alpha=0.8)

    # --- 6. CULOAR & GRID ---
    ax.add_patch(patches.Rectangle((L_tech, W_sera/2 - culoar/2), L_sera - L_tech, culoar, alpha=0.05, fc='orange'))
    ax.set_aspect('equal')
    ax.grid(True, linestyle=':', alpha=0.3)
    
    plt.legend(loc='upper right')
    return fig
