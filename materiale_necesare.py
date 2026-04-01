# materiale_necesare.py

def calculeaza_deviz_detaliat(total_turnuri, nr_magistrale, L_sera, W_sera):
    """
    Calculează necesarul de materiale 'la cheie' bazat pe configurația serei.
    Include fiecare robinet, clemă și priză individuală.
    """
    # --- 1. HIDRAULICĂ (CONEXIUNI INDIVIDUALE) ---
    # Fiecare turn are propriul set de conexiuni pentru mentenanță independentă
    robineti_izolare = total_turnuri  # 1 robinet per turn
    teuri_pvc = total_turnuri * 2     # conexiune magistrală + bifurcație
    coturi_pvc = total_turnuri * 2    # direcționare spre duze
    duze_mist = total_turnuri * 2     # 2 duze per turn pentru acoperire 360
    cleme_fixare_teava = total_turnuri * 3 # fixare pe structura verticală
    furtun_presiune_m = total_turnuri * 2.5 # legătura între duze și robinet
    
    # --- 2. ELECTRICE (ALIMENTARE INDIVIDUALĂ) ---
    # 1 turn = 1 priză (pentru pompe individuale sau iluminat dedicat)
    # Protecție IP55 obligatorie pentru mediu umed
    prize_ip55 = total_turnuri + 8  # +8 pentru: 4 peristaltice, 1 pompa 120W, 1 router/PC, 2 extra
    stechere_mascul = total_turnuri + 5
    # Calcul cablu: 3.5m per turn + lungimea magistralelor
    cablu_alimentare_m = (total_turnuri * 3.5) + (L_sera * 2) 
    canal_cablu_m = L_sera * nr_magistrale
    tablou_electric = 1
    sigurante_automate = 6 # Grupate: Pompe, Peristaltice, Senzori, Lumini, Automatizare, General
    
    # --- 3. STRUCTURĂ ȘI RECIPIENTE ---
    bazine_colectoare_turn = total_turnuri
    teava_pvc_verticala_2m = total_turnuri # corpul turnului (Ø110 sau Ø160)
    ibc_1000l = 2 # 1 stoc, 1 prep
    suport_metalic_turn = total_turnuri
    
    # --- 4. AUTOMATIZARE ȘI SENZORI ---
    pompe_peristaltice = 4
    kit_senzor_ph_ec = 1
    microcontroler_esp32 = 1
    modul_relee_8_canale = 1
    sursa_alimentare_12v = 2 # 1 pentru pompe, 1 pentru senzori/controler

    return {
        "Hidraulică (Instalație Turnuri)": {
            "Robineți sferă 1/2 (izolare per turn)": robineti_izolare,
            "Duze pulverizare fine (Mist)": duze_mist,
            "Teuri și fitinguri PVC 20mm": teuri_pvc,
            "Coturi PVC 20mm": coturi_pvc,
            "Furtun presiune (m)": round(furtun_presiune_m, 1),
            "Cleme fixare rapidă": cleme_fixare_teava
        },
        "Electrice (Power & Control IP55)": {
            "Prize IP55 (protecție umiditate)": prize_ip55,
            "Ștechere IP44": stechere_mascul,
            "Cablu MYYM 3x1.5 (m)": round(cablu_alimentare_m, 1),
            "Canal cablu / Tub cofrat (m)": round(canal_cablu_m, 1),
            "Siguranțe automate (linii separate)": sigurante_automate,
            "Tablou distribuție central": tablou_electric
        },
        "Componente Structură Turn": {
            "Teavă PVC Ø110/Ø160 (2m)": teava_pvc_verticala_2m,
            "Bazine colectoare (bază turn)": bazine_colectoare_turn,
            "Coșulețe (net pots) 40/turn": total_turnuri * 40,
            "Suport metalic / fixare turn": suport_metalic_turn
        },
        "Sistem Central & Automatizare": {
            "IBC 1000L (Stocare & Nutrienți)": ibc_1000l,
            "Pompă presiune HPA 120W": 1,
            "Pompe Peristaltice (A, B, pH+, pH-)": pompe_peristaltice,
            "Senzori pH/EC + Controler ESP32": 1,
            "Surse alimentare 12V DC": sursa_alimentare_12v
        }
    }
