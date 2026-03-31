import matplotlib.pyplot as plt
import matplotlib.patches as patches

def calculeaza_layout(L_utila, W_sera, pas_x, D_bazin, dist_y, culoar):
    # 1. Calcul coloane pe lungime
    nr_x = int(L_utila / pas_x)
    
    # 2. Calcul câte "Unități de Perechi" încap pe lățime
    # O unitate = (Turn + Spațiu Magistrală + Turn) + Culoar
    latime_unitate_pereche = (D_bazin * 2) + dist_y + culoar
    nr_unitati_y = int(W_sera / latime_unitate_pereche)
    
    if nr_unitati_y == 0: nr_unitati_y = 1 # Siguranță minimă
    
    total_turnuri = nr_x * (nr_unitati_y * 2 * 2) # *2 rânduri/pereche *2 părți ale culoarului
    return nr_x, nr_unitati_y, total_turnuri

def randeaza_2d(L_sera, W_sera, L_tech, nr_x, nr_unit_y, pas_x, dist_y, D_bazin, culoar):
    fig, ax = plt.subplots(figsize=(16, 9))
    
    # --- 1. CONTUR & ZONĂ TEHNICĂ ---
    ax.add_patch(patches.Rectangle((0, 0), L_sera, W_sera, lw=3, ec='black', fc='none'))
    ax.add_patch(patches.Rectangle((0, 0), L_tech, W_sera, alpha=0.05, fc='gray'))

    # --- 2. IBC-URI (Rămân jos pentru estetică) ---
    ibc_s = 1.0
    ax.add_patch(patches.Rectangle((0.2, 0.3), ibc_s, ibc_s, fc='#a2d2ff', ec='blue', lw=2)) # IBC 2
    ax.add_patch(patches.Rectangle((0.2, 2.1), ibc_s, ibc_s, fc='#e0f2fe', ec='blue', lw=1.5)) # IBC 1
    
    p_x, p_y = L_tech - 0.4, 0.8 # Pompa HPA
    ax.plot(p_x, p_y, 'ro', markersize=12)

    # --- 3. LOGICA DE MULTIPLICARE PE LĂȚIME ---
    # Calculăm spațiul ocupat de o pereche dublă (Sus/Jos față de un culoar)
    # Desenăm grupuri de rânduri simetrice față de culoarele distribuite pe lățime
    pas_y_unitate = W_sera / (nr_unit_y + 1)
    
    magistrale_y = []

    for unit in range(1, nr_unit_y + 1):
        y_centru_culoar = unit * pas_y_unitate
        
        # Perechea de rânduri JOS față de culoar
        m_y_jos = y_centru_culoar - (culoar/2) - (D_bazin) - (dist_y/2)
        y_r1 = m_y_jos + (dist_y/2) 
        y_r2 = m_y_jos - (dist_y/2) - D_bazin
        
        # Perechea de rânduri SUS față de culoar
        m_y_sus = y_centru_culoar + (culoar/2) + (D_bazin) + (dist_y/2)
        y_r3 = m_y_sus - (dist_y/2) - D_bazin
        y_r4 = m_y_sus + (dist_y/2)

        y_linii_grup = [y_r1, y_r2, y_r3, y_r4]
        magistrale_y.extend([m_y_jos, m_y_sus])

        # Desenare Turnuri pentru acest grup
        for i in range(nr_x):
            x_pos = L_tech + (i * pas_x) + 0.2
            for idx, yy in enumerate(y_linii_grup):
                if 0 < yy < W_sera - D_bazin: # Verificăm să nu iasă din seră
                    ax.add_patch(plt.Circle((x_pos + D_bazin/2, yy + D_bazin/2), D_bazin/2, color='#2ecc71', alpha=0.6))
                    # Alimentare din magistrală
                    curr_m_y = m_y_jos if idx < 2 else m_y_sus
                    ax.plot([x_pos + D_bazin/2, x_pos + D_bazin/2], [yy + D_bazin/2, curr_m_y], color='blue', lw=0.5, alpha=0.3)

    # --- 4. MAGISTRALE & ALIMENTARE ---
    for my in magistrale_y:
        if 0 < my < W_sera:
            ax.plot([L_tech, L_sera - 0.5], [my, my], color='blue', lw=2)
            # Conexiune la Pompa HPA (Verticală de distribuție)
            ax.plot([p_x, p_x, L_tech], [p_y, my, my], color='blue', lw=1.5, alpha=0.6)

    # --- 5. RETUR (PRIN JOS) ---
    ax.plot([L_sera - 0.5, L_sera - 0.5], [min(magistrale_y), 0.15], color='cyan', lw=2)
    ax.plot([L_sera - 0.5, 0.7], [0.15, 0.15], color='cyan', lw=2, ls='--')
    ax.plot([0.7, 0.7], [0.15, 0.3], color='cyan', lw=2, ls='--')

    ax.set_aspect('equal')
    ax.set_xlim(-0.5, L_sera + 0.5)
    ax.set_ylim(-0.5, W_sera + 0.5)
    plt.title(f"Configurație Scalabilă: {nr_x} coloane x {nr_unit_y*4} rânduri", pad=20)
    
    return fig
