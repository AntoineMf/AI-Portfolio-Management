# ------------- Population Class ------------- #
# Libraries
import random as rd

from Portfolio import Portfolio


class Population:
    # --- Constructor and Attributes --- #

    def __init__(self, listOfAssets, amount, indexGeneration, numIndividuals, lastPop=0):

        self.indexGeneration = indexGeneration
        self.listPortfolio = []
        self.numIndividuals = numIndividuals
        self.listOfAssets = listOfAssets
        self.amount = amount
        self.lastPop = lastPop

        if indexGeneration == 0:
            self.createInitPop()
        # elif(num_generation)
        else:
            self.createPop()

    def createInitPop(self):
        for individu in range(self.numIndividuals):
            self.listPortfolio.append(Portfolio(self.listOfAssets,self.amount))

    def createPop(self): 
        lastListPortfolio = self.lastPop.listPortfolio
        print(f"last pop : {len(lastListPortfolio[0].weights)}")
        for i in range(3):
            self.listPortfolio.append(self.mutation(lastListPortfolio[i])) 

        self.listPortfolio.extend(self.crossover(lastListPortfolio[0],lastListPortfolio[1])) # crois1
        self.listPortfolio.extend(self.crossover(lastListPortfolio[1],lastListPortfolio[2]))
        self.listPortfolio.extend(self.crossover(lastListPortfolio[0],lastListPortfolio[2]))
        self.listPortfolio.extend(self.crossover(self.mutation(lastListPortfolio[0]),self.mutation(lastListPortfolio[1])))
         # mut + crois 1
        self.listPortfolio.extend(self.crossover(self.mutation(lastListPortfolio[1]),self.mutation(lastListPortfolio[2])))
        self.listPortfolio.extend(self.crossover(self.mutation(lastListPortfolio[0]),self.mutation(lastListPortfolio[2])))

        
        for i in range(0, 10):
            self.listPortfolio.append(lastListPortfolio[i])
        for i in range(0, 7):
            indexA = rd.randint(0,10)
            while True:
                indexB = rd.randint(0, 10)
                if indexA != indexB:
                    break

            indexC = rd.randint(0,10)
            while True:
                indexD = rd.randint(0, 10)
                if indexD != indexC:
                    break
            
            #print(self.mutation())
            self.listPortfolio.append(self.mutation(lastListPortfolio[indexA])) # mut1
            self.listPortfolio.append(self.mutation(lastListPortfolio[indexB])) # mut2
            self.listPortfolio.append(self.mutation(lastListPortfolio[indexC])) # mut3
            self.listPortfolio.append(self.mutation(lastListPortfolio[indexD])) # mut4
            
            self.listPortfolio.extend(self.crossover(lastListPortfolio[indexA],lastListPortfolio[indexB])) #crossover 1
            
            self.listPortfolio.extend(self.crossover(lastListPortfolio[indexC],lastListPortfolio[indexD])) #crossover 2
            
            self.listPortfolio.extend(self.crossover(self.mutation(lastListPortfolio[indexA]),self.mutation(lastListPortfolio[indexB]))) # mut + cross 1
            self.listPortfolio.extend(self.crossover(self.mutation(lastListPortfolio[indexC]),self.mutation(lastListPortfolio[indexD]))) # mut + cross 2
            
        for i in range(0, 35):
            self.listPortfolio.append(Portfolio(self.listOfAssets, self.amount))
    

    def crossover(self, portfolioA, portfolioB):
        size = len(portfolioA.shares) / 2
        index = list()
        newShares1 = [i for i in portfolioA.shares]
        newShares2 = [i for i in portfolioB.shares]
        while True:
            if len(index) == size:
                break
            i = rd.randint(0, len(portfolioA.shares)-1)
            if i not in index:
                index.append(i)
                newShares1[i] = portfolioB.shares[i]
                newShares2[i] = portfolioA.shares[i]
        lastPrices = self.listOfAssets.LastPrices()
        newWeights1 = [newShares1[i] * lastPrices[i]/self.amount for i in range(0, len(newShares1))]
        newWeights2 = [newShares2[i] * lastPrices[i] / self.amount for i in range(0, len(newShares2))]
        print(f"weight 1 : {newWeights1}")
        print(f"len : {len(newWeights1)}")
        #return [newWeights1, newWeights2]
        return Portfolio(self.listOfAssets,self.amount,newWeights1),Portfolio(self.listOfAssets,self.amount,newWeights2)

    def mutation(self, portfolio):
        nbMut = rd.randint(1, 5)
        listIndex = []
        weights = [portfolio.weights[i] for i in range(0, len(portfolio.weights))]
        listWeight = portfolio.shares
        weightsRnd = []
        lastPrices = self.listOfAssets.LastPrices()
        while True:
            if len(listIndex) == nbMut:
                break
            index = rd.randint(0, len(listWeight))
            if index not in listIndex:
                listIndex.append(index)
                weightsRnd.append(rd.randint(5000, 100000) / 100000)
        sharesRnd = [weightsRnd[i]*self.amount / lastPrices[listIndex[i]] for i in range(0, len(listIndex))]
        sharesRnd = [round(sharesRnd[i]) if round(sharesRnd[i]) < sharesRnd[i] else round(sharesRnd[i]) - 1 for i in
                     range(0, len(listIndex))]
        for i in range(0, nbMut):
            weights[listIndex[i]] = sharesRnd[i]
        return Portfolio(self.listOfAssets, self.amount, weights)



    def createPortfolio(self, weights):
        return Portfolio(self.listOfAssets, self.amount, weights)

    

