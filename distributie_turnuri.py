import matplotlib.pyplot as plt
import matplotlib.patches as patches

def calculeaza_layout(L_utila, pas_x):
    nr_x = int(L_utila / pas_x)
    return nr_x, nr_x * 4

def randeaza_2d(L_sera, W_sera, L_tech, nr_x, pas_x, dist_y, D_bazin, culoar):
    fig, ax = plt.subplots(figsize=(14, 8))
    
    # --- 1. CONTUR SERĂ ---
    ax.add_patch(patches.Rectangle((0, 0), L_sera, W_sera, lw=3, ec='black', fc='none'))
    
    # --- 2. ZONA TEHNICĂ (IBC-URI REPOZIȚIONATE) ---
    ax.add_patch(patches.Rectangle((0, 0), L_tech, W_sera, alpha=0.05, fc='gray'))
    
    ibc_size = 1.0
    # IBC 2 la limita inferioară (jos)
    y_ibc2 = 0.5 
    # IBC 1 la ~1m deasupra lui IBC 2
    y_ibc1 = y_ibc2 + ibc_size + 1.0
    
    # Desenare IBC 2 (Stocare/Retur)
    ax.add_patch(patches.Rectangle((0.2, y_ibc2), ibc_size, ibc_size, fc='#a2d2ff', ec='blue', lw=2))
    ax.text(0.7, y_ibc2 + 0.5, "IBC 2\n(STOCK/RETUR)", ha='center', fontsize=8, fontweight='bold')
    
    # Desenare IBC 1 (Preparare)
    ax.add_patch(patches.Rectangle((0.2, y_ibc1), ibc_size, ibc_size, fc='#a2d2ff', ec='blue', lw=2))
    ax.text(0.7, y_ibc1 + 0.5, "IBC 1\n(PREP)", ha='center', fontsize=8, fontweight='bold')

    # POMPA TRANSFER (Vertical între ele)
    ax.plot([0.7, 0.7], [y_ibc1, y_ibc2 + ibc_size], color='darkblue', lw=2, ls=':')
    ax.plot(0.7, (y_ibc1 + y_ibc2 + ibc_size)/2, 'go', markersize=7)

    # POMPA HPA (Lângă IBC 2)
    p_main_x, p_main_y = L_tech - 0.4, y_ibc2 + 0.5
    ax.plot(p_main_x, p_main_y, 'ro', markersize=12)
    ax.text(p_main_x, p_main_y - 0.4, "POMPA HPA", ha='center', color='red', fontsize=8, fontweight='bold')
    
    # Conexiune IBC 2 -> Pompă
    ax.plot([0.2 + ibc_size, p_main_x], [y_ibc2 + 0.5, p_main_y], color='blue', lw=2)

    # --- 3. CONFIGURARE RÂNDURI ---
    y_jos_ext = (W_sera / 2) - (culoar / 2) - D_bazin - dist_y - D_bazin
    y_jos_int = (W_sera / 2) - (culoar / 2) - D_bazin
    y_sus_int = (W_sera / 2) + (culoar / 2)
    y_sus_ext = (W_sera / 2) + (culoar / 2) + D_bazin + dist_y
    
    mag_y_jos = y_jos_int - (dist_y / 2)
    mag_y_sus = y_sus_int + D_bazin + (dist_y / 2)

    # ALIMENTARE (Traseu curat de la pompă la rânduri)
    ax.plot([p_main_x, p_main_x, L_tech], [p_main_y, mag_y_jos, mag_y_jos], color='blue', lw=2.5)
    ax.plot([p_main_x, p_main_x, L_tech], [p_main_y, mag_y_sus, mag_y_sus], color='blue', lw=2.5)

    # --- 4. TURNURI ---
    for i in range(nr_x):
        x_pos = L_tech + (i * pas_x) + 0.2
        for idx, y in enumerate([y_jos_ext, y_jos_int, y_sus_int, y_sus_ext]):
            ax.add_patch(plt.Circle((x_pos + D_bazin/2, y + D_bazin/2), D_bazin/2, color='#2ecc71', alpha=0.6))
            t_mag_y = mag_y_jos if idx < 2 else mag_y_sus
            ax.plot([x_pos + D_bazin/2, x_pos + D_bazin/2], [y + D_bazin/2, t_mag_y], color='blue', lw=0.5, alpha=0.3)

    # MAGISTRALELE ORIZONTALE
    ax.plot([L_tech, L_sera - 0.5], [mag_y_jos, mag_y_jos], color='blue', lw=2.5)
    ax.plot([L_tech, L_sera - 0.5], [mag_y_sus, mag_y_sus], color='blue', lw=2.5)

    # --- 5. CIRCUIT RETUR PRIN PARTEA DE JOS ---
    # Colector final (vertical dreapta)
    ax.plot([L_sera - 0.5, L_sera - 0.5], [mag_y_sus, 0.2], color='cyan', lw=2)
    # Magistrala de retur (orizontal jos)
    ax.plot([L_sera - 0.5, 0.7], [0.2, 0.2], color='cyan', lw=2, ls='--', label='Retur Recirculare')
    # Intrare în IBC 2 (vertical stânga)
    ax.plot([0.7, 0.7], [0.2, y_ibc2], color='cyan', lw=2, ls='--')
    
    ax.text(L_sera/2, 0.35, "CONDUCTĂ RETUR (COLECTARE)", ha='center', fontsize=7, color='darkcyan', fontweight='bold')

    # --- 6. FINALIZARE ---
    ax.set_aspect('equal')
    ax.set_xlim(-0.5, L_sera + 0.5)
    ax.set_ylim(-0.5, W_sera + 0.5)
    ax.legend(loc='upper right', fontsize='x-small')
    return fig
