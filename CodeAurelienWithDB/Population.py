# ------------- Population Class ------------- #
# Libraries
from asyncio.windows_events import NULL
import random as rd

from Portfolio import Portfolio


class Population:
    # --- Constructor and Attributes --- #

    def __init__(self, listOfAssets, amount, index_generation, num_individu, lastPop=0):

        self.index_generation=index_generation
        self.listPortfolio=[]
        self.num_individu=num_individu
        self.listOfAssets = listOfAssets
        self.amount=amount
        self.lastPop=lastPop

        if(index_generation==0):
            self.createInitPop()
        #elif(num_generation)
        else:
            self.createPop()

    def createInitPop(self):
        for i in range (self.num_individu):
            self.listPortfolio.append(Portfolio(self.listOfAssets,self.amount))

    def createPop(self): 
        lastListPortfolio = self.lastPop.listPortfolio
        for i in range(0, 10):
            self.listPortfolio.append(lastListPortfolio[i])
        for i in range(0, 10):
            indexA = rd.randint(0,10)
            while True:
                indexB = rd.randint(0, 10)
                if indexA != indexB:
                    break

            self.listPortfolio.append(lastListPortfolio[i]) # mut1
            self.listPortfolio.append(lastListPortfolio[i]) # mut2
            self.listPortfolio.append(lastListPortfolio[i]) # crois1
            self.listPortfolio.append(lastListPortfolio[i]) # mut + crois 1
            self.listPortfolio.append(lastListPortfolio[i]) # mut + crois 2
        for i in range(0, 30):
            self.listPortfolio.append(Portfolio(self.listOfAssets, self.amount))
    

    def crossover(self, portfolioA, portfolioB):
        size = len(portfolioA.listWeights) / 2
        newWeights1 = portfolioA.listWeights[:size] + portfolioB.listWeight[size:]
        newWeights2 = portfolioB.listWeights[:size] + portfolioA.listWeight[size:]
        return [newWeights1, newWeights2]

    def mutation(self, portfolio):
        nbMut = rd.randint(1, 5)
        listIndex = []
        listWeight = portfolio.listWeight
        while True:
            if len(listIndex) == nbMut:
                break
            index = rd.randint(0, len(portfolio.listWeight))
            if index not in listIndex:
                listIndex.append(index)
                listWeight[index] = rd.randint(5000, 100000) / 500000





    def createPortfolio(self, weights):
        return Portfolio(self.listOfAssets, self.amount, weights)
