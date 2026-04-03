# materiale_necesare.py

def calculeaza_deviz_detaliat(total_turnuri, nr_magistrale, L_sera, W_sera, H_sera):
    """
    Generează devizul actualizat cu observațiile tehnice:
    - LED-uri duble per turn
    - Magistrale optimizate (distanța pompă -> M1, M2, M3)
    - Conectori de separație pentru prize
    """
    # 1. HIDRAULICĂ OPTIMIZATĂ
    # Magistrale: acoperă doar distanța de la pompa HPA la punctele de distribuție M
    # L_sera * nr_magistrale este acum calculat mai precis
    lungime_pvc_25mm = (L_sera * 0.3) * nr_magistrale # aproximare distanță pompă -> coloane
    lungime_pvc_20mm = L_sera * nr_magistrale # teava efectivă pentru M1, M2, M3
    # Furtun 8mm: 0.5m/turn + 5% marjă
    lungime_furtun_8mm = (total_turnuri * 0.5) * 1.05

    # 2. ELECTRICE & LED (DUBLU)
    led_full_spectrum = total_turnuri * 2 # Conform notei tale: minim 2 la turn
    # Prize: 1 la 4 turnuri + conectori
    nr_conectori_separatie = int(total_turnuri / 2) # cel puțin 1 la 2 turnuri

    return {
        "🏗️ Structură Seră & Înveliș": {
            "Țeavă rectangulară stâlpi/grinzi (ml)": 138.0,
            "Țeavă rotundă arce (ml)": 138.6,
            "Contravântuiri (set)": 8,
            "Folie UV dublă (mp)": 450.0,
            "Ventilator mic pernă aer + Tub": 1,
            "Plasă umbrire + Plasă insecte (mp)": 296.0,
            "Sistem Cooling Pad": 1
        },
        "💧 Sistem Hidroponic & Hidraulic": {
            "Turn hidroponic - complet (40 plante)": total_turnuri,
            "Bazin IBC 1000L": 2,
            "Pompă HPA (Main)": 1,
            "Pompă transfer (IBC1 -> IBC2)": 1,
            "Țeavă PVC 25 mm (Pompă -> M)": round(lungime_pvc_25mm, 1),
            "Țeavă PVC 20 mm (M1, M2, M3)": round(lungime_pvc_20mm, 1),
            "Furtun 8mm (Legături turnuri)": round(lungime_furtun_8mm, 1),
            "Miniflotoare + Robineți": total_turnuri + 2,
            "Seturi Racorduri/Coturi (inclusiv retur)": 3 # 3 seturi conform notei tale
        },
        "⚡ Electrice & Automatizare": {
            "Tablou automatizare + ESP32": 1,
            "Senzori (CO2, Umiditate, Temp, Lumină)": 1,
            "Iluminat LED Full Spectrum": led_full_spectrum,
            "Tester pH și EC industrial": 1,
            "Cablu principal + Cablu LED (m)": total_turnuri * 5,
            "Siguranțe (General, 16A, 10A)": 6,
            "Prize IP55": 107,
            "Conectori separație (1 la 2 turnuri)": nr_conectori_separatie
        }
    }

def genereaza_text_specificatii(deviz_final, total_t, L, W, H):
    text = f"=== PROIECT TEHNIC ACTUALIZAT: {total_t} TURNURI ===\n"
    text += f"Dimensiuni: {L}m x {W}m x {H}m\n\n"
    for cat, items in deviz_final.items():
        text += f"[{cat}]\n"
        for nume, cant in items.items():
            text += f" - {nume}: {cant}\n"
        text += "\n"
    return text
