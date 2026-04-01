class AutomatizareSera:
    def __init__(self):
        self.status = {
            "Peristaltică A": False, "Peristaltică B": False,
            "Peristaltică pH UP": False, "Peristaltică pH DOWN": False,
            "Pompă 120W": False
        }

    def proceseaza_automat(self, ph, ec, ph_lim, ec_lim, activ):
        mesaje = []
        # Reset state
        for k in self.status: self.status[k] = False
        
        if not activ:
            return ["Sistem Automat OPRIT"], self.status

        # Logică pH
        if ph < ph_lim[0]:
            self.status["Peristaltică pH UP"] = True
            mesaje.append("⬆️ Dozare pH UP ACTIVĂ")
        elif ph > ph_lim[1]:
            self.status["Peristaltică pH DOWN"] = True
            mesaje.append("⬇️ Dozare pH DOWN ACTIVĂ")

        # Logică EC
        if ec < ec_lim[0]:
            self.status["Peristaltică A"] = True
            self.status["Peristaltică B"] = True
            mesaje.append("🧪 Dozare Nutrienți A+B ACTIVĂ")
            
        return mesaje, self.status
