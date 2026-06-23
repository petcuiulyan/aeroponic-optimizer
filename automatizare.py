class AutomatizareSera:
    def __init__(self):
        self.status = {
            "Pompa nutrienți": False,
            "pH Up": False,
            "pH Down": False,
            "Pompa principală": False
        }

    def pornire(self):
        for k in self.status:
            self.status[k] = True

    def oprire(self):
        for k in self.status:
            self.status[k] = False
``
