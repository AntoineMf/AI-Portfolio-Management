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
            self.RandomWeights(0.2)

        self.returns = 0
        self.vol = 0

    # --- Methods --- #
    # Sort a population based on..
    """
    def ChooseAssets(self, numberOfAssets=38):
        temp = list()
        index = range(0, len(self.listOfAssets.listAssets))
        while len(temp) < numberOfAssets:
            val = rd.choices(index)[0]
            if val not in temp:
                temp.append(val)
        choices = [True if i in temp else False for i in range(0, len(self.listOfAssets.listAssets))]
        return choices
    """

    def ChooseAssets(self, numberOfAssets=38):
        choices = list()
        index = range(0, len(self.listOfAssets.listAssets))
        while len(choices) < numberOfAssets:
            val = rd.choices(index)[0]
            if val not in choices:
                choices.append(val)
        return choices

    def MaxShares(self, lastPrices, choices):
        prices = [lastPrices[i] if choices[i] else float('inf') for i in range(0, len(lastPrices))]
        maxShares = int(self.amount / (min(prices) * 2))
        return maxShares

    """
    def RandomWeights(self, confidence=0.01, numberOfAssets=38):
        lastPrices = self.listOfAssets.LastPrices()
        choices = self.ChooseAssets(numberOfAssets)
        maxShares = self.MaxShares(lastPrices, choices)
        print(maxShares)
        #print(choices)
        print("First")
        while True:
            amountToBeFilled = self.amount
            shares = [rd.randint(1, maxShares) if choices[i] else 0 for i in range(0, len(choices))]
            print(shares)
            weights = [(shares[i]*lastPrices[i])/self.amount for i in range(0, len(choices))]
            sumWeights = sum(weights)
            print(sumWeights)
            if (1 - confidence) < sumWeights <= 1:
                print("ok!")
                break
        self.weights = weights
        self.shares = shares
    """

    def RandomWeights(self, confidence=0.01, numberOfAssets=38):
        lastPrices = self.listOfAssets.LastPrices()
        choices = self.ChooseAssets(numberOfAssets)
        maxPercentage = 0.2 if len(choices) > 5 else 0.5
        #print(choices)
        print("First")
        while True:
            shares = [0 for i in range(0, len(self.listOfAssets.listAssets))]
            amountToBeFilled = self.amount
            for i in range(0, len(choices)):
                maxShares = int(amountToBeFilled / lastPrices[choices[i]]) if amountToBeFilled \
                    < maxPercentage * self.amount else int(self.amount * maxPercentage / lastPrices[choices[i]])
                if maxShares == 0:
                    continue
                shares[choices[i]] = rd.randint(1, maxShares)
                amountToBeFilled -= shares[choices[i]] * lastPrices[choices[i]]

            print(shares)
            sum = 0
            for i in range(0, len(shares)):
                sum += shares[i]*lastPrices[i]

            if (1-confidence) < sum/self.amount <= 1:
                break

            #weights = [(shares[i]*lastPrices[i])/self.amount for i in range(0, len(choices))]
            #sumWeights = sum(weights)
            #print(sumWeights)
            #if (1 - confidence) < sumWeights <= 1:
            #    print("ok!")
            #    break
        #self.weights = weights
        #self.shares = shares
        self.weights = [shares[i]*lastPrices[i]/self.amount for i in range(0, len(shares))]
        print(shares)
        print(str(sum/self.amount))

    def ComputeNoShares(self):
        lastPrices = self.listOfAssets.LastPrices()
        self.shares = [self.weights[i]*self.amount/lastPrices[i] for i in range(0, len(lastPrices))]

    def ComputeReturns(self):
        noOfDays = self.listOfAssets.returns[0].count()
        returnsAssets = self.listOfAssets.returns
        listOfPrices = self.listOfAssets.ListOfPrices(noOfDays)
        returns = [sum([(self.shares[i]) * (listOfPrices[n][i]) * (returnsAssets.iloc[n,i]) / self.amount
                       for i in range(0, len(self.listOfAssets.listAssets))]) for n in range(0, noOfDays - 1)]
        self.returns = returns

    def ComputeVol(self):
        variance = 0
        for i in range(0, len(self.listOfAssets.listAssets)):
            for j in range(0, len(self.listOfAssets)):
                variance += self.weights[i]*self.weights[j]*self.listOfAssets.covMat.matrix.iloc[i, j]
        self.vol = variance**0.5