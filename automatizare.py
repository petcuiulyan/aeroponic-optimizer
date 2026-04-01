# automatizare.py

class AutomatizareSera:
    def __init__(self):
        self.status = {
            "Peristaltică A": False, "Peristaltică B": False,
            "Peristaltică pH UP": False, "Peristaltică pH DOWN": False,
            "Pompă 120W": False
        }

    def proceseaza_automat(self, ph, ec, ph_lim, ec_lim, activ):
        mesaje = []
        for k in self.status: self.status[k] = False
        
        if not activ:
            return ["Sistem Automat OPRIT"], self.status

        if ph < ph_lim[0]:
            self.status["Peristaltică pH UP"] = True
            mesaje.append("⬆️ Dozare pH UP ACTIVĂ")
        elif ph > ph_lim[1]:
            self.status["Peristaltică pH DOWN"] = True
            mesaje.append("⬇️ Dozare pH DOWN ACTIVĂ")

        if ec < ec_lim[0]:
            self.status["Peristaltică A"] = True
            self.status["Peristaltică B"] = True
            mesaje.append("🧪 Dozare Nutrienți A+B ACTIVĂ")
            
        return mesaje, self.status

    def actualizeaza_stari(self, timpi, activ):
        """Sincronizează statusul cu timpii de dozare preciză"""
        for k in self.status: self.status[k] = False
        if not activ: return self.status
        
        for nume_pompa, secunde in timpi.items():
            if nume_pompa in self.status and secunde > 0:
                self.status[nume_pompa] = True
        return self.status
