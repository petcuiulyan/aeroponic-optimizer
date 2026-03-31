# distributie_turnuri.py
import matplotlib.pyplot as plt
import matplotlib.patches as patches

def calcul_pozitii(L_utila, W_sera, L_tech, pas_x, dist_y, D_bazin, culoar):
    nr_x = int(L_utila / pas_x)
    
    # Coordonate Y conform schiței tale (perechi cu magistrală pe mijloc)
    y_pereche_jos = [(W_sera/2 - culoar/2 - D_bazin), (W_sera/2 - culoar/2 - 2*D_bazin - dist_y)]
    y_pereche_sus = [(W_sera/2 + culoar/2), (W_sera/2 + culoar/2 + D_bazin + dist_y)]
    
    return nr_x, y_pereche_jos + y_pereche_sus

def randeaza_2d(L, W, L_tech, nr_x, y_linii, D_bazin, pas_x, culoar):
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.add_patch(patches.Rectangle((0,0), L, W, lw=2, ec='black', fc='none')) # Sera
    ax.add_patch(patches.Rectangle((0,0), L_tech, W, alpha=0.1, fc='blue')) # Tech
    
    for i in range(nr_x):
        x = L_tech + (i * pas_x)
        for y in y_linii:
            ax.add_patch(plt.Circle((x + D_bazin/2, y + D_bazin/2), D_bazin/2, color='#2ecc71'))
    
    ax.set_aspect('equal')
    return fig
