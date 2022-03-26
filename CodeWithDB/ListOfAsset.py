from Asset import Asset


class ListOfAsset:
    """
    Création d'un objet contenant toutes les donnees concernant les actifs : -liste des actifs avec leurs noms,
    prix et a des dates donnes
    -La matrice de returns des actifs
    -La matrice de covariance des actifs
    """

    def __init__(self, names, values, dates, returns, covMat):
        """
        Initialisation de l'objet
        """
        # Creation de la liste contenant tous les actifs avec leurs prix à des dates donnees et leurs noms
        self.listAssets = [Asset(names[i], values[names[i]], dates) for i in range(0, len(names))]
        # Matrice de returns
        self.returns = returns
        # Matrice de covariance
        self.covMat = covMat

    def LastPrices(self):
        """
        Retourne la liste des derniers closing price de chacun des actifs
        """
        lastPrices = [self.listAssets[i].values.loc[0] for i in range(0, len(self.listAssets))]
        return lastPrices

    def ListOfPrices(self, numberOfDays):
        """
        Retourne la liste des closing price de chacun des actifs entre la derniere date et une date soubaitee
        """
        prices = [[self.listAssets[i].values.loc[j] for i in range(0, len(self.listAssets))]
                  for j in range(0, numberOfDays)]
        return prices

    def __str__(self):
        """
        Permet d'afficher le nom des actifs quand on print l'objet listOfAsset
        """
        return str([self.listAssets[i].name for i in range(0, len(self.listAssets))])
