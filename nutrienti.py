# nutrienti.py

def calculeaza_dozare_precisa(ph_actual, ec_actual, ph_lim, ec_lim, volum_maxim=700):
    """
    Algoritm de calcul pentru dozare controlată (abordare cu minus).
    Returnează secundele de funcționare pentru fiecare pompă.
    """
    # Parametri tehnici
    raport_nutrienti_ml_l = 0.9  # 9ml la 10L (limita de siguranță)
    debit_pompa_ml_s = 1.0       # Presupunem 1ml/secundă
    factor_siguranta = 0.3       # Corectăm doar 30% din deficit pe iterație
    
    comenzi_pompe = {
        "Peristaltică A": 0.0,
        "Peristaltică B": 0.0,
        "Peristaltică pH UP": 0.0,
        "Peristaltică pH DOWN": 0.0
    }
    
    # --- CALCUL EC ---
    if ec_actual < ec_lim[0]: # ec_lim[0] este limita inferioară (ex: 1.1)
        # Calculăm deficitul relativ față de țintă
        deficit_relativ = (ec_lim[0] - ec_actual) / ec_lim[0]
        
        # Cantitatea teoretică pentru volumul de 700L la raportul stabilit
        ml_teoretic = volum_maxim * raport_nutrienti_ml_l
        
        # Aplicăm deficitul și factorul de siguranță
        ml_de_injectat = ml_teoretic * deficit_relativ * factor_siguranta
        
        secunde = round(ml_de_injectat / debit_pompa_ml_s, 1)
        comenzi_pompe["Peristaltică A"] = secunde
        comenzi_pompe["Peristaltică B"] = secunde

    # --- CALCUL pH ---
    # Estimare: 2ml soluție corectoare per 0.1 unitate pH la 700L
    if ph_actual > ph_lim[1]: # pH prea mare (necesită DOWN)
        deficit_ph = ph_actual - ph_lim[1]
        ml_ph = (deficit_ph / 0.1) * 1.5 * factor_siguranta # 1.5ml per 0.1 pH
        comenzi_pompe["Peristaltică pH DOWN"] = round(ml_ph / debit_pompa_ml_s, 1)
        
    elif ph_actual < ph_lim[0]: # pH prea mic (necesită UP)
        deficit_ph = ph_lim[0] - ph_actual
        ml_ph = (deficit_ph / 0.1) * 1.5 * factor_siguranta
        comenzi_pompe["Peristaltică pH UP"] = round(ml_ph / debit_pompa_ml_s, 1)

    return comenzi_pompe
