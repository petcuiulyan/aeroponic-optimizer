class AutomatizareSera:
    def __init__(self):
        # Parametri Țintă (Ideali)
        self.target_ph = 6.0
        self.target_ec = 1.8
        self.target_co2 = 800 # ppm
        
        # Stări Echipamente
        self.electrovalve = [False, False, False] # Pentru magistrale
        self.pompe_peristaltice = {"pH_Down": False, "A": False, "B": False}
        self.pompa_120w = False

    def logica_dozare(self, ph_actual, ec_actual):
        """Decide care pompă peristaltică trebuie să pornească"""
        actiuni = []
        if ph_actual > self.target_ph + 0.2:
            actiuni.append("PORNEȘTE: Peristaltică pH-Down")
            self.pompe_peristaltice["pH_Down"] = True
        else:
            self.pompe_peristaltice["pH_Down"] = False

        if ec_actual < self.target_ec - 0.1:
            actiuni.append("PORNEȘTE: Pompe Peristaltice A+B (Nutrienți)")
            self.pompe_peristaltice["A"] = True
            self.pompe_peristaltice["B"] = True
        else:
            self.pompe_peristaltice["A"] = False
            self.pompe_peristaltice["B"] = False
        
        return actiuni if actiuni else ["Echilibru Nutritiv OK"]

    def logica_umplere_magistrale(self, ora_curenta):
        """
        Programare umplere periodică (ex: la fiecare 4 ore)
        Deoarece ai flotoare la turnuri, pompa trebuie să meargă până 
        când presiunea crește sau un timp fix (flood time).
        """
        program = [8, 12, 16, 20] # Orele de alimentare
        if ora_curenta in program:
            self.pompa_120w = True
            return "ALIMENTARE ACTIVĂ: Umplere bazine turnuri"
        self.pompa_120w = False
        return "SISTEM ÎN AȘTEPTARE (Flotoare închise)"

    def monitorizare_mediu(self, temp, hum, co2):
        """Logica pentru ventilație și CO2"""
        if co2 < self.target_co2:
            return "Sugestie: Pornește generator CO2 / Verifică ventilația"
        if temp > 28:
            return "ALARMĂ: Temperatură ridicată! Activare extractoare."
        return "Mediu Ambient: Optim"
