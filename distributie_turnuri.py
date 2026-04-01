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
                # Magistrala trece între rânduri
                magistrale_y.append(current_y + D_bazin + (dist_y / 2))
                current_y = next_y_pair
                state = 1
            else:
                # Rând singur la final: magistrala trece pe marginea de sus a bazinului
                magistrale_y.append(current_y + D_bazin + 0.1)
                break
        else:
            current_y = current_y + D_bazin + culoar_min
            state = 0
            
    total_turnuri = nr_x * len(y_positions)
    return nr_x, y_positions, magistrale_y, total_turnuri

def randeaza_2d(L_sera, W_sera, L_tech, nr_x, y_positions, magistrale_y, pas_x, D_bazin, total_turnuri):
    fig, ax = plt.subplots(figsize=(16, 10))
    
    # 1. Spațiu și Zonă Tehnică
    ax.add_patch(patches.Rectangle((0, 0), L_sera, W_sera, lw=3, ec='black', fc='none'))
    ax.add_patch(patches.Rectangle((0, 0), L_tech, W_sera, alpha=0.08, fc='gray'))

    # 2. IBC-uri și Pompă
    ax.add_patch(patches.Rectangle((0.2, 0.3), 1, 1, fc='#a2d2ff', ec='blue', lw=2)) # IBC 2
    ax.add_patch(patches.Rectangle((0.2, 2.3), 1, 1, fc='#e0f2fe', ec='blue', lw=1.5)) # IBC 1
    p_x, p_y = L_tech - 0.4, 0.8
    ax.plot(p_x, p_y, 'ro', markersize=12, label="Pompa HPA")

    # 3. Turnuri (Desenate primele, pentru a fi sub magistrale vizual dacă e cazul)
    for i in range(nr_x):
        x = L_tech + (i * pas_x) + 0.2
        for y in y_positions:
            ax.add_patch(plt.Circle((x + D_bazin/2, y + D_bazin/2), D_bazin/2, 
                                    color='#2ecc71', alpha=0.4, ec='darkgreen', lw=0.5))

    # 4. Magistrale (Corectate să treacă PE LÂNGĂ turnuri)
    for my in magistrale_y:
        # Magistrala orizontală
        ax.plot([L_tech, L_sera - 0.5], [my, my], color='blue', lw=3, zorder=5)
        # Legătura verticală la sursa de apă (Pompă)
        ax.plot([p_x, p_x, L_tech], [p_y, my, my], color='blue', lw=2, alpha=0.5, zorder=4)
        
        # Desenăm conexiunile de la magistrală la fiecare turn (micile furtunuri)
        # Acestea vor pleca din magistrală spre centrul turnului
        for i in range(nr_x):
            x_t = L_tech + (i * pas_x) + 0.2 + D_bazin/2
            # Găsim rândul cel mai apropiat de această magistrală
            closest_y = min(y_positions, key=lambda y: abs((y + D_bazin/2) - my))
            if abs((closest_y + D_bazin/2) - my) < (D_bazin + dist_y):
                ax.plot([x_t, x_t], [my, closest_y + D_bazin/2], color='blue', lw=1, alpha=0.3)

    # 5. Colector Retur (Cyan)
    if magistrale_y:
        max_m_y = max(magistrale_y)
        ax.plot([L_sera - 0.5, L_sera - 0.5], [max_m_y, 0.15], color='cyan', lw=3)
        ax.plot([L_sera - 0.5, 0.7], [0.15, 0.15], color='cyan', lw=2, ls='--')
        ax.plot([0.7, 0.7], [0.15, 0.3], color='cyan', lw=2, ls='--')

    ax.set_aspect('equal')
    ax.set_xlim(-0.5, L_sera + 0.5)
    ax.set_ylim(-0.5, W_sera + 0.5)
    plt.title(f"Layout Aeroponic Optimizat: {total_turnuri} Turnuri | Magistrale pe Culoar", fontsize=15)
    return fig
