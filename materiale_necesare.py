# materiale_necesare.py

def calculeaza_deviz_detaliat(total_turnuri, nr_magistrale, L_sera, W_sera, H_sera):
    perimetru = 2 * (L_sera + W_sera)
    suprafata_mp = L_sera * W_sera
    
    # --- LOGICA NOUA CONFORM COMENTARIILOR TALE ---
    # PVC 25mm: Distanta de la pompa la M1, M2, M3 (estimat 1/3 din lungime per magistrala)
    pvc_25_dist = (L_sera * 0.3) * nr_magistrale 
    # PVC 20mm: Toata teava pentru magistralele propriu-zise
    pvc_20_dist = L_sera * nr_magistrale
    # Furtun 8mm: 0.5m per turn + 5% marja
    furtun_8_dist = (total_turnuri * 0.5) * 1.05
    
    # LED-uri: Minim 2 per turn
    led_total = total_turnuri * 2
    # Conectori separatie: 1 la 2 turnuri
    conectori = int(total_turnuri / 2)

    return {
        "🏗️ Structură Seră & Înveliș": {
            "Țeavă rectangulară stâlpi/grinzi (ml)": 138.0,
            "Țeavă rotundă arce (ml)": 138.6,
            "Contravântuiri (set)": 8.0,
            "Folie UV dublă (mp)": 450.0,
            "Ventilator mic pernă aer + Tub": 1.0,
            "Plasă umbrire + insecte (mp)": 296.0,
            "Sistem Cooling Pad": 1.0
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
            "Prize IP55": 107.0,
            "Conectori separație (1 la 2 turnuri)": float(conectori)
        }
    }

def genereaza_text_specificatii(deviz, total_t, L, W, H):
    text = f"=== FISA TEHNICA ACTUALIZATA - {total_t} TURNURI ===\n"
    text += f"Configuratie: {L}m x {W}m x {H}m\n"
    text += "="*45 + "\n\n"
    for cat, items in deviz.items():
        text += f"[{cat.upper()}]\n"
        for k, v in items.items():
            text += f" - {k}: {v}\n"
        text += "\n"
    return text
