# ------------- Returns Class ------------- #
# Packages

# Libraries
import pandas as pd


class Returns:
    '''
    Set up des returns via les données de la BDD et des parametre rentré en MAIN
    Double boucle For pour la matrice des returns et set up des Names pour les noms des columns.
    '''
    def __init__(self, values, rolling_window, names, max_number=0):
        self.rolling_window = rolling_window
        self.max_number = max_number
        if max_number == 0:
            max_number = len(values) - rolling_window
        self.matrixReturns = pd.DataFrame(data=None, index=range(0, max_number), columns=range(0, len(values.iloc[0])))
        self.matrixReturns = pd.DataFrame(data=None, index=range(0, max_number), columns=names)
        for j in range(0, len(values.iloc[0])):
            for i in range(0, max_number):
                # Formules des returns
                self.matrixReturns.iloc[i, j] = ((values.iloc[i, j] / values.iloc[i + rolling_window, j]) - 1)

    '''Permet de retourner la liste des returns d'un seul assets de la matrice des returns de tout les assets'''
    def getReturnsAsset(self, asset):
        list_of_returns = []
        # TODO  index = asset.index (A reflechir: attribut index d un asset pour les matrices de returns et varCov)
        for i in range(0, len(self.matrixReturns)):
            list_of_returns[i] = self.matrixReturns[i][asset]
        return list_of_returns
    
    '''Surcharge du print() pour afficher la matrice de returns'''
    def __str__(self):
        return str(self.matrixReturns)
