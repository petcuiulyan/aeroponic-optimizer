import matplotlib.pyplot as plt
import matplotlib.patches as patches

def calculeaza_layout(L_utila, pas_x):
    nr_x = int(L_utila / pas_x)
    return nr_x, nr_x * 4

def randeaza_2d(L_sera, W_sera, L_tech, nr_x, pas_x, dist_y, D_bazin, culoar):
    fig, ax = plt.subplots(figsize=(14, 8))
    
    # 1. Contur Seră
    ax.add_patch(patches.Rectangle((0, 0), L_sera, W_sera, lw=3, ec='black', fc='none'))
    
    # 2. Zona Tehnică (Gri deschis)
    ax.add_patch(patches.Rectangle((0, 0), L_tech, W_sera, alpha=0.05, fc='gray'))
    
    # IBC-uri: IBC2 Jos, IBC1 Sus
    ibc_s = 1.0
    y_ibc2 = 0.5 
    y_ibc1 = y_ibc2 + ibc_s + 1.0
    
    # Desenare IBC 2 (Stocare/Retur)
    ax.add_patch(patches.Rectangle((0.2, y_ibc2), ibc_s, ibc_s, fc='#a2d2ff', ec='blue', lw=2))
    ax.text(0.7, y_ibc2 + 0.5, "IBC 2\n(STOCK/RETUR)", ha='center', va='center', fontsize=8, fontweight='bold')
    
    # Desenare IBC 1 (Preparare)
    ax.add_patch(patches.Rectangle((0.2, y_ibc1), ibc_s, ibc_s, fc='#a2d2ff', ec='blue', lw=2))
    ax.text(0.7, y_ibc1 + 0.5, "IBC 1\n(PREP)", ha='center', va='center', fontsize=8, fontweight='bold')

    # Pompa HPA (Roșu) - Lângă IBC 2
    p_x, p_y = L_tech - 0.4, y_ibc2 + 0.5
    ax.plot(p_x, p_y, 'ro', markersize=12)
    ax.plot([0.2 + ibc_s, p_x], [y_ibc2 + 0.5, p_y], color='blue', lw=2) # Link IBC2-Pompa

    # 3. Calcul rânduri turnuri
    y_j1 = (W_sera / 2) - (culoar / 2) - D_bazin - dist_y - D_bazin
    y_j2 = (W_sera / 2) - (culoar / 2) - D_bazin
    y_s1 = (W_sera / 2) + (culoar / 2)
    y_s2 = (W_sera / 2) + (culoar / 2) + D_bazin + dist_y
    
    mag_y_j = y_j2 - (dist_y / 2)
    mag_y_s = y_s1 + D_bazin + (dist_y / 2)

    # Alimentare din Pompa HPA
    ax.plot([p_x, p_x, L_tech], [p_y, mag_y_j, mag_y_j], color='blue', lw=2)
    ax.plot([p_x, p_x, L_tech], [p_y, mag_y_s, mag_y_s], color='blue', lw=2)

    # 4. Turnuri
    for i in range(nr_x):
        x = L_tech + (i * pas_x) + 0.2
        for yy in [y_j1, y_j2, y_s1, y_s2]:
            ax.add_patch(plt.Circle((x + D_bazin/2, yy + D_bazin/2), D_bazin/2, color='#2ecc71', alpha=0.6))

    # Magistrale
    ax.plot([L_tech, L_sera - 0.5], [mag_y_j, mag_y_j], color='blue', lw=2)
    ax.plot([L_tech, L_sera - 0.5], [mag_y_s, mag_y_s], color='blue', lw=2)

    # 5. RETUR (Colectare prin JOS)
    ax.plot([L_sera - 0.5, L_sera - 0.5], [mag_y_s, 0.2], color='cyan', lw=2) # Coborâre
    ax.plot([L_sera - 0.5, 0.7], [0.2, 0.2], color='cyan', lw=2, ls='--')      # Magistrala Jos
    ax.plot([0.7, 0.7], [0.2, y_ibc2], color='cyan', lw=2, ls='--')           # Intrare IBC2

    ax.set_aspect('equal')
    return fig
