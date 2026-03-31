# nutrienti.py
def calcul_hidraulic(nr_turnuri, L_magistrala):
    # 40 plante/turn, fiecare turn are nevoie de aprox 2L/min în ciclu de ceață
    debit_necesar_lpm = nr_turnuri * 0.1 # estimat pentru duze HPA
    return {
        "ibc_count": 2, # Standard conform schiței tale
        "lungime_magistrala_apa": L_magistrala * 2,
        "debit_pompa_recomandat": debit_necesar_lpm * 1.2 # +20% rezervă
    }
