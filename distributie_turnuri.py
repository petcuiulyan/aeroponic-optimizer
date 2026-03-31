import matplotlib.pyplot as plt
import matplotlib.patches as patches

def calculeaza_layout(L_utila, pas_x):
    # Calculăm câte coloane de turnuri încap pe lungimea rămasă
    nr_x = int(L_utila / pas_x)
    return nr_x, nr_x * 4

def randeaza_2d(L_sera, W_sera, L_tech, nr_x, pas_x, dist_y, D_bazin, culoar):
    fig, ax = plt.subplots(figsize=(14, 8))
    
    # --- 1. CONTUR SERĂ ---
    ax.add_patch(patches.Rectangle((0, 0), L_sera, W_sera, lw=3, ec='black', fc='none'))
    
    # --- 2. ZONA TEHNICĂ (IBC2 JOS, IBC1 SUS) ---
    ax.add_patch(patches.Rectangle((0, 0), L_tech, W_sera, alpha=0.05, fc='gray'))
    
    ibc_s = 1.0
    y_ibc2 = 0.3 # Aproape de limita de jos
    y_ibc1 = y_ibc2 + ibc_s + 0.8 # IBC1 la distanță de IBC2
    
    # Desenare IBC 2 (Stocare și Retur)
    ax.add_patch(patches.Rectangle((0.2, y_ibc2), ibc_s, ibc_s, fc='#a2d2ff', ec='blue', lw=2))
    ax.text(0.7, y_ibc2 + 0.5, "IBC 2\n(STOCK/RETUR)", ha='center', va='center', fontsize=8, fontweight='bold')
    
    # Desenare IBC 1 (Preparare)
    ax.add_patch(patches.Rectangle((0.2, y_ibc1), ibc_s, ibc_s, fc='#e0f2fe', ec='blue', lw=1.5))
    ax.text(0.7, y_ibc1 + 0.5, "IBC 1\n(PREP)", ha='center', va='center', fontsize=8, fontweight='bold')

    # Pompa de Transfer (Verticală între ele)
    ax.plot([0.7, 0.7], [y_ibc1, y_ibc2 + ibc_s], color='darkblue', lw=2, ls=':')
    ax.plot(0.7, (y_ibc1 + y_ibc2 + ibc_s)/2, 'go', markersize=7)

    # POMPA HPA (Lângă IBC 2, estetic)
    p_x, p_y = L_tech - 0.4, y_ibc2 + 0.5
    ax.plot(p_x, p_y, 'ro', markersize=12)
    ax.text(p_x, p_y - 0.4, "POMPA HPA", ha='center', color='red', fontsize=8, fontweight='bold')
    ax.plot([0.2 + ibc_s, p_x], [y_ibc2 + 0.5, p_y], color='blue', lw=2) # Conexiune IBC2-Pompă

    # --- 3. CONFIGURARE RÂNDURI TURNURI ---
    # Calculăm pozițiile Y pentru a lăsa culoarul pe centru
    y_j1 = (W_sera / 2) - (culoar / 2) - D_bazin - dist_y - D_bazin
    y_j2 = (W_sera / 2) - (culoar / 2) - D_bazin
    y_s1 = (W_sera / 2) + (culoar / 2)
    y_s2 = (W_sera / 2) + (culoar / 2) + D_bazin + dist_y
    
    mag_y_j = y_j2 - (dist_y / 2)
    mag_y_s = y_s1 + D_bazin + (dist_y / 2)

    # Alimentare din Pompa HPA către Magistrale (Traseu în unghi drept)
    ax.plot([p_x, p_x, L_tech], [p_y, mag_y_j, mag_y_j], color='blue', lw=2.5)
    ax.plot([p_x, p_x, L_tech], [p_y, mag_y_s, mag_y_s], color='blue', lw=2.5)

    # --- 4. TURNURI ȘI MAGISTRALE ---
    for i in range(nr_x):
        x_pos = L_tech + (i * pas_x) + 0.2
        for idx, yy in enumerate([y_j1, y_j2, y_s1, y_s2]):
            # Turn
            ax.add_patch(plt.Circle((x_pos + D_bazin/2, yy + D_bazin/2), D_bazin/2, color='#2ecc71', alpha=0.6))
            # Derivație subțire către magistrală
            m_y = mag_y_j if idx < 2 else mag_y_s
            ax.plot([x_pos + D_bazin/2, x_pos + D_bazin/2], [yy + D_bazin/2, m_y], color='blue', lw=0.5, alpha=0.3)

    # Liniile magistrale orizontale
    ax.plot([L_tech, L_sera - 0.5], [mag_y_j, mag_y_j], color='blue', lw=2.5)
    ax.plot([L_tech, L_sera - 0.5], [mag_y_s, mag_y_s], color='blue', lw=2.5)

    # --- 5. CIRCUIT RETUR (PRIN PARTEA DE JOS) ---
    # Linia verticală de colectare la capătul serei (dreapta)
    ax.plot([L_sera - 0.5, L_sera - 0.5], [mag_y_s, 0.15], color='cyan', lw=2)
    # Linia orizontală de retur care vine prin JOS de tot
    ax.plot([L_sera - 0.5, 0.7], [0.15, 0.15], color='cyan', lw=2, ls='--')
    # Urcarea în IBC 2
    ax.plot([0.7, 0.7], [0.15, y_ibc2], color='cyan', lw=2, ls='--')
    
    ax.text(L_sera/2, 0.25, "RETUR COLECTARE (Circuit Închis)", ha='center', fontsize=7, color='darkcyan', fontweight='bold')

    # --- 6. FINALIZARE ---
    ax.set_aspect('equal')
    ax.set_xlim(-0.5, L_sera + 0.5)
    ax.set_ylim(-0.5, W_sera + 0.5)
    ax.grid(True, linestyle=':', alpha=0.2)
    
    return fig
