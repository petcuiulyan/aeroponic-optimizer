def calculeaza_materiale(L, W, H, total_turnuri, lungime_magistrale):
    # 1. STRUCTURA
    suprafata_ext = (2 * L * H) + (2 * W * H) + (L * W) # Estimare brută
    profile_metalice_m = (L + W + H) * 10 # Coeficient de densitate structură
    
    # 2. SISTEM AEROPONIC
    teava_pvc_turnuri_m = total_turnuri * 2.0 # 2 metri per turn
    cosulete = total_turnuri * 40
    duze = total_turnuri * 2
    
    # 3. HIDRAULICA
    magistrale_total_m = lungime_magistrale * 1.1 # cu marjă
    
    return {
        "Structura": {
            "Policarbonat (mp)": round(suprafata_ext, 2),
            "Profile metalice (m)": round(profile_metalice_m, 1)
        },
        "Sistem Cultură": {
            "Total Turnuri": total_turnuri,
            "Total Locuri Plantare": cosulete,
            "Teavă PVC verticală (m)": teava_pvc_turnuri_m
        },
        "Hidraulica": {
            "Magistrale (m)": round(magistrale_total_m, 1),
            "Duze Mist": duze,
            "Pompe Peristaltice": 4,
            "IBC 1000L": 2
        }
    }
