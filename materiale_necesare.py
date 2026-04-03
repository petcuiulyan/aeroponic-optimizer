# materiale_necesare.py

def calculeaza_deviz_detaliat(total_turnuri, nr_magistrale, L_sera, W_sera, H_sera):
    """
    Formule dinamice bazate pe geometrie:
    """
    # --- CALCUL STRUCTURĂ (DINAMIC) ---
    nr_arce = int(L_sera / 2) + 1  # Un arc la fiecare 2 metri
    
    # Stâlpii: Înălțimea (H) influențează direct lungimea stâlpilor laterali
    # Presupunem 2 stâlpi per arc (stânga/dreapta)
    stalpi_ml = nr_arce * 2 * H_sera 
    
    # Grinzi longitudinale: 4 rânduri pe toată lungimea serei
    grinzi_ml = L_sera * 4 
    
    # Arce: Calculăm lungimea unui arc de cerc (aproximare 1.5 * lățime pentru boltă)
    arce_ml = nr_arce * (W_sera * 1.5)
    
    # Folia UV: Acoperă acoperișul (L * Arce_ml) + cele două fețe (W * H * 2)
    suprafata_folie = (L_sera * (W_sera * 1.6)) + (2 * (W_sera * H_sera))
    
    # Plasă insecte: Perimetrul serei * Înălțime
    plasa_ml = (2 * (L_sera + W_sera)) * 1.2 # marjă 20%

    # --- HIDRAULICĂ OPTIMIZATĂ ---
    pvc_25_dist = (L_sera * 0.3) * nr_magistrale 
    pvc_20_dist = L_sera * nr_magistrale
    furtun_8_dist = (total_turnuri * 0.5) * 1.05
    
    # LED-uri și Electrice
    led_total = total_turnuri * 2
    conectori = int(total_turnuri / 2)

    return {
        "🏗️ Structură Seră & Înveliș (Calculat din H)": {
            "Țeavă rectangulară stâlpi/grinzi (ml)": round(stalpi_ml + grinzi_ml, 1),
            "Țeavă rotundă arce (ml)": round(arce_ml, 1),
            "Contravântuiri (set)": 8.0,
            "Folie UV dublă (mp)": round(suprafata_folie * 1.1, 1), # +10% pierderi
            "Ventilator mic pernă aer + Tub": 1.0,
            "Plasă umbrire + insecte (mp)": round(plasa_ml, 1),
            "Sistem Cooling Pad": 1.0 if W_sera > 6 else 0.0
        },
        "💧 Sistem Hidraulic HPA": {
            "Turn hidroponic complet (40 plante)": float(total_turnuri),
            "Bazin IBC 1000L": 2.0,
            "Pompă HPA (Main)": 1.0,
            "Pompă transfer (IBC1 -> IBC2)": 1.0,
            "Țeavă PVC 25 mm (Pompă -> M)": round(pvc_25_dist, 1),
            "Țeavă PVC 20 mm (Magistrale M)": round(pvc_20_dist, 1),
            "Furtun 8mm (Legături turnuri)": round(furtun_8_dist, 1),
            "Miniflotoare": 2.0,
            "Robineți izolare turn": float(total_turnuri),
            "Seturi Racorduri/Coturi (incl. Retur)": 3.0
        },
        "⚡ Electrice & Automatizare": {
            "Tablou automatizare + ESP32": 1.0,
            "Senzori (CO2, Lux, Temp, Hum)": 1.0,
            "Iluminat LED Full Spectrum (2x/turn)": float(led_total),
            "Tester pH și EC industrial": 1.0,
            "Cablu principal + LED (m)": float(total_turnuri * 5),
            "Prize IP55": float(total_turnuri + 5),
            "Conectori separație (1 la 2 turnuri)": float(conectori)
        }
    }
