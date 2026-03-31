import matplotlib.pyplot as plt
import matplotlib.patches as patches

def calculeaza_layout(L_utila, pas_x):
    nr_x = int(L_utila / pas_x)
    return nr_x, nr_x * 4

def randeaza_2d(L_sera, W_sera, L_tech, nr_x, pas_x, dist_y, D_bazin, culoar):
    fig, ax = plt.subplots(figsize=(14, 8))
    
    # --- 1. CONTUR SERĂ ---
    ax.add_patch(patches.Rectangle((0, 0), L_sera, W_sera, lw=3, ec='black', fc='none'))
    
    # --- 2. ZONA TEHNICĂ (DETALIATĂ) ---
    ax.add_patch(patches.Rectangle((0, 0), L_tech, W_sera, alpha=0.05, fc='gray'))
    
    # Desenare IBC-uri (pătrate de aprox 1x1m la scară)
    ibc_w, ibc_l = 1.0, 1.0
    # IBC 1 (Sus)
    ax.add_patch(patches.Rectangle((0.2, W_sera - 1.5), ibc_l, ibc_w, fc='#a2d2ff', ec='blue', lw=2, label='IBC 1 (Nutrienți)'))
    ax.text(0.7, W_sera - 1.0, "IBC 1\n(pH/EC)", ha='center', fontsize=8, fontweight='bold')
    
    # IBC 2 (Jos)
    ax.add_patch(patches.Rectangle((0.2, 0.5), ibc_l, ibc_w, fc='#a2d2ff', ec='blue', lw=2, label='IBC 2 (Agitator)'))
    ax.text(0.7, 1.0, "IBC 2\n(BUFFER)", ha='center', fontsize=8, fontweight='bold')

    # POMPA TRANSFER (Între IBC-uri)
    ax.plot([0.7, 0.7], [W_sera - 1.5, 1.5], color='darkblue', lw=2, ls=':')
    ax.plot(0.7, W_sera/2 + 0.5, 'go', markersize=8, label='Pompă Transfer')
    ax.text(0.8, W_sera/2 + 0.5, "P. Transfer", fontsize=7)

    # POMPA PRINCIPALĂ 20 BAR
    p_main_x, p_main_y = L_tech - 0.5, W_sera/2
    ax.plot(p_main_x, p_main_y, 'ro', markersize=12, label='Pompă 20 BAR')
    ax.text(p_main_x, p_main_y - 0.4, "POMPĂ\nPRINCIPALĂ", ha='center', color='red', fontsize=8, fontweight='bold')
    
    # Conexiune IBC 2 -> Pompă Principală
    ax.plot([0.7, p_main_x], [1.0, p_main_y], color='blue', lw=2)

    # --- 3. CONFIGURARE RÂNDURI TURNURI ---
    y_jos_ext = (W_sera / 2) - (culoar / 2) - D_bazin - dist_y - D_bazin
    y_jos_int = (W_sera / 2) - (culoar / 2) - D_bazin
    y_sus_int = (W_sera / 2) + (culoar / 2)
    y_sus_ext = (W_sera / 2) + (culoar / 2) + D_bazin + dist_y
    
    mag_y_jos = y_jos_int - (dist_y / 2)
    mag_y_sus = y_sus_int + D_bazin + (dist_y / 2)

    # --- 4. DISTRIBUȚIE DIN POMPĂ CĂTRE MAGISTRALE ---
    # Plecare din pompă spre cele 2 magistrale
    ax.plot([p_main_x, L_tech], [p_main_y, mag_y_jos], color='blue', lw=2)
    ax.plot([p_main_x, L_tech], [p_main_y, mag_y_sus], color='blue', lw=2)

    # ELECTROVALVE (La intrarea pe magistrale)
    ax.plot(L_tech, mag_y_jos, 'rs', markersize=8)
    ax.plot(L_tech, mag_y_sus, 'rs', markersize=8)

    # --- 5. TURNURI ȘI MAGISTRALE ---
    for i in range(nr_x):
        x_pos = L_tech + (i * pas_x) + 0.2
        for idx, y in enumerate([y_jos_ext, y_jos_int, y_sus_int, y_sus_ext]):
            ax.add_patch(plt.Circle((x_pos + D_bazin/2, y + D_bazin/2), D_bazin/2, color='#2ecc71', alpha=0.7))
            # Derivații mici
            t_mag_y = mag_y_jos if idx < 2 else mag_y_sus
            ax.plot([x_pos + D_bazin/2, x_pos + D_bazin/2], [y + D_bazin/2, t_mag_y], color='blue', lw=0.5)

    ax.plot([L_tech, L_sera], [mag_y_jos, mag_y_jos], color='blue', lw=2.5)
    ax.plot([L_tech, L_sera], [mag_y_sus, mag_y_sus], color='blue', lw=2.5)

    # --- 6. FINALIZARE GRAFIC ---
    ax.set_aspect('equal')
    ax.set_xlim(-0.5, L_sera + 0.5)
    ax.set_ylim(-0.5, W_sera + 0.5)
    plt.legend(loc='lower right', fontsize='small')
    return fig
