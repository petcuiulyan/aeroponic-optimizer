# automatizare.py
def necesar_senzori(nr_turnuri):
    return {
        "esp32_count": 1, 
        "senzori_ph_ec": 1, 
        "electrovalve_mari": 2, # Două valve principale (Sus/Jos)
        "relee_putere": 2,      # Pentru valvele de debit mare
        "metraj_cablu_date": nr_turnuri * 0.5, # Mai puțin cablu acum
        "senzori_hala": 2 
    }
