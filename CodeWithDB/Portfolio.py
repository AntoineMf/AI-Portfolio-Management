
# ------------- Portfolio Class ------------- #
# Libraries
import random as rd
import numpy as np
from Functions import Functions as fct

class Portfolio:
    # --- Constructor and Attributes --- #
    def __init__(self, listOfAssets, amount, returnsClient, volClient, weights=0, score=0):
        self.returnsClient = returnsClient
        self.volClient = volClient
        if self.volClient != 0 and self.returnsClient != 0: self.sharpeClient = returnsClient/volClient
        self.listOfAssets = listOfAssets
        #print(self.listOfAssets)
        self.numberOfAssets = 6
        self.score = score
        self.amount = amount
        self.shares = []
        self.weights = weights if weights != 0 else self.RandomWeights()
        self.computeShares()
        #print(self.weights)
        """
        if weights != 0:
            self.weights = weights
        else:
            self.weights = 0
            self.RandomWeights()
        """
        self.returns = self.ComputeReturns()
        self.vol = self.ComputeVol()
        self.sharpe = self.ComputeSharpe()
        self.avgReturns = sum(self.returns)/len(self.returns)

        self.fitness()
        #print(self.shares)
        #print(self.shares)
        #print(self.weights)
        #print(self.vol)
        #print(self.ComputeSharpe())
        #print(self.returns)
        #print(self.listOfAssets.returns.matrixReturns.shape[0])

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

    def ChooseAssets(self):
        choices = list()
        index = range(0, len(self.listOfAssets.listAssets))
        while len(choices) < self.numberOfAssets:
            val = rd.choices(index)[0]
            if val not in choices:
                choices.append(val)
        return choices

    """
    def MaxShares(self, lastPrices, choices):
        prices = [lastPrices[i] if choices[i] else float('inf') for i in range(0, len(lastPrices))]
        maxShares = int(self.amount / (min(prices) * 2))
        return maxShares
    """
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
    

    def RandomWeightsfirst(self, confidence=0.01, numberOfAssets=38):
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

    def RandomWeightsTest(self, confidence=0.01, numberOfAssets=38):
        #lastPrices = self.listOfAssets.LastPrices()
        choices = self.ChooseAssets(numberOfAssets)
        maxPercentage = 0.125 if len(choices) > 5 else 0.5
        minPercentage = 0.001
        while True:
            weights = list()
            weightsCum = 0
            for i in range(0, numberOfAssets):
                if (1 - weightsCum) < minPercentage:
                    break
                weights.append((rd.randint(int(minPercentage*1000), int(min(1-weightsCum, maxPercentage)*1000)))/1000)
                #print(rd.randint(int(minPercentage*10000), int(min(float(1-weightsCum), maxPercentage)*10000))/10000)
                #print(int(minPercentage*10000))
                weightsCum += weights[i]
            print(weightsCum)
            print(len(weights))
            if 1 - confidence < weightsCum <= 1 and len(weights) == numberOfAssets:
                break
        self.weights = weights
        print(weights)
    
    def RandomWeightsTer(self, confidence=0.01, numberOfAssets=20):
        #lastPrices = self.listOfAssets.LastPrices()
        choices = self.ChooseAssets(numberOfAssets)
        maxPercentage = 0.4 if len(choices) > 5 else 0.5
        minPercentage = 0.001
        while True:

            #weights = [rd.randint(minPercentage*10000, maxPercentage*10000)/10000 for i in range(0, numberOfAssets)]
            weights = [rd.randint(1, 100000) / 100000 for i in range(0, numberOfAssets)]
            #print(sum(weights))
            weights = [i / sum(weights) for i in weights]
            if 1 - confidence < sum(weights) <= 1:
                break

        self.weights = weights
        print(sum(weights))
        print(max(weights))
        print(min(weights))
        #print(weights)
    """

    """
    def RandomWeightsBis(self, numberOfAssets=38):
        choices = self.ChooseAssets(numberOfAssets)
        #maxPercentage = 0.4 if len(choices) > 5 else 0.5
        #minPercentage = 0.001
        weights = [rd.randint(1000, 100000) / 100000 for i in range(0, numberOfAssets)]
        weights = [i / sum(weights) for i in weights]
        self.weights = [0 for i in range(0,len(self.listOfAssets.listAssets))]
        index = 0
        for i in range(0, len(self.weights)):
            if i in choices:
                self.weights[i] = weights[index]
                index += 1
    """

    def RandomWeights(self):
        choices = self.ChooseAssets()
        rndWeights = [rd.randint(1000, 100000) / 100000 for i in range(0, self.numberOfAssets)]
        rndWeights = [i / sum(rndWeights) for i in rndWeights]
        weightsTemp = [0 for i in range(0, len(self.listOfAssets.listAssets))]
        index = 0
        for i in range(0, len(weightsTemp)):
            if i in choices:
                weightsTemp[i] = rndWeights[index]
                index += 1
        lastPrices = self.listOfAssets.LastPrices()
        shares = [weightsTemp[i]*self.amount/lastPrices[i] for i in range(0, len(lastPrices))]
        self.shares = [round(shares[i]) - 1 if round(shares[i]) > shares[i] else round(shares[i]) for i in range(0, len(shares))]
        #self.shares = [round(shares[i]) for i in range(0, len(shares))]
        return [self.shares[i]*lastPrices[i]/self.amount for i in range(0, len(self.shares))]
        #print(f"weight sum {str(sum(self.weights))}")

    def computeShares(self):
        lastPrices = self.listOfAssets.LastPrices()
        self.shares = [self.weights[i] * self.amount / lastPrices[i] for i in range(0, len(lastPrices))]
        #self.shares = [round(shares[i]) - 1 if round(shares[i]) > shares[i] else round(shares[i]) for i in
                       #range(0, len(shares))]

    """
    def ComputeNoShares(self):
        lastPrices = self.listOfAssets.LastPrices()
        self.shares = [self.weights[i]*self.amount/lastPrices[i] for i in range(0, len(lastPrices))]
        test = [(round(self.shares[i])-1)*lastPrices[i] if round(self.shares[i]) > self.shares[i] else round(self.shares[i])*lastPrices[i] for i in range(0, len(self.shares))]
        print(str(sum(test)/self.amount))
    """

    def ComputeReturns(self):
        noOfDays = self.listOfAssets.returns.matrixReturns.shape[0]
        returnsAssets = self.listOfAssets.returns.matrixReturns
        listOfPrices = self.listOfAssets.ListOfPrices(noOfDays)
        #print(listOfPrices)
        returns = [sum([(self.shares[i]) * (listOfPrices[n][i]) * (returnsAssets.iloc[n, i]) / self.amount
                       for i in range(0, len(self.listOfAssets.listAssets))]) for n in range(0, noOfDays - 1)]
        
        # test
        
        #nav = [sum([(self.shares[i]) * (listOfPrices[n][i]) for i in range(0, len(self.listOfAssets.listAssets))])
               #for n in range(0, noOfDays)]
        #returns = [(nav[i] / nav[i + 1]) - 1 for i in range(0, noOfDays - 1)]
        #returns = [sum([(self.shares[i]) * (listOfPrices[n][i]) * (returnsAssets.iloc[n, i]) / self.amount
                        #for i in range(0, len(self.listOfAssets.listAssets))]) for n in range(0, noOfDays - 1)]
        #print(returns)
        return returns

    def ComputeVol(self):
        variance = 0
        for i in range(0, len(self.listOfAssets.listAssets)):
            for j in range(0, len(self.listOfAssets.listAssets)):
                variance += self.weights[i]*self.weights[j]*self.listOfAssets.covMat.matrix.iloc[i, j]
        return variance**0.5

    def ComputeSharpe(self):
        sum = 0
        for i in range(0, len(self.returns)):
            sum += self.returns[i]
        sharpe = sum / (len(self.returns) * self.vol)
        return sharpe
        #print(f"sharp : {sharpe}")
    """
    def fitness(self):
        #score = self.sharpe
        score = self.avgReturns
        print(score)
        uninvested = 1 - sum(self.weights)
        if uninvested < 0:
            score -= 10 * abs(uninvested)
        elif uninvested > 0.15:
            score -= 2 * uninvested
        else:
            score -= 0.5 * uninvested
        if self.volClient != 0 and self.returnsClient != 0:
            score -= 1000 * abs(self.vol - self.volClient)
            score -= 1000 * abs(self.avgReturns - self.returnsClient)
            
        elif self.volClient != 0:
            score -= 1.5 *abs(self.vol - self.volClient)
            
        elif self.returnsClient != 0:
            pass
            #score -= 1000 * abs(self.avgReturns - self.returnsClient)
            
        self.score = score
    """
    def fitness(self):
        # score = self.sharpe
        self.score = 0
        sumWeights = sum(self.weights)
        #score = self.avgReturns
        #print(score)
        uninvested = 1 - sumWeights
        if sumWeights < 1:
            self.score -= 0.9 * fct.eucldideanDist(1, sumWeights)
        elif sumWeights < 1.05:
            self.score -= 20 * fct.eucldideanDist(1, sumWeights)
        else:
            self.score -= 1000 * fct.eucldideanDist(1, sumWeights)

        if self.volClient != 0 and self.returnsClient != 0:
            self.score -= fct.eucldideanDist(self.vol, self.volClient) / self.volClient
            self.score -= fct.eucldideanDist(self.avgReturns, self.returnsClient) / self.returnsClient
            self.score -= fct.eucldideanDist(self.sharpe, self.sharpeClient) / self.sharpeClient
            #self.score -= 0.8 * np.linalg.norm(self.vol - self.volClient) / self.volClient
            #print(f"Pénalité vol {np.linalg.norm(self.vol - self.volClient) / self.volClient})")
            #self.score -= 1.2 * np.linalg.norm(self.avgReturns - self.returnsClient) / self.returnsClient
            #print(f"Pénalité returns {np.linalg.norm(self.avgReturns - self.returnsClient) / self.returnsClient})")
            #self.score -= np.linalg.norm(self.sharpe - (self.returnsClient / self.volClient)) / (self.returnsClient/ self.volClient)

        elif self.volClient != 0:
            self.score -= 100 * fct.eucldideanDist(self.vol, self.volClient) / self.volClient
            self.score += self.sharpe

        elif self.returnsClient != 0:
            self.score -= 5 * fct.eucldideanDist(self.avgReturns, self.returnsClient) / self.returnsClient
            #self.score += self.sharpe
            self.score -= 10000 * fct.eucldideanDist(self.avgReturns, self.returnsClient) / self.returnsClient
            # score -= 1000 * abs(self.avgReturns - self.returnsClient)
        #print(f"score: {self.score}")
        #self.score = score