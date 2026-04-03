# materiale_necesare.py

def calculeaza_deviz_detaliat(total_turnuri, nr_magistrale, L_sera, W_sera, H_sera):
    """
    Generează un deviz complet bazat pe lista extinsă de piese.
    Include structură, climă, hidraulică și automatizare avansată.
    """
    
    # --- 1. STRUCTURĂ METALICĂ ȘI ÎNVELIȘ ---
    perimetru = 2 * (L_sera + W_sera)
    suprafata_folie = (L_sera * W_sera * 1.5) + (perimetru * H_sera) # estimare cu boltă
    
    # --- 2. CLIMATIZARE ȘI VENTILAȚIE ---
    nr_ventilatoare_evacuare = 1 if (L_sera * W_sera) < 100 else 2
    nr_ventilatoare_recirculare = int(L_sera / 5) # un ventilator la fiecare 5m
    
    # --- 3. HIDRAULICĂ (DETALIATĂ) ---
    lungime_magistrala_25mm = L_sera * nr_magistrale
    lungime_retur_20mm = L_sera + W_sera
    nr_miniflotoare = 2 # unul per IBC
    
    # --- 4. ILUMINAT ȘI ELECTRICE ---
    nr_corpuri_led = total_turnuri # 1 corp Full Spectrum vertical per turn
    
    return {
        "🏗️ Structură și Înveliș (Sera)": {
            "Țeavă rectangulară (Stâlpi/Grinzi) - ml": round(perimetru * 3, 1),
            "Țeavă rotundă (Arce) - ml": round(L_sera * 2.5, 1),
            "Folie UV dublă (pernă aer) - mp": round(suprafata_folie * 1.2, 1),
            "Ventilator mic pernă aer": 1,
            "Plasă insecte laterală (ml)": perimetru,
            "Plasă umbrire (mp)": L_sera * W_sera
        },
        "❄️ Climatizare și Cooling": {
            "Ventilator evacuare mare": nr_ventilatoare_evacuare,
            "Ventilator recirculare interior": nr_ventilatoare_recirculare,
            "Sistem Cooling Pad (set)": 1 if W_sera > 8 else 0,
            "Pompă recirculare cooling": 1 if W_sera > 8 else 0
        },
        "💧 Sistem Hidraulic HPA": {
            "Turnuri hidroponice complete": total_turnuri,
            "IBC 1000L (Stocare/Prep)": 2,
            "Pompă HPA 120W (Main)": 1,
            "Pompă transfer (IBC1 -> IBC2)": 1,
            "Țeavă PVC 25mm (Magistrale) - m": round(lungime_magistrala_25mm, 1),
            "Țeavă PVC 20mm (Retur) - m": round(lungime_retur_20mm, 1),
            "Furtun 8mm (Conexiuni turn) - m": total_turnuri * 2.5,
            "Miniflotoare (control nivel)": nr_miniflotoare,
            "Robineți și Racorduri (set)": total_turnuri + 10
        },
        "💡 Iluminat și Automatizare Pro": {
            "LED Full Spectrum Vertical": nr_corpuri_led,
            "Tablou automatizare complet": 1,
            "ESP32 + Relee + Surse": 1,
            "Senzor CO2 / Lumină / Temp-Hum": 1,
            "Tester pH și EC industrial": 1,
            "Pompe peristaltice (A/B/pH+/pH-)": 4,
            "Prize și Întrerupătoare (set)": total_turnuri + 10
        }
    }

def genereaza_text_specificatii(deviz, total_t, L, W):
    text = f"=== PROIECT TEHNIC SERA AEROPONICA ===\n"
    text += f"Configuratie: {total_t} turnuri | Suprafata: {L*W}mp\n\n"
    for cat, mat in deviz.items():
        text += f"[{cat}]\n"
        for k, v in mat.items():
            text += f" - {k}: {v}\n"
        text += "\n"
    return text
