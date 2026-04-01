class AutomatizareSera:
    def __init__(self):
        self.status = {
            "Peristaltică A": False,
            "Peristaltică B": False,
            "Peristaltică pH UP": False,
            "Peristaltică pH DOWN": False,
            "Pompă 120W": False
        }

    def actualizeaza_stari(self, timpi, activ):
        """Sincronizează releele cu timpii de dozare"""
        for k in self.status:
            self.status[k] = False
            
        if not activ:
            return self.status
            
        for nume, secunde in timpi.items():
            if nume in self.status and secunde > 0:
                self.status[nume] = True
        
        # Pompa de umplere 120W este activă când sistemul este pornit
        self.status["Pompă 120W"] = True
        return self.status

    def proceseaza_automat(self, ph, ec, ph_lim, ec_lim, activ):
        """Păstrat pentru compatibilitate cu afișarea mesajelor"""
        mesaje = []
        if not activ: return ["Sistem Oprit"], self.status
        if ph < ph_lim[0] or ph > ph_lim[1]: mesaje.append("⚠️ pH în afara limitelor")
        if ec < ec_lim[0]: mesaje.append("⚠️ EC scăzut - Necesită nutrienți")
        return mesaje, self.status
