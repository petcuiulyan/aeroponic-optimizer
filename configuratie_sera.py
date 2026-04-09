# configuratie_sera.py

def get_dimensiuni_sera(L, W, H, L_tech):
    volum_total = L * W * H
    suprafata_utila = (L - L_tech) * W
    return {
        "volum": volum_total,
        "suprafata_utila": suprafata_utila,
        "L_utila": L - L_tech
    }

def zona_germinare(total_turnuri, L_tech, W):
    """
    Estimăm capacitatea tăvilor de germinare în zona tehnică.
    Am adăugat 'total_turnuri' ca argument pentru a repara eroarea.
    """
    try:
        # Calcul: (Număr total plante / 200 plante per tavă) 
        # unde 112 este nr de plante/turn (din contextul tău)
        nr_tavi = (float(total_turnuri) * 112) / 200 
        return round(nr_tavi, 2)
    except (ValueError, TypeError):
        return 0
