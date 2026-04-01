import matplotlib.pyplot as plt
import matplotlib.patches as patches

def calculeaza_layout(L_utila, W_sera, pas_x, D_bazin, dist_y, culoar_min):
    nr_x = int(L_utila / pas_x)
    
    y_positions = []
    magistrale_y = []
    
    # Pornim de la marginea de jos
    current_y = 0.5 
    
    # Stare: 0 = trebuie să punem primul rând dintr-o pereche, 1 = trebuie să punem al doilea rând (perechea)
    state = 0 
    
    while current_y + D_bazin <= W_sera - 0.5:
        # Plasăm rândul curent
        y_positions.append(current_y)
        
        if state == 0:
            # Tocmai am pus primul rând. Încercăm să punem perechea (la distanță mică dist_y)
            next_y_if_pair = current_y + D_bazin + dist_y
            
            # Verificăm dacă mai încape perechea + un culoar minim după ea sau dacă e ultimul rând posibil
            if next_y_if_pair + D_bazin <= W_sera - 0.5:
                # Creăm magistrala între cele două rânduri
                magistrale_y.append(current_y + D_bazin + (dist_y / 2))
                current_y = next_y_if_pair
                state = 1 # Următorul pas va trebui să sară un culoar
            else:
                # Nu mai încape nici măcar perechea, închidem magistrala aici
                magistrale_y.append(current_y + D_bazin/2)
                break
        else:
            # Am terminat o pereche. Trebuie să sărim un culoar de minim 1.2m
            next_y_after_aisle = current_y + D_bazin + culoar_min
            
            if next_y_after_aisle + D_bazin <= W_sera - 0.5:
                current_y = next_y_after_aisle
                state = 0 # Resetăm la începutul unei noi perechi
            else:
                # Nu mai încape un rând nou după culoar
                break

    total_turnuri = nr_x * len(y_positions)
    return nr_x, y_positions, magistrale_y, total_turnuri

def randeaza_2d(L_sera, W_sera, L_tech, nr_x, y_positions, magistrale_y, pas_x, D_bazin, total_turnuri):
    fig, ax = plt.subplots(figsize=(16, 10))
    
    # Desenăm limitele serei
    ax.add_patch(patches.Rectangle((0, 0), L_sera, W_sera, lw=3, ec='black', fc='none'))
    ax.add_patch(patches.Rectangle((0, 0), L_tech, W_sera, alpha=0.1, fc='gray'))

    # IBC-uri și Pompa
    ax.add_patch(patches.Rectangle((0.2, 0.3), 1, 1, fc='#a2d2ff', ec='blue', lw=2)) # IBC 2
    ax.add_patch(patches.Rectangle((0.2, 2.3), 1, 1, fc='#e0f2fe', ec='blue', lw=1.5)) # IBC 1
    p_x, p_y = L_tech - 0.4, 0.8
    ax.plot(p_x, p_y, 'ro', markersize=12)

    # Turnuri
    for i in range(nr_x):
        x = L_tech + (i * pas_x) + 0.2
        for y in y_positions:
            ax.add_patch(plt.Circle((x + D_bazin/2, y + D_bazin/2), D_bazin/2, color='#2ecc71', alpha=0.6))

    # Magistrale
    for my in magistrale_y:
        ax.plot([L_tech, L_sera - 0.5], [my, my], color='blue', lw=2, label="Magistrală HPA")
        ax.plot([p_x, p_x, L_tech], [p_y, my, my], color='blue', lw=1.5, alpha=0.4)

    # Retur Recirculare
    if magistrale_y:
        max_m_y = max(magistrale_y)
        ax.plot([L_sera - 0.5, L_sera - 0.5], [max_m_y, 0.15], color='cyan', lw=2)
        ax.plot([L_sera - 0.5, 0.7], [0.15, 0.15], color='cyan', lw=2, ls='--')
        ax.plot([0.7, 0.7], [0.15, 0.3], color='cyan', lw=2, ls='--')

    ax.set_aspect('equal')
    plt.title(f"Distribuție Optimizată: {len(y_positions)} rânduri | Total {total_turnuri} Turnuri", fontsize=15)
    return fig
