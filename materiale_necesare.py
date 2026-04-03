# materiale_necesare.py

def calculeaza_deviz_detaliat(total_turnuri, nr_magistrale, L_sera, W_sera, H_sera):
    """
    Generează devizul bazat pe lista TA de materiale.
    Include acum calcule pentru structură, climă și electrice.
    """
    perimetru = 2 * (L_sera + W_sera)
    suprafata_mp = L_sera * W_sera
    
    # --- CALCULE STRUCTURĂ ---
    nr_arce = int(L_sera / 2) + 1 # un arc la fiecare 2 metri
    
    return {
        "🏗️ Structură Seră & Înveliș": {
            "Țeavă rectangulară stâlpi/grinzi (ml)": round(perimetru * 2 + (nr_arce * 2), 1),
            "Țeavă rotundă arce (ml)": round(nr_arce * W_sera * 1.4, 1), # calcul arcadă
            "Contravântuiri (set)": 8,
            "Folie UV dublă (mp)": round(suprafata_mp * 2.5, 1),
            "Ventilator mic pernă aer + Tub": 1,
            "Plasă umbrire + Plasă insecte (mp)": round(suprafata_mp + (perimetru * 2), 1),
            "Sistem Cooling Pad": 1 if W_sera > 6 else 0
        },
        "💧 Sistem Hidroponic & Hidraulic": {
            "Turn hidroponic - complet (40 plante)": total_turnuri,
            "Bazin IBC 1000L": 2,
            "Pompă recirculare magistrale (HPA)": 1,
            "Pompă transfer (IBC1 -> IBC2)": 1,
            "Țeavă PVC 25 mm (m)": round(L_sera * nr_magistrale, 1),
            "Țeavă PVC 20 mm (m)": round(L_sera + W_sera, 1),
            "Furtun 8mm (m)": total_turnuri * 2.5,
            "Miniflotoare + Robineți": total_turnuri + 2,
            "Racorduri, Coturi, Reducții (set)": 1 
        },
        "⚡ Electrice & Automatizare": {
            "Tablou automatizare + ESP32": 1,
            "Senzori (CO2, Umiditate, Temp, Lumină)": 1,
            "Iluminat LED Full Spectrum (buc)": total_turnuri,
            "Tester pH și EC (industrial)": 1,
            "Temporizator LED + Relee": 1,
            "Cablu principal + Cablu LED (m)": round(total_turnuri * 5, 1),
            "Siguranțe (General, 16A, 10A)": 6,
            "Prize + Întrerupătoare": total_turnuri + 5
        }
    }

def genereaza_text_specificatii(deviz, total_t, L, W, H):
    """Generează conținutul pentru fișierul .txt"""
    text = f"FISA TEHNICA SERA - {total_t} TURNURI\n"
    text += f"Configuratie: {L}m x {W}m x {H}m\n"
    text += "="*40 + "\n\n"
    for cat, mat in deviz.items():
        text += f"[{cat.upper()}]\n"
        for k, v in mat.items():
            text += f" - {k}: {v}\n"
        text += "\n"
    return text
