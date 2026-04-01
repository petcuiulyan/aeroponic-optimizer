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
    
    # 1. Contur Seră
    ax.add_patch(patches.Rectangle((0, 0), L_sera, W_sera, lw=3, ec='black', fc='none'))
    ax.add_patch(patches.Rectangle((0, 0), L_tech, W_sera, alpha=0.08, fc='gray'))

    # --- 2. ZONA TEHNICĂ ---
    y_ibc2 = 0.5
    y_ibc1 = y_ibc2 + 2.0 
    
    # IBC 2 & IBC 1
    ax.add_patch(patches.Rectangle((0.2, y_ibc2), 1, 1, fc='#a2d2ff', ec='blue', lw=2, zorder=5))
    ax.add_patch(patches.Rectangle((0.2, y_ibc1), 1, 1, fc='#e0f2fe', ec='blue', lw=1.5, zorder=5))
    ax.text(0.7, y_ibc2+0.5, "IBC 2\n(STOCK)", ha='center', fontweight='bold', fontsize=8)
    ax.text(0.7, y_ibc1+0.5, "IBC 1\n(PREP)", ha='center', fontweight='bold', fontsize=8)

    # POMPA TRANSFER (IBC1 -> IBC2)
    p_trans_y = (y_ibc1 + y_ibc2 + 1.0) / 2
    ax.plot(0.7, p_trans_y, 'go', markersize=8, zorder=6)
    ax.plot([0.7, 0.7], [y_ibc1, y_ibc2 + 1.0], color='green', lw=1.5, ls='--', alpha=0.6)

    # POMPA HPA (IBC2 -> Sistem)
    p_hpa_x, p_hpa_y = L_tech - 0.5, y_ibc2 + 0.5
    ax.plot(p_hpa_x, p_hpa_y, 'ro', markersize=12, zorder=10)
    ax.plot([1.2, p_hpa_x], [y_ibc2 + 0.5, p_hpa_y], color='blue', lw=2)

    # --- 3. TURNURI & LEGĂTURI ---
    for i in range(nr_x):
        x_t = L_tech + (i * pas_x) + 0.2 + D_bazin/2
        y_base_t = L_tech + (i * pas_x) + 0.2 # Coordonata X de start a bazinului
        
        for y_t in y_positions:
            # Desenare Turn
            ax.add_patch(plt.Circle((x_t, y_t + D_bazin/2), D_bazin/2, 
                                    color='#2ecc71', alpha=0.4, ec='darkgreen', lw=0.5))
            
            # LEGĂTURA LA MAGISTRALĂ (Feeder)
            # Găsim magistrala cea mai apropiată de acest rând
            closest_mag = min(magistrale_y, key=lambda m: abs(m - (y_t + D_bazin/2)))
            # Desenăm legătura doar dacă magistrala deservește acest rând (distanță mică)
            if abs(closest_mag - (y_t + D_bazin/2)) < (D_bazin + dist_y):
                ax.plot([x_t, x_t], [closest_mag, y_t + D_bazin/2], color='blue', lw=1, alpha=0.3)

    # --- 4. MAGISTRALE ORIZONTALE ---
    for my in magistrale_y:
        # Linia principală de rând
        ax.plot([L_tech, L_sera - 0.5], [my, my], color='blue', lw=3, zorder=6)
        # Conexiunea verticală de la Pompa HPA la fiecare magistrală
        ax.plot([p_hpa_x, p_hpa_x, L_tech], [p_hpa_y, my, my], color='blue', lw=1.5, alpha=0.4)

    # --- 5. RETUR ---
    if magistrale_y:
        max_m_y = max(magistrale_y)
        # Colector vertical la capăt
        ax.plot([L_sera - 0.5, L_sera - 0.5], [max_m_y, 0.15], color='cyan', lw=3)
        # Magistrala de retur pe jos
        ax.plot([L_sera - 0.5, 0.7], [0.15, 0.15], color='cyan', lw=2.5, ls='--')
        # Intrare în IBC 2
        ax.plot([0.7, 0.7], [0.15, y_ibc2], color='cyan', lw=2.5, ls='--')

    ax.set_aspect('equal')
    ax.set_xlim(-0.5, L_sera + 0.5)
    ax.set_ylim(-0.5, W_sera + 0.5)
    return fig
