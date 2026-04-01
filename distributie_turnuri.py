import matplotlib.pyplot as plt
import matplotlib.patches as patches

def calculeaza_layout(L_utila, W_sera, pas_x, D_bazin, dist_y, culoar_min):
    nr_x = int(L_utila / pas_x)
    y_positions = []
    magistrale_y = []
    
    current_y = 0.5 
    state = 0 
    
    while current_y + D_bazin <= W_sera - 0.5:
        y_positions.append(current_y)
        if state == 0:
            next_y_pair = current_y + D_bazin + dist_y
            if next_y_pair + D_bazin <= W_sera - 0.5:
                magistrale_y.append(current_y + D_bazin + (dist_y / 2))
                current_y = next_y_pair
                state = 1
            else:
                magistrale_y.append(current_y + D_bazin + 0.1)
                break
        else:
            current_y = current_y + D_bazin + culoar_min
            state = 0
            
    total_turnuri = nr_x * len(y_positions)
    return nr_x, y_positions, magistrale_y, total_turnuri

def randeaza_2d(L_sera, W_sera, L_tech, nr_x, y_positions, magistrale_y, pas_x, D_bazin, dist_y, total_turnuri):
    fig, ax = plt.subplots(figsize=(16, 10))
    
    # 1. Spațiu și Zonă Tehnică
    ax.add_patch(patches.Rectangle((0, 0), L_sera, W_sera, lw=3, ec='black', fc='none'))
    ax.add_patch(patches.Rectangle((0, 0), L_tech, W_sera, alpha=0.08, fc='gray'))

    # --- 2. CONFIGURARE HIDRAULICĂ ZONĂ TEHNICĂ ---
    # Coordonate IBC-uri
    y_ibc2 = 0.5
    y_ibc1 = y_ibc2 + 1.0 + 1.0 # 1m distanță între ele
    
    # Desenare IBC 2 (Rezervor de lucru / Buffer)
    ax.add_patch(patches.Rectangle((0.2, y_ibc2), 1, 1, fc='#a2d2ff', ec='blue', lw=2, zorder=5))
    ax.text(0.7, y_ibc2+0.5, "IBC 2\n(STOCK)", ha='center', fontweight='bold', fontsize=8)
    
    # Desenare IBC 1 (Preparare Nutrienți)
    ax.add_patch(patches.Rectangle((0.2, y_ibc1), 1, 1, fc='#e0f2fe', ec='blue', lw=1.5, zorder=5))
    ax.text(0.7, y_ibc1+0.5, "IBC 1\n(PREP)", ha='center', fontweight='bold', fontsize=8)

    # POMPA DE TRANSFER (Între IBC1 și IBC2)
    p_trans_x, p_trans_y = 0.7, y_ibc2 + 1.5
    ax.plot(p_trans_x, p_trans_y, 'go', markersize=8, zorder=6) # Verde pentru transfer
    ax.text(p_trans_x + 0.2, p_trans_y, "Pompă\nTransfer", fontsize=7, color='green')
    # Legături Transfer: IBC1 -> Pompă -> IBC2
    ax.plot([0.7, 0.7], [y_ibc1, p_trans_y], color='green', lw=1.5, ls='--')
    ax.plot([0.7, 0.7], [p_trans_y, y_ibc2 + 1.0], color='green', lw=1.5, ls='--')

    # POMPA PRINCIPALĂ HPA (Lângă IBC 2)
    p_hpa_x, p_hpa_y = L_tech - 0.5, y_ibc2 + 0.5
    ax.plot(p_hpa_x, p_hpa_y, 'ro', markersize=12, zorder=10)
    ax.text(p_hpa_x, p_hpa_y - 0.4, "POMPA HPA\n(20 BAR)", ha='center', color='red', fontweight='bold', fontsize=8)
    # Legătură IBC 2 -> Pompă HPA
    ax.plot([1.2, p_hpa_x], [y_ibc2 + 0.5, p_hpa_y], color='blue', lw=2.5)

    # 3. Turnuri
    for i in range(nr_x):
        x = L_tech + (i * pas_x) + 0.2
        for y in y_positions:
            ax.add_patch(plt.Circle((x + D_bazin/2, y + D_bazin/2), D_bazin/2, 
                                    color='#2ecc71', alpha=0.4, ec='darkgreen', lw=0.5))

    # 4. Magistrale și Distribuție
    for my in magistrale_y:
        # Magistrala orizontală
        ax.plot([L_tech, L_sera - 0.5], [my, my], color='blue', lw=3, zorder=6)
        # Legătura din Pompa HPA către Magistrale (Traseu Curat)
        ax.plot([p_hpa_x, p_hpa_x, L_tech], [p_hpa_y, my, my], color='blue', lw=1.5, alpha=0.5)

    # 5. Colector Retur (Cyan)
    # Colectează de la capătul magistralelor și se întoarce în IBC 2
    if magistrale_y:
        max_m_y = max(magistrale_y)
        ax.plot([L_sera - 0.5, L_sera - 0.5], [max_m_y, 0.15], color='cyan', lw=3)
        ax.plot([L_sera - 0.5, 0.7], [0.15, 0.15], color='cyan', lw=2.5, ls='--')
        ax.plot([0.7, 0.7], [0.15, y_ibc2], color='cyan', lw=2.5, ls='--')
        ax.text(L_sera/2, 0.25, "RETUR COLECTARE", color='darkcyan', fontsize=7, ha='center', fontweight='bold')

    ax.set_aspect('equal')
    ax.set_xlim(-0.5, L_sera + 0.5)
    ax.set_ylim(-0.5, W_sera + 0.5)
    return fig
