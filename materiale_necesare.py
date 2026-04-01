def calculeaza_deviz_complet(total_turnuri, nr_magistrale, L_sera, W_sera):
    # --- 1. HIDRAULICĂ (CONEXIUNI INDIVIDUALE) ---
    # Fiecare turn are propriul set de conexiuni
    robineti_izolare = total_turnuri  # 1 per turn
    teuri_pvc = total_turnuri * 2     # conexiune magistrală + bifurcație
    coturi_pvc = total_turnuri * 2    # direcționare spre duze
    duze_mist = total_turnuri * 2     # 2 duze per turn pentru acoperire 360
    cleme_fixare_teava = total_turnuri * 3 # fixare pe structura verticală
    furtun_presiune_m = total_turnuri * 2.5 # legătura între duze și robinet
    
    # --- 2. ELECTRICE (ALIMENTARE INDIVIDUALĂ) ---
    # 1 turn = 1 priză (pentru pompe individuale sau iluminat dedicat)
    prize_ip55 = total_turnuri + 8  # +8 pentru: 4 peristaltice, 1 pompa 120W, 1 router/PC, 2 extra
    stechere_mascul = total_turnuri + 5
    cablu_alimentare_m = (total_turnuri * 3.5) + (L_sera * 2) # estimare traseu turnuri + magistrală
    canal_cablu_m = L_sera * nr_magistrale
    tablou_electric = 1
    sigurante_automate = 6 # Grupate pe zone: Pompe, Peristaltice, Senzori, Lumini, Automatizare, General
    
    # --- 3. STRUCTURĂ ȘI RECIPIENTE ---
    bazine_colectoare_turn = total_turnuri
    teava_pvc_verticala_2m = total_turnuri # corpul turnului
    ibc_1000l = 2
    suport_metalic_turn = total_turnuri
    
    # --- 4. AUTOMATIZARE ȘI SENZORI ---
    pompe_peristaltice = 4
    kit_senzor_ph_ec = 1
    microcontroler_esp32 = 1
    modul_relee_8_canale = 1
    sursa_alimentare_12v = 2 # 1 pentru pompe, 1 pentru senzori/controler

    return {
        "Hidraulică (Instalație Turnuri)": {
            "Robineți sferă 1/2": robineti_izolare,
            "Duze pulverizare fine": duze_mist,
            "Teuri și fitinguri PVC": teuri_pvc,
            "Furtun presiune (m)": round(furtun_presiune_m, 1),
            "Cleme fixare": cleme_fixare_teava
        },
        "Electrice (Power & Control)": {
            "Prize IP55 (protecție apă)": prize_ip55,
            "Ștechere": stechere_mascul,
            "Cablu MYYM 3x1.5 (m)": round(cablu_alimentare_m, 1),
            "Canal cablu protecție (m)": round(canal_cablu_m, 1),
            "Siguranțe automate (buc)": sigurante_automate,
            "Tablou distribuție": tablou_electric
        },
        "Componente Turn": {
            "Teavă PVC Ø110/Ø160 (2m)": teava_pvc_verticala_2m,
            "Bazine colectoare baze": bazine_colectoare_turn,
            "Coșulețe (net pots) 40/turn": total_turnuri * 40
        },
        "Sistem Central": {
            "IBC 1000L": ibc_1000l,
            "Pompă presiune 120W": 1,
            "Pompe Peristaltice": pompe_peristaltice,
            "Senzori + Controler": 1
        }
    }
