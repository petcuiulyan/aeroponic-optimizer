import matplotlib.pyplot as plt
import matplotlib.patches as patches


def calculeaza_layout(L_utila, W_sera, pas_x, D_bazin, dist_y, culoar_min):
    nr_x = int(L_utila / pas_x)

    y_positions = []
    magistrale_y = []

    current_y = 0.5

    while current_y + D_bazin <= W_sera - 0.5:
        y_positions.append(current_y)
        magistrale_y.append(current_y + D_bazin / 2)

        current_y += D_bazin + dist_y + culoar_min

    total_turnuri = nr_x * len(y_positions)

    return nr_x, y_positions, magistrale_y, total_turnuri


def randeaza_2d(L, W, L_tech, nr_x, y_positions, pas_x, D):
    fig, ax = plt.subplots(figsize=(12, 6))

    ax.add_patch(patches.Rectangle((0, 0), L, W, fill=False))

    for i in range(nr_x):
        for y in y_positions:
            x = L_tech + i * pas_x
            ax.add_patch(plt.Circle((x, y), D / 2, color='green', alpha=0.5))

    ax.set_title("Layout Turnuri")
    ax.set_aspect('equal')

    return fig
``
