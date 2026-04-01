pimport matplotlib.pyplot as plt
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

def randeaza_2d(L_sera, W_sera, L_tech, nr_x, y_positions, magistrale_y, pas_x, D_bazin, dist_y, total_turnuri, culoar_min):
    fig, ax = plt.subplots(figsize=(18, 11))
    
    # 1. Contur și Zonă Tehnică
    ax.add_patch(patches.Rectangle((0, 0), L_sera, W_sera, lw=3, ec='black', fc='none'))
    ax.add_patch(patches.Rectangle((0, 0), L_tech, W_sera, alpha=0.08, fc='gray'))
    ax.text(L_tech/2, W_sera - 0.5, "ZONĂ TEHNICĂ", ha='center', fontweight='bold', alpha=0.3)

    # 2. IBC-uri
    y_ibc2, y_ibc1 = 0.5, 2.5
    ax.add_patch(patches.Rectangle((0.2, y_ibc2), 1, 1, fc='#a2d2ff', ec='blue', lw=2, zorder=5))
    ax.add_patch(patches.Rectangle((0.2, y_ibc1), 1, 1, fc='#e0f2fe', ec='blue', lw=1.5, zorder=5))
    ax.text(0.7, y_ibc2+0.5, "IBC 2\n(STOCK)", ha='center', va='center', fontweight='bold', fontsize=9)
    ax.text(0.7, y_ibc1+0.5, "IBC 1\n(PREP)", ha='center', va='center', fontweight='bold', fontsize=9)

    # 3. Pompe și Legături Tehnice
    p_hpa_x, p_hpa_y = L_tech - 0.5, y_ibc2 + 0.5
    ax.plot(p_hpa_x, p_hpa_y, 'ro', markersize=15, zorder=10) # Pompa HPA
    ax.text(p_hpa_x, p_hpa_y + 0.3, "POMPĂ HPA\n(20 BAR)", color='red', fontweight='bold', ha='center', fontsize=8)
    
    p_tr_y = (y_ibc1 + y_ibc2 + 1.0) / 2
    ax.plot(0.7, p_tr_y, 'go', markersize=10, zorder=10) # Pompa Transfer
    ax.text(0.1, p_tr_y, "POMPĂ\nTRANSFER", color='green', fontweight='bold', fontsize=8)
    ax.plot([0.7, 0.7], [y_ibc1, y_ibc2 + 1.0], color='green', lw=2, ls='--', alpha=0.5)

    # 4. Turnuri și Feedere (Legături)
    for i in range(nr_x):
        x_c = L_tech + (i * pas_x) + 0.2 + D_bazin/2
        for y_t in y_positions:
            y_c = y_t + D_bazin/2
            ax.add_patch(plt.Circle((x_c, y_c), D_bazin/2, color='#2ecc71', alpha=0.4, ec='darkgreen'))
            
            # Legătura la magistrală
            closest_m = min(magistrale_y, key=lambda m: abs(m - y_c))
            if abs(closest_m - y_c) < (D_bazin):
                ax.plot([x_c, x_c], [closest_m, y_c], color='blue', lw=0.8, alpha=0.4)

    # 5. Magistrale și Cotele de Dimensiuni
    for idx, my in enumerate(magistrale_y):
        ax.plot([L_tech, L_sera - 0.5], [my, my], color='blue', lw=3, zorder=6)
        ax.text(L_sera - 2, my + 0.1, f"Magistrală {idx+1}", color='blue', fontsize=7)
        ax.plot([p_hpa_x, p_hpa_x, L_tech], [p_hpa_y, my, my], color='blue', lw=1.5, alpha=0.4)

    # --- COTE (DIMENSIUNI PE PLAN) ---
    # Cotă Pas X (între primele două turnuri)
    if nr_x > 1:
        x1 = L_tech + 0.2 + D_bazin/2
        x2 = x1 + pas_x
        ax.annotate('', xy=(x1, W_sera-0.2), xytext=(x2, W_sera-0.2), arrowprops=dict(arrowstyle='<->', color='gray'))
        ax.text((x1+x2)/2, W_sera-0.15, f"Pas X: {pas_x:.2f}m", ha='center', fontsize=8, color='gray')

    # Cotă Culoar (între primele două grupuri)
    if len(y_positions) >= 3:
        y_c1 = y_positions[1] + D_bazin
        y_c2 = y_positions[2]
        ax.annotate('', xy=(L_sera-0.3, y_c1), xytext=(L_sera-0.3, y_c2), arrowprops=dict(arrowstyle='<->', color='orange'))
        ax.text(L_sera-0.2, (y_c1+y_c2)/2, f"Culoar: {y_c2-y_c1:.2f}m", va='center', rotation=90, fontsize=8, color='orange')

    # Cotă Spațiu Pereche (dist_y)
    if len(y_positions) >= 2:
        y_p1 = y_positions[0] + D_bazin
        y_p2 = y_positions[1]
        ax.annotate('', xy=(L_tech+0.5, y_p1), xytext=(L_tech+0.5, y_p2), arrowprops=dict(arrowstyle='<->', color='blue'))
        ax.text(L_tech+0.6, (y_p1+y_p2)/2, f"Spațiu Y: {dist_y:.2f}m", va='center', fontsize=7, color='blue')

    # 6. Retur
    if magistrale_y:
        max_m_y = max(magistrale_y)
        ax.plot([L_sera - 0.5, L_sera - 0.5], [max_m_y, 0.15], color='cyan', lw=3)
        ax.plot([L_sera - 0.5, 0.7], [0.15, 0.15], color='cyan', lw=2.5, ls='--')
        ax.plot([0.7, 0.7], [0.15, y_ibc2], color='cyan', lw=2.5, ls='--')
        ax.text(L_sera/2, 0.05, "CONDUCTĂ RETUR (RECIRCULARE)", color='darkcyan', fontweight='bold', fontsize=8, ha='center')

    ax.set_aspect('equal')
    plt.title(f"PLAN TEHNIC AEROPONIC - {total_turnuri} Turnuri", fontsize=16, fontweight='bold', pad=20)
    return fig
