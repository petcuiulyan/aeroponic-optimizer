import matplotlib.pyplot as plt
import matplotlib.patches as patches

def calculeaza_layout(L_utila, W_sera, pas_x, D_bazin, dist_y, culoar_min):
    # 1. Calcul coloane pe lungime (fix)
    nr_x = int(L_utila / pas_x)
    
    # --- LOGICA REPETITIVĂ SMART PE LĂȚIME ---
    # Începem de la margini (sus și jos) și avansăm spre centru
    y_positions = []
    magistrale_y = []
    
    buffer_perete = 0.5
    y_jos_curent = buffer_perete
    y_sus_curent = W_sera - buffer_perete - D_bazin

    # Adăugăm primele perechi marginale (obligatorii)
    # Perechea JOS
    y_jos_next = y_jos_curent + D_bazin + dist_y
    y_positions.extend([y_jos_curent, y_jos_next])
    magistrale_y.append(y_jos_curent + D_bazin + (dist_y/2))
    
    # Perechea SUS
    y_sus_next = y_sus_curent - dist_y - D_bazin
    y_positions.extend([y_sus_next, y_sus_curent])
    magistrale_y.append(y_sus_curent - (dist_y/2))

    # Actualizăm frontul de avansare
    y_jos_front = y_jos_next + D_bazin
    y_sus_front = y_sus_next

    # --- BUCLA DE UMPLERE SMART ---
    # Încercăm să adăugăm perechi SIMETRICE dinspre margini spre centru
    # atâta timp cât spațiul rămas între fronturi este suficient
    # Necesar pentru o pereche nouă pe ambele părți: (2 * D_bazin + dist_y) + (2 * CuloarMin)
    # Dar noi verificăm doar dacă încap 2 rânduri și rămâne un culoar central
    
    necesar_pereche = D_bazin + dist_y + D_bazin
    
    continue_filling = True
    while continue_filling:
        # Spațiul liber actual pe mijloc
        spatiu_liber = y_sus_front - y_jos_front
        
        # Mai încap încă DOUĂ perechi (una jos, una sus) și un culoar central?
        if spatiu_liber > (2 * necesar_pereche + culoar_min):
            # Adăugăm pereche JOS
            y_r1 = y_jos_front + culoar_min # Lăsăm culoar față de rândul anterior
            y_r2 = y_r1 + D_bazin + dist_y
            y_positions.extend([y_r1, y_r2])
            magistrale_y.append(y_r1 + D_bazin + (dist_y/2))
            y_jos_front = y_r2 + D_bazin # Actualizăm frontul jos
            
            # Adăugăm pereche SUS
            y_r4 = y_sus_front - culoar_min - D_bazin # Lăsăm culoar față de rândul anterior
            y_r3 = y_r4 - dist_y - D_bazin
            y_positions.extend([y_r3, y_r4])
            magistrale_y.append(y_r4 - (dist_y/2))
            y_sus_front = y_r3 # Actualizăm frontul sus
            
        else:
            # Nu mai încap două perechi. Verificăm dacă mai încape UNA singură centrală
            if spatiu_liber > (necesar_pereche + 2 * culoar_min):
                y_centru = W_sera / 2
                y_r_mid1 = y_centru - (dist_y/2) - D_bazin
                y_r_mid2 = y_centru + (dist_y/2)
                y_positions.extend([y_r_mid1, y_r_mid2])
                magistrale_y.append(y_centru)
            
            continue_filling = False # Oprim bucla

    total_turnuri = nr_x * len(y_positions)
    return nr_x, y_positions, magistrale_y, total_turnuri

def randeaza_2d(L_sera, W_sera, L_tech, nr_x, y_positions, magistrale_y, pas_x, D_bazin):
    fig, ax = plt.subplots(figsize=(16, 10))
    
    # Contur și Zonă Tehnică
    ax.add_patch(patches.Rectangle((0, 0), L_sera, W_sera, lw=3, ec='black', fc='none'))
    ax.add_patch(patches.Rectangle((0, 0), L_tech, W_sera, alpha=0.05, fc='gray'))

    # IBC-uri și Pompă
    ax.add_patch(patches.Rectangle((0.2, 0.3), 1, 1, fc='#a2d2ff', ec='blue', lw=2)) # IBC 2
    ax.add_patch(patches.Rectangle((0.2, 2.3), 1, 1, fc='#e0f2fe', ec='blue', lw=1.5)) # IBC 1
    p_x, p_y = L_tech - 0.4, 0.8
    ax.plot(p_x, p_y, 'ro', markersize=12)

    # Desenare Turnuri
    for i in range(nr_x):
        x_pos = L_tech + (i * pas_x) + 0.2
        for yy in y_positions:
            ax.add_patch(plt.Circle((x_pos + D_bazin/2, yy + D_bazin/2), D_bazin/2, color='#2ecc71', alpha=0.6))

    # Magistrale Dinamice
    for my in magistrale_y:
        ax.plot([L_tech, L_sera - 0.5], [my, my], color='blue', lw=2)
        # Alimentare din Pompă (Traseu Perimetral)
        ax.plot([p_x, p_x, L_tech], [p_y, my, my], color='blue', lw=1.5, alpha=0.4)

    # Colectare Retur (Prin JOS)
    if magistrale_y:
        ax.plot([L_sera - 0.5, L_sera - 0.5], [max(magistrale_y), 0.15], color='cyan', lw=2)
        ax.plot([L_sera - 0.5, 0.7], [0.15, 0.15], color='cyan', lw=2, ls='--')
        ax.plot([0.7, 0.7], [0.15, 0.3], color='cyan', lw=2, ls='--')

    ax.set_aspect('equal')
    ax.set_xlim(-0.5, L_sera + 0.5)
    ax.set_ylim(-0.5, W_sera + 0.5)
    plt.title(f"Layout Smart Iterativ: {nr_x} coloane x {len(y_positions)} rânduri | Total {total_turnuri} Turnuri", pad=20)
    return fig
