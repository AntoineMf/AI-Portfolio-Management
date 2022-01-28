import pandas as pd
from Asset import Asset


class ListOfAsset:
    def __init__(self, names, values, dates, returns, covMat):
        self.listAssets = list()
        for i in range(0, len(names) - 1):
            self.listAssets.append(Asset(names[i], values[names[i]], dates))
        self.returns = returns
        self.covMat = covMat
        self.meanAssetsPrice = 0

    def MeanAssetPrice(self):
        assetPrices = 0
        for i in range(0, len(self.listAssets)):
            assetPrices += self.listAssets[i].values.loc[0]
        mean = assetPrices / len(self.listAssets)
        return mean
