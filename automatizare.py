class AutomatizareSera:
    def __init__(self):
        # Intervalele tale specifice
        self.ph_min, self.ph_max = 5.9, 6.5
        self.ec_min, self.ec_max = 1.1, 1.6
        
        # Stări pompe (True = pornit, False = oprit)
        self.status = {
            "Peristaltică A": False,
            "Peristaltică B": False,
            "Peristaltică pH UP": False,
            "Peristaltică pH DOWN": False,
            "Pompă 120W": False
        }

    def proceseaza_dozare_automata(self, ph_actual, ec_actual):
        """Logica de dozare bazată pe intervale (Range)"""
        mesaje = []
        
        # --- Logica pH (5.9 - 6.5) ---
        if ph_actual < self.ph_min:
            self.status["Peristaltică pH UP"] = True
            self.status["Peristaltică pH DOWN"] = False
            mesaje.append("⬆️ pH prea mic! Dozare pH UP activă.")
        elif ph_actual > self.ph_max:
            self.status["Peristaltică pH DOWN"] = True
            self.status["Peristaltică pH UP"] = False
            mesaje.append("⬇️ pH prea mare! Dozare pH DOWN activă.")
        else:
            self.status["Peristaltică pH UP"] = False
            self.status["Peristaltică pH DOWN"] = False
            mesaje.append("✅ pH în interval optim.")

        # --- Logica EC (1.1 - 1.6) ---
        if ec_actual < self.ec_min:
            self.status["Peristaltică A"] = True
            self.status["Peristaltică B"] = True
            mesaje.append("🧪 EC scăzut! Dozare Soluție A + B activă.")
        elif ec_actual > self.ec_max:
            self.status["Peristaltică A"] = False
            self.status["Peristaltică B"] = False
            mesaje.append("⚠️ EC ridicat! Dozare oprită (necesită diluție).")
        else:
            self.status["Peristaltică A"] = False
            self.status["Peristaltică B"] = False
            mesaje.append("✅ EC în interval optim.")

        return mesaje
