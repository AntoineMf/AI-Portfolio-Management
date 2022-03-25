# ------------- Asset Class ------------- #

class Asset:
    '''Création d'un asset (nom, liste des prix et dates correspondantes)'''
    def __init__(self, name, values, dates):
        self.name = name
        self.values = values
        self.dates = dates
