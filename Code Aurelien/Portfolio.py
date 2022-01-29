# ------------- Portfolio Class ------------- #
# Libraries
import random as rd


class Portfolio:
    # --- Constructor and Attributes --- #
    def __init__(self, listOfAssets, amount, weights=0, score=0):
        self.listOfAssets = listOfAssets
        self.score = score
        self.amount = amount
        if weights == 0:
            self.weights = [0 for i in range(0, len(self.listOfAssets.listAssets))]
        else:
            self.weights = 0

    # --- Methods --- #
    # Sort a population based on..

    def RandomWeights(self, confidence=0.01, numberOfAssets=38):
        lastPrices = self.listOfAssets.LastPrices()
        choices = self.WeightAssets(numberOfAssets)
        maxShares = self.MaxShares(lastPrices, choices)
        """
        meanPrices = self.listOfAssets.MeanAssetPrice()
        sumPrices = meanPrices*len(self.listOfAssets.listAssets)
        ratioToInvest = self.amount / sumPrices * 1000
        """
        while True:
            shares = [rd.randint(1, maxShares) if choices[i] else 0 for i in range(0, len(choices))]
            weights = [(shares[i]*lastPrices[i])/self.amount for i in range(0, len(choices))]
            sumWeights = sum(weights)
            if (1 - confidence) < sumWeights <= 1:
                break
            """
            sumOfWeights = 0
            weightsSimu = rd.sample(range(0, ratioToInvest), numberOfAssets)
            if not (0 in weightsSimu):
                for i in weightsSimu:
                    sumOfWeights += i
                if (1 - confidence) * ratioToInvest <= sumOfWeights <= ratioToInvest:
                    break
            """
        self.weights = weights

    def WeightAssets(self, numberOfAssets=38):
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
