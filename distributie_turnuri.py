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
                # Magistrala trece EXACT la mijlocul spațiului dist_y
                magistrale_y.append(current_y + D_bazin + (dist_y / 2))
                current_y = next_y_pair
                state = 1
            else:
                # Rând singur la final
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

    # 2. IBC-uri și Pompă
    ax.add_patch(patches.Rectangle((0.2, 0.3), 1, 1, fc='#a2d2ff', ec='blue', lw=2))
    ax.add_patch(patches.Rectangle((0.2, 2.3), 1, 1, fc='#e0f2fe', ec='blue', lw=1.5))
    p_x, p_y = L_tech - 0.4, 0.8
    ax.plot(p_x, p_y, 'ro', markersize=12, zorder=10)

    # 3. Turnuri
    for i in range(nr_x):
        x = L_tech + (i * pas_x) + 0.2
        for y in y_positions:
            ax.add_patch(plt.Circle((x + D_bazin/2, y + D_bazin/2), D_bazin/2, 
                                    color='#2ecc71', alpha=0.5, ec='darkgreen', lw=0.5))

    # 4. Magistrale (Zorder mare pentru a fi peste conexiuni)
    for my in magistrale_y:
        ax.plot([L_tech, L_sera - 0.5], [my, my], color='blue', lw=3, zorder=6)
        ax.plot([p_x, p_x, L_tech], [p_y, my, my], color='blue', lw=1.5, alpha=0.4, zorder=5)
        
        # Conexiuni scurte de la magistrală la centrele turnurilor
        for i in range(nr_x):
            x_t = L_tech + (i * pas_x) + 0.2 + D_bazin/2
            # Căutăm cele două rânduri deservite de această magistrală
            for y in y_positions:
                if abs((y + D_bazin/2) - my) < (D_bazin/2 + dist_y):
                    ax.plot([x_t, x_t], [my, y + D_bazin/2], color='blue', lw=1, alpha=0.2)

    # 5. Colector Retur (Cyan)
    if magistrale_y:
        max_m_y = max(magistrale_y)
        ax.plot([L_sera - 0.5, L_sera - 0.5], [max_m_y, 0.15], color='cyan', lw=3)
        ax.plot([L_sera - 0.5, 0.7], [0.15, 0.15], color='cyan', lw=2, ls='--')
        ax.plot([0.7, 0.7], [0.15, 0.3], color='cyan', lw=2, ls='--')

    ax.set_aspect('equal')
    ax.set_xlim(-0.5, L_sera + 0.5)
    ax.set_ylim(-0.5, W_sera + 0.5)
    plt.title(f"Layout Aeroponic: {total_turnuri} Turnuri | {len(y_positions)} Rânduri", fontsize=15)
    return fig
