import pandas as pd
from Asset import Asset


class ListOfAsset:

    '''
    Création d'un objet contenant toutes les donnees concernant les actifs : -liste des actifs avec leurs noms,
    prix et a des dates donnes
    -La matrice de returns des actifs
    '''
    def __init__(self, names, values, dates, returns, covMat):
        # Creation de la liste contenant tous les actifs avec leurs prix à des dates donnees et leurs noms
        self.listAssets = [Asset(names[i], values[names[i]], dates) for i in range(0, len(names))]
        self.returns = returns
        self.covMat = covMat

    '''Retourne le prix moyen de l'assests sur la durée.'''
    def MeanAssetPrice(self):
        assetPrices = 0
        for i in range(0, len(self.listAssets)):
            assetPrices += self.listAssets[i].values.loc[0]
        mean = assetPrices / len(self.listAssets)
        return mean

    '''???'''
    def LastPrices(self):
        """
        Retourne la liste des derniers closing price de chacun des actifs
        """
        lastPrices = [self.listAssets[i].values.loc[0] for i in range(0, len(self.listAssets))]
        return lastPrices
    
    ''' ???
    Retourne le prix de tout les assetds dans l'intervalle de temps donnée NbOfDays
    '''
    def ListOfPrices(self, numberOfDays):
        """

        """
        prices = [[self.listAssets[i].values.loc[j] for i in range(0, len(self.listAssets))]
                  for j in range(0, numberOfDays)]
        return prices

    '''Surcharge du print pour afficher les noms des asstets de la liste.'''
    def __str__(self):
        return str([self.listAssets[i].name for i in range(0, len(self.listAssets))])
