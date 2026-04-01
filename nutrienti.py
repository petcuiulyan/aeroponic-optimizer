def calcul_hidraulic(nr_turnuri, L_magistrala):
    # 40 plante/turn
    debit_necesar_lpm = nr_turnuri * 0.1 
    return {
        "ibc_count": 2,
        "lungime_magistrala_apa": L_magistrala * 2,
        "debit_pompa_recomandat": debit_necesar_lpm * 1.2 
    }

def calculeaza_dozare_precisa(ph_actual, ec_actual, ph_lim, ec_lim, volum_maxim=700):
    """
    Calcul bazat pe raportul tău: 9ml/10L (0.9ml/L).
    Dozăm doar 30% din deficit pentru a lăsa spațiu de omogenizare.
    """
    RAPORT_ML_L = 0.9
    DEBIT_S = 1.0  # 1ml/s
    FACTOR_SIGURANTA = 0.3
    
    timpi = {
        "Peristaltică A": 0.0,
        "Peristaltică B": 0.0,
        "Peristaltică pH UP": 0.0,
        "Peristaltică pH DOWN": 0.0
    }
    
    # Calcul Nutrienți (EC)
    if ec_actual < ec_lim[0]:
        deficit = (ec_lim[0] - ec_actual) / ec_lim[0]
        ml_injectie = (volum_maxim * RAPORT_ML_L) * deficit * FACTOR_SIGURANTA
        timpi["Peristaltică A"] = timpi["Peristaltică B"] = round(ml_injectie / DEBIT_S, 1)

    # Calcul pH
    if ph_actual > ph_lim[1]:
        delta = ph_actual - ph_lim[1]
        ml_acid = (delta / 0.1) * 1.5 * FACTOR_SIGURANTA # 1.5ml per 0.1 pH unit
        timpi["Peristaltică pH DOWN"] = round(ml_acid / DEBIT_S, 1)
    elif ph_actual < ph_lim[0]:
        delta = ph_lim[0] - ph_actual
        ml_baza = (delta / 0.1) * 1.5 * FACTOR_SIGURANTA
        timpi["Peristaltică pH UP"] = round(ml_baza / DEBIT_S, 1)
        
    return timpi
