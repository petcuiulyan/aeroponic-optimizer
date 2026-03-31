import matplotlib.pyplot as plt
import matplotlib.patches as patches

def calculeaza_layout(L_utila, W_sera, pas_x, D_bazin, dist_y, culoar_min):
    nr_x = int(L_utila / pas_x)
    
    # --- LOGICA SMART PE LĂȚIME ---
    y_positions = []
    magistrale_y = []
    
    # 1. Plasăm prima pereche jos (lângă perete)
    y_r1 = 0.5 # mic buffer de perete
    y_r2 = y_r1 + D_bazin + dist_y
    mag_y_jos = y_r1 + D_bazin + (dist_y/2)
    y_positions.extend([y_r1, y_r2])
    magistrale_y.append(mag_y_jos)
    
    # 2. Plasăm ultima pereche sus (lângă perete)
    y_r4 = W_sera - 0.5 - D_bazin
    y_r3 = y_r4 - dist_y - D_bazin
    mag_y_sus = y_r4 - (dist_y/2)
    y_positions.extend([y_r3, y_r4])
    magistrale_y.append(mag_y_sus)
    
    # 3. Calculăm spațiul rămas pe mijloc între perechea de jos și cea de sus
    spatiu_mijloc = y_r3 - (y_r2 + D_bazin)
    
    # 4. Decizia Smart
    # Dacă spațiul este între 1.5m și 2.5m, îl lăsăm ca și culoar principal
    # Dacă spațiul depășește 2.5m, mai inserăm un rând sau o pereche
    if spatiu_mijloc > 2.5:
        # Mai încape o pereche pe mijloc
        y_centru = W_sera / 2
        y_r_mid1 = y_centru - (dist_y/2) - D_bazin
        y_r_mid2 = y_centru + (dist_y/2)
        y_positions.extend([y_r_mid1, y_r_mid2])
        magistrale_y.append(y_centru)
    elif spatiu_mijloc > 1.8:
        # Spatiu mare, dar nu de pereche? Punem un singur rând central
        y_r_mid = (W_sera / 2) - (D_bazin / 2)
        y_positions.append(y_r_mid)
        magistrale_y.append(y_r_mid + D_bazin/2)

    total_turnuri = nr_x * len(y_positions)
    return nr_x, y_positions, magistrale_y, total_turnuri

def randeaza_2d(L_sera, W_sera, L_tech, nr_x, y_positions, magistrale_y, pas_x, D_bazin):
    fig, ax = plt.subplots(figsize=(16, 9))
    
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
        # Alimentare din Pompă
        ax.plot([p_x, p_x, L_tech], [p_y, my, my], color='blue', lw=1.5, alpha=0.5)

    # Colectare Retur (Prin JOS)
    ax.plot([L_sera - 0.5, L_sera - 0.5], [max(magistrale_y), 0.15], color='cyan', lw=2)
    ax.plot([L_sera - 0.5, 0.7], [0.15, 0.15], color='cyan', lw=2, ls='--')
    ax.plot([0.7, 0.7], [0.15, 0.3], color='cyan', lw=2, ls='--')

    ax.set_aspect('equal')
    ax.set_xlim(-0.5, L_sera + 0.5)
    ax.set_ylim(-0.5, W_sera + 0.5)
    return fig
