# ------------- Portfolio Class ------------- #
# Libraries
import random as rd


class Portfolio:
    # --- Constructor and Attributes --- #
    def __init__(self, listOfAssets, amount, weights=0, score=0):
        self.listOfAssets = listOfAssets
        self.score = score
        self.amount = amount
        self.shares = 0
        if weights != 0:
            self.weights = weights

        else:
            self.RandomWeights()

        self.returns = 0
        self.vol = 0

    # --- Methods --- #
    # Sort a population based on..

    def ChooseAssets(self, numberOfAssets=38):
        temp = list()
        for i in range(0, numberOfAssets):
            val = rd.choices(range(0, len(self.listOfAssets.listAssets)))
            if val in temp:
                i -= 1
                continue
            temp.append(val)
        choices = [True if i in temp else False for i in range(0, len(self.listOfAssets.listAssets))]
        return choices

    def MaxShares(self, lastPrices, choices):
        prices = [lastPrices[i] if choices[i] else float('inf') for i in range(0, len(lastPrices))]
        maxShares = int(self.amount / (min(prices) * 2))
        return maxShares

    def RandomWeights(self, confidence=0.01, numberOfAssets=38):
        lastPrices = self.listOfAssets.LastPrices()
        choices = self.ChooseAssets(numberOfAssets)
        maxShares = self.MaxShares(lastPrices, choices)
        while True:
            shares = [rd.randint(1, maxShares) if choices[i] else 0 for i in range(0, len(choices))]
            weights = [(shares[i]*lastPrices[i])/self.amount for i in range(0, len(choices))]
            sumWeights = sum(weights)
            if (1 - confidence) < sumWeights <= 1:
                break
        self.weights = weights
        self.shares = shares

    def ComputeNoShares(self):
        lastPrices = self.listOfAssets.LastPrices()
        self.shares = [self.weights[i]*self.amount/lastPrices[i] for i in range(0, len(lastPrices))]

    def computeReturns(self):
        noOfDays = self.listOfAssets.returns[0].count()
        returnsAssets = self.listOfAssets.returns
        listOfPrices = self.listOfAssets.ListOfPrices(noOfDays)
        returns = [sum([(self.shares[i]) * (listOfPrices[n][i]) * (returnsAssets.iloc[n,i]) / self.amount
                       for i in range(0, len(self.listOfAssets.listAssets))]) for n in range(0, noOfDays - 1)]
        self.returns = returns

    def set_score(self, score):
        self.score = score

    def get_vol(self):
        print("j'ai pas compris la formule de Vol")
        return 1

    def normalisation_des_poids(self):
        '''
        adaptation de tout les poids pour que ça somme à 1
        '''
        total = 0
        for assets in self._list_assets:
            total = total + assets._weigth
        for assets in self._list_assets:
            assets._weigth = assets._weigth / total

    def set_score_portfolio(self):  # ratio de sharpe
        '''
        calcul du score : Moy(wi*ri/vol) normalement mais pour le proto on va juste faire moy(wi*ri)
        '''
        tamp = 0
        for assets in self._list_assets:
            tamp = tamp + assets._rendement_moy * assets._weigth / self._volatility
        self._score = tamp / len(self._list_assets)

    def Set_vol(self):
        vol_membre_1 = 0
        vol_membre_2 = 0
        for assets in self._list_assets:
            vol_membre_1 = vol_membre_1 + assets._weigth * assets._ecart_type
        for index_i in range(len(self._list_assets)):
            for index_j in range(index_i, len(self._list_assets)):
                vol_membre_2 = vol_membre_2 + self._list_assets[index_i]._weigth * self._list_assets[
                    index_j]._weigth * cov_assets(self._list_assets[index_i], self._list_assets[index_j])
        self._volatility = vol_membre_1 + vol_membre_2
