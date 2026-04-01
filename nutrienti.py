# nutrienti.py

def calcul_hidraulic(nr_turnuri, L_magistrala):
    # 40 plante/turn, fiecare turn are nevoie de aprox 2L/min în ciclu de ceață
    debit_necesar_lpm = nr_turnuri * 0.1 # estimat pentru duze HPA
    return {
        "ibc_count": 2, # Standard conform schiței tale
        "lungime_magistrala_apa": L_magistrala * 2,
        "debit_pompa_recomandat": debit_necesar_lpm * 1.2 # +20% rezervă
    }

def calculeaza_dozare_precisa(ph_actual, ec_actual, ph_lim, ec_lim, volum_maxim=700):
    """Algoritm bazat pe raportul de 9ml/10L și volum de lucru de 700L"""
    raport_ml_l = 0.9  # 9ml la 10L
    debit_s = 1.0      # Presupunem 1ml/s debit pompă
    f_siguranta = 0.3  # Dozăm doar 30% din deficit pentru siguranță
    
    # Folosim denumirile EXACTE ale pompelor din clasa AutomatizareSera
    timpi = {
        "Peristaltică A": 0.0,
        "Peristaltică B": 0.0,
        "Peristaltică pH UP": 0.0,
        "Peristaltică pH DOWN": 0.0
    }
    
    # Calcul EC (Nutrienți A+B)
    if ec_actual < ec_lim[0]:
        deficit = (ec_lim[0] - ec_actual) / ec_lim[0]
        ml_necesar = (volum_maxim * raport_ml_l) * deficit * f_siguranta
        timpi["Peristaltică A"] = timpi["Peristaltică B"] = round(ml_necesar / debit_s, 1)

    # Calcul pH
    if ph_actual > ph_lim[1]: # pH prea mare
        deficit_ph = ph_actual - ph_lim[1]
        ml_acid = (deficit_ph / 0.1) * 1.5 * f_siguranta # 1.5ml per 0.1 unitate pH la 700L
        timpi["Peristaltică pH DOWN"] = round(ml_acid / debit_s, 1)
    elif ph_actual < ph_lim[0]: # pH prea mic
        deficit_ph = ph_lim[0] - ph_actual
        ml_baza = (deficit_ph / 0.1) * 1.5 * f_siguranta
        timpi["Peristaltică pH UP"] = round(ml_baza / debit_s, 1)
        
    return timpi
