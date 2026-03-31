# automatizare.py
def necesar_senzori(nr_turnuri):
    return {
        "esp32_count": 1, 
        "senzori_ph_ec": 1, # În IBC1
        "electrovalve": int(nr_turnuri / 2), # 1 per pereche
        "metraj_cablu_date": nr_turnuri * 1.5,
        "senzori_hala": 2 # Temp/Hum în extremități
    }
