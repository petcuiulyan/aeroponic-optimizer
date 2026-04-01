import matplotlib.pyplot as plt
import matplotlib.patches as patches

def calculeaza_layout(L_utila, W_sera, pas_x, D_bazin, dist_y, culoar_min):
    nr_x = int(L_utila / pas_x)
    y_positions = []
    magistrale_y = []
    
    # Pornim de la 0.5m de peretele de jos
    current_y = 0.5 
    
    # State 0: Căutăm să punem primul rând dintr-o pereche
    # State 1: Am pus primul rând, încercăm să punem perechea lui
    state = 0 
    
    while current_y + D_bazin <= W_sera - 0.5:
        # Adăugăm rândul curent
        y_positions.append(current_y)
        
        if state == 0:
            # Tocmai am pus rândul 1 dintr-o posibilă pereche
            # Verificăm dacă mai încape rândul 2 (perechea) la distanță mică
            next_y_pair = current_y + D_bazin + dist_y
            
            if next_y_pair + D_bazin <= W_sera - 0.5:
                # Încap ambele! Punem magistrala între ele
                magistrale_y.append(current_y + D_bazin + (dist_y / 2))
                current_y = next_y_pair
                state = 1 # Marcăm că am terminat o pereche
            else:
                # Nu mai încape perechea, punem o magistrală individuală și ieșim
                magistrale_y.append(current_y + D_bazin/2)
                break
        else:
            # Am terminat o pereche (2 rânduri). Trebuie să sărim obligatoriu culoarul
            current_y = current_y + D_bazin + culoar_min
            state = 0 # Resetăm pentru o nouă pereche după culoar
            
    total_turnuri = nr_x * len(y_positions)
    return nr_x, y_positions, magistrale_y, total_turnuri

def randeaza_2d(L_sera, W_sera, L_tech, nr_x, y_positions, magistrale_y, pas_x, D_bazin, total_turnuri):
    fig, ax = plt.subplots(figsize=(16, 10))
    
    # Fundal și Zonă Tehnică
    ax.add_patch(patches.Rectangle((0, 0), L_sera, W_sera, lw=3, ec='black', fc='none'))
    ax.add_patch(patches.Rectangle((0, 0), L_tech, W_sera, alpha=0.08, fc='gray'))

    # Componente Zonă Tehnică
    ax.add_patch(patches.Rectangle((0.2, 0.3), 1, 1, fc='#a2d2ff', ec='blue', lw=2)) # IBC 2
    ax.add_patch(patches.Rectangle((0.2, 2.3), 1, 1, fc='#e0f2fe', ec='blue', lw=1.5)) # IBC 1
    p_x, p_y = L_tech - 0.4, 0.8
    ax.plot(p_x, p_y, 'ro', markersize=12)

    # Turnuri (Cercuri)
    for i in range(nr_x):
        x = L_tech + (i * pas_x) + 0.2
        for y in y_positions:
            ax.add_patch(plt.Circle((x + D_bazin/2, y + D_bazin/2), D_bazin/2, color='#2ecc71', alpha=0.5))

    # Magistrale HPA (Albastru)
    for my in magistrale_y:
        ax.plot([L_tech, L_sera - 0.5], [my, my], color='blue', lw=2)
        ax.plot([p_x, p_x, L_tech], [p_y, my, my], color='blue', lw=1.5, alpha=0.3)

    # Retur Recirculare (Cyan)
    if magistrale_y:
        max_m_y = max(magistrale_y)
        ax.plot([L_sera - 0.5, L_sera - 0.5], [max_m_y, 0.15], color='cyan', lw=2.5)
        ax.plot([L_sera - 0.5, 0.7], [0.15, 0.15], color='cyan', lw=2.5, ls='--')
        ax.plot([0.7, 0.7], [0.15, 0.3], color='cyan', lw=2.5, ls='--')

    ax.set_aspect('equal')
    ax.set_xlim(-0.5, L_sera + 0.5)
    ax.set_ylim(-0.5, W_sera + 0.5)
    plt.title(f"Layout Optimizat Fără Suprapunere: {total_turnuri} Turnuri", fontsize=15)
    return fig
