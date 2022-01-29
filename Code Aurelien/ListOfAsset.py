import pandas as pd
from Asset import Asset


class ListOfAsset:
    def __init__(self, names, values, dates, returns, covMat):
        self.listAssets = [Asset(names[i], values[names[i]], dates) for i in range(0, len(names))]
        self.returns = returns
        self.covMat = covMat
        self.meanAssetsPrice = 0

    def MeanAssetPrice(self):
        assetPrices = 0
        for i in range(0, len(self.listAssets)):
            assetPrices += self.listAssets[i].values.loc[0]
        mean = assetPrices / len(self.listAssets)
        return mean

    def LastPrices(self):
        lastPrices = [self.listAssets[i].values.loc[0] for i in range(0, len(self.listAssets))]
        """
        lastPrices = list()
        for i in range(0, len(self.listAssets)):
            lastPrices.append(self.listAssets[i].values.loc[0])
        """
        return lastPrices

    def ListOfPrices(self, numberOfDays):
        prices = [[self.listAssets[i].values.loc[j] for i in range(0, len(self.listAssets))]
                  for j in range(0, numberOfDays)]
        return prices

    def __str__(self):
        return str([self.listAssets[i].name for i in range(0, len(self.listAssets))])
