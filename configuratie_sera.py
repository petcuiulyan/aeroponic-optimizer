import config

def calculeaza_inaltime(W):
    """
    Înălțime automată structură tip tunel (30% din lățime)
    """
    return round(W * 0.3, 2)


def get_dimensiuni_sera(L, W):
    H = calculeaza_inaltime(W)
    L_utila = L - config.DEFAULT_DIMENSIONS["tech_zone"]

    return {
        "L": L,
        "W": W,
        "H": H,
        "L_utila": L_utila,
        "suprafata": round(L * W, 2)
    }
