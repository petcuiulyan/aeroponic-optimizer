import matplotlib.pyplot as plt
import matplotlib.patches as patches

def calculeaza_layout(L_utila, pas_x):
    nr_x = int(L_utila / pas_x)
    return nr_x, nr_x * 4

def randeaza_2d(L_sera, W_sera, L_tech, nr_x, pas_x, dist_y, D_bazin, culoar):
    fig, ax = plt.subplots(figsize=(14, 8))
    
    # --- 1. CONTUR SERĂ ---
    ax.add_patch(patches.Rectangle((0, 0), L_sera, W_sera, lw=3, ec='black', fc='none'))
    
    # --- 2. ZONA TEHNICĂ COMPACTĂ (IBC-uri la 1m distanță) ---
    ax.add_patch(patches.Rectangle((0, 0), L_tech, W_sera, alpha=0.05, fc='gray'))
    
    ibc_w, ibc_l = 1.0, 1.0
    # Poziționăm IBC-urile pe verticală cu distanță de ~1m între ele
    y_ibc2 = (W_sera / 2) - 1.2  # IBC 2 mai jos de centru
    y_ibc1 = y_ibc2 + ibc_w + 1.0 # IBC 1 la 1 metru deasupra lui IBC 2
    
    # IBC 1 (Nutrienți)
    ax.add_patch(patches.Rectangle((0.2, y_ibc1), ibc_l, ibc_w, fc='#a2d2ff', ec='blue', lw=2))
    ax.text(0.7, y_ibc1 + 0.5, "IBC 1\n(PREP)", ha='center', fontsize=8, fontweight='bold')
    
    # IBC 2 (Buffer/Retur)
    ax.add_patch(patches.Rectangle((0.2, y_ibc2), ibc_l, ibc_w, fc='#a2d2ff', ec='blue', lw=2))
    ax.text(0.7, y_ibc2 + 0.5, "IBC 2\n(STOCK)", ha='center', fontsize=8, fontweight='bold')

    # POMPA TRANSFER (Între ele)
    ax.plot([0.7, 0.7], [y_ibc1, y_ibc2 + ibc_w], color='darkblue', lw=2, ls=':')
    ax.plot(0.7, (y_ibc1 + y_ibc2 + ibc_w)/2, 'go', markersize=7)

    # POMPA PRINCIPALĂ 20 BAR (Plasată estetic lângă IBC 2)
    p_main_x, p_main_y = L_tech - 0.4, y_ibc2 + 0.5
    ax.plot(p_main_x, p_main_y, 'ro', markersize=12)
    ax.text(p_main_x, p_main_y - 0.4, "POMPA HPA", ha='center', color='red', fontsize=8, fontweight='bold')
    
    # Conexiune scurtă IBC 2 -> Pompă
    ax.plot([0.2 + ibc_l, p_main_x], [y_ibc2 + 0.5, p_main_y], color='blue', lw=2)

    # --- 3. CONFIGURARE RÂNDURI ȘI MAGISTRALE ---
    y_jos_ext = (W_sera / 2) - (culoar / 2) - D_bazin - dist_y - D_bazin
    y_jos_int = (W_sera / 2) - (culoar / 2) - D_bazin
    y_sus_int = (W_sera / 2) + (culoar / 2)
    y_sus_ext = (W_sera / 2) + (culoar / 2) + D_bazin + dist_y
    
    mag_y_jos = y_jos_int - (dist_y / 2)
    mag_y_sus = y_sus_int + D_bazin + (dist_y / 2)

    # ALIMENTARE (Pompă -> Magistrale) - Traseu perimetral estetic
    ax.plot([p_main_x, p_main_x, L_tech], [p_main_y, mag_y_jos, mag_y_jos], color='blue', lw=2.5)
    ax.plot([p_main_x, p_main_x, L_tech], [p_main_y, mag_y_sus, mag_y_sus], color='blue', lw=2.5)

    # ELECTROVALVE (La intrare)
    ax.plot(L_tech, mag_y_jos, 'rs', markersize=8)
    ax.plot(L_tech, mag_y_sus, 'rs', markersize=8)

    # --- 4. TURNURI ---
    for i in range(nr_x):
        x_pos = L_tech + (i * pas_x) + 0.2
        for idx, y in enumerate([y_jos_ext, y_jos_int, y_sus_int, y_sus_ext]):
            ax.add_patch(plt.Circle((x_pos + D_bazin/2, y + D_bazin/2), D_bazin/2, color='#2ecc71', alpha=0.6))
            t_mag_y = mag_y_jos if idx < 2 else mag_y_sus
            ax.plot([x_pos + D_bazin/2, x_pos + D_bazin/2], [y + D_bazin/2, t_mag_y], color='blue', lw=0.5)

    # MAGISTRALELE (Linii principale)
    ax.plot([L_tech, L_sera - 0.5], [mag_y_jos, mag_y_jos], color='blue', lw=2.5)
    ax.plot([L_tech, L_sera - 0.5], [mag_y_sus, mag_y_sus], color='blue', lw=2.5)

    # --- 5. RETUR RECIRCULARE (Legătura de final) ---
    # Unim cele două magistrale la capătul serei
    ax.plot([L_sera - 0.5, L_sera - 0.5], [mag_y_jos, mag_y_sus], color='cyan', lw=2, label='Circuit Retur')
    
    # Linia de întoarcere către IBC 2 (pe sub culoarul central sau lateral)
    # O desenăm pe lateralul de sus pentru a nu aglomera mijlocul
    ax.plot([L_sera - 0.5, L_tech, 0.7], [W_sera - 0.2, W_sera - 0.2, y_ibc2 + ibc_w], 
            color='cyan', lw=1.5, ls='--', alpha=0.7)
    ax.text(L_sera/2, W_sera - 0.15, "CONDUCTĂ COLECTARE RETUR", ha='center', fontsize=7, color='darkcyan')

    # --- 6. FINALIZARE ---
    ax.set_aspect('equal')
    ax.set_xlim(-0.5, L_sera + 0.5)
    ax.set_ylim(-0.5, W_sera + 0.5)
    return fig
