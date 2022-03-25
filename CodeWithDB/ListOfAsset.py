import pandas as pd
from Asset import Asset


class ListOfAsset:

    '''
    Cration d'une liste comprenant tout les assets, chaque assets possède indépendamment son nom, ses values (prices) à
    chaque date. Les returns et la VARCOV matrix, eux sont communs à tout les assets. Donc necessitée de les passer en
    attributs ??
    MeanAssetsPrice est un faux attribu car il n'est jamais valorisé
     '''
    def __init__(self, names, values, dates, returns, covMat):
        self.listAssets = [Asset(names[i], values[names[i]], dates) for i in range(0, len(names))]
        self.returns = returns
        self.covMat = covMat
        self.meanAssetsPrice = 0

    '''Retourne le prix moyen de l'assests sur la durée.'''
    def MeanAssetPrice(self):
        assetPrices = 0
        for i in range(0, len(self.listAssets)):
            assetPrices += self.listAssets[i].values.loc[0]
        mean = assetPrices / len(self.listAssets)
        return mean

    '''???'''
    def LastPrices(self):
        lastPrices = [self.listAssets[i].values.loc[0] for i in range(0, len(self.listAssets))]
        """
        lastPrices = list()
        for i in range(0, len(self.listAssets)):
            lastPrices.append(self.listAssets[i].values.loc[0])
        """
        return lastPrices
    
    ''' ???
    Retourne le prix de tout les assetds dans l'intervalle de temps donnée NbOfDays
    '''
    def ListOfPrices(self, numberOfDays):
        prices = [[self.listAssets[i].values.loc[j] for i in range(0, len(self.listAssets))]
                  for j in range(0, numberOfDays)]
        return prices

    '''Surcharge du print pour afficher les noms des asstets de la liste.'''
    def __str__(self):
        return str([self.listAssets[i].name for i in range(0, len(self.listAssets))])
