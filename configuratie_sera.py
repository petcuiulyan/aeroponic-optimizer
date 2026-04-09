# configuratie_sera.py
def get_dimensiuni_sera(L, W, H, L_tech):
    volum_total = L * W * H
    suprafata_utila = (L - L_tech) * W
    return {
        "volum": volum_total,
        "suprafata_utila": suprafata_utila,
        "L_utila": L - L_tech
    }

def zona_germinare(L_tech, W):
    # Estimăm capacitatea tăvilor de germinare în zona tehnică
    nr_tavi = int(total_turnuri*112/200) # 0.5mp per tavă
    return nr_tavi
