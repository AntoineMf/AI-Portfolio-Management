# ------------- Population Class ------------- #
# Libraries
import random as rd

from Portfolio import Portfolio


class Population:
    # --- Constructor and Attributes --- #

    def __init__(self, listOfAssets, amount, indexGeneration, numIndividuals, maxGeneration, returnsClient,
                 volClient, lastPop=0):
        """
            Constructeur d'une population. Selon l'indexGénération (0 = pop_0 initiale) on construit soit une pop de
            numIndividuals induvidus, soit des population issues des croisement et mutation de la LastPop existante.
            La population est immédiatement triée dès sa crétion.
            """
        self.returnsClient = returnsClient
        self.volClient = volClient
        self.indexGeneration = indexGeneration
        self.listPortfolio = []
        self.numIndividuals = numIndividuals
        self.listOfAssets = listOfAssets
        self.amount = amount
        self.lastPop = lastPop
        self.maxGeneration = maxGeneration

        if indexGeneration == 0:
            self.createInitPop()
        else:
            self.createPop()
        self.sortPopulation()

    def createInitPop(self):
        for individu in range(self.numIndividuals):
            self.listPortfolio.append(Portfolio(self.listOfAssets, self.amount, self.returnsClient, self.volClient))

    def createPop(self): 
        lastListPortfolio = self.lastPop.listPortfolio
        if self.indexGeneration / self.maxGeneration < 0.5:
            for i in range(0, 10):
                self.listPortfolio.append(lastListPortfolio[i])

            # for i in range(0, 5):
            #    self.listPortfolio.append(lastListPortfolio[int((len(lastListPortfolio)/2)-i-1)])

            # print(f"last pop : {len(lastListPortfolio[0].weights)}")

            # self.listPortfolio.extend(self.crossover(lastListPortfolio[0], lastListPortfolio[1])) # crois1
            # self.listPortfolio.extend(self.crossover(lastListPortfolio[1], lastListPortfolio[2]))
            # self.listPortfolio.extend(self.crossover(lastListPortfolio[0], lastListPortfolio[2]))
            for i in range(1):
                self.listPortfolio.extend(
                    self.crossover(self.mutation(lastListPortfolio[0]), self.mutation(lastListPortfolio[1])))
                # mut + crois 1
                self.listPortfolio.extend(
                    self.crossover(self.mutation(lastListPortfolio[1]), self.mutation(lastListPortfolio[2])))
                self.listPortfolio.extend(
                    self.crossover(self.mutation(lastListPortfolio[0]), self.mutation(lastListPortfolio[2])))

            ''' Creation d'index aléatoire pour les mutation à venir'''
            for i in range(1):
                indexA = rd.randint(0, 40)
                while True:
                    indexB = rd.randint(0, 10)
                    if indexA != indexB:
                        break

                indexC = rd.randint(0, 40)
                while True:
                    indexD = rd.randint(0, 10)
                    if indexD != indexC:
                        break
                        # print(self.mutation())
                self.listPortfolio.append(self.mutation(lastListPortfolio[indexA]))  # mut1
                self.listPortfolio.append(self.mutation(lastListPortfolio[indexB]))  # mut2
                self.listPortfolio.append(self.mutation(lastListPortfolio[indexC]))  # mut3
                self.listPortfolio.append(self.mutation(lastListPortfolio[indexD]))  # mut4

                self.listPortfolio.extend(
                    self.crossover(lastListPortfolio[indexA], lastListPortfolio[indexB]))  # crossover 1

                self.listPortfolio.extend(
                    self.crossover(lastListPortfolio[indexC], lastListPortfolio[indexD]))  # crossover 2

                self.listPortfolio.extend(self.crossover(self.mutation(lastListPortfolio[indexA]),
                                                         self.mutation(lastListPortfolio[indexB])))  # mut + cross 1
                self.listPortfolio.extend(self.crossover(self.mutation(lastListPortfolio[indexC]),
                                                         self.mutation(lastListPortfolio[indexD])))  # mut + cross 2
            for i in range(4):
                self.listPortfolio.append(self.mutation(lastListPortfolio[i]))

            for i in range(0, 43):
                self.listPortfolio.append(Portfolio(self.listOfAssets, self.amount, self.returnsClient, self.volClient))

        elif self.indexGeneration / self.maxGeneration < 0.8:
            for i in range(0, 15):
                self.listPortfolio.append(lastListPortfolio[i])

            for i in range(1):
                self.listPortfolio.extend(
                    self.crossover(self.mutation(lastListPortfolio[0]), self.mutation(lastListPortfolio[1])))
                # mut + crois 1
                self.listPortfolio.extend(
                    self.crossover(self.mutation(lastListPortfolio[1]), self.mutation(lastListPortfolio[2])))
                self.listPortfolio.extend(
                    self.crossover(self.mutation(lastListPortfolio[0]), self.mutation(lastListPortfolio[2])))
                self.listPortfolio.extend(
                    self.crossover(self.mutation(lastListPortfolio[0]), self.mutation(lastListPortfolio[3])))
                self.listPortfolio.extend(
                    self.crossover(self.mutation(lastListPortfolio[1]), self.mutation(lastListPortfolio[3])))
                self.listPortfolio.extend(
                    self.crossover(self.mutation(lastListPortfolio[2]), self.mutation(lastListPortfolio[3])))
            for i in range(1):
                indexA = rd.randint(0, 20)
                while True:
                    indexB = rd.randint(0, 10)
                    if indexA != indexB:
                        break

                indexC = rd.randint(0, 20)
                while True:
                    indexD = rd.randint(0, 10)
                    if indexD != indexC:
                        break
                        # print(self.mutation())
                self.listPortfolio.append(self.mutation(lastListPortfolio[indexA]))  # mut1
                self.listPortfolio.append(self.mutation(lastListPortfolio[indexB]))  # mut2
                self.listPortfolio.append(self.mutation(lastListPortfolio[indexC]))  # mut3
                self.listPortfolio.append(self.mutation(lastListPortfolio[indexD]))  # mut4

                self.listPortfolio.extend(
                    self.crossover(lastListPortfolio[indexA], lastListPortfolio[indexB]))  # crossover 1

                self.listPortfolio.extend(
                    self.crossover(lastListPortfolio[indexC], lastListPortfolio[indexD]))  # crossover 2

                self.listPortfolio.extend(self.crossover(self.mutation(lastListPortfolio[indexA]),
                                                         self.mutation(lastListPortfolio[indexB])))  # mut + cross 1
                self.listPortfolio.extend(self.crossover(self.mutation(lastListPortfolio[indexC]),
                                                         self.mutation(lastListPortfolio[indexD])))  # mut + cross 2
            for i in range(11):
                self.listPortfolio.append(self.mutation(lastListPortfolio[i]))

            for i in range(0, 25):
                self.listPortfolio.append(Portfolio(self.listOfAssets, self.amount, self.returnsClient, self.volClient))
        else:
            for i in range(0, 25):
                self.listPortfolio.append(lastListPortfolio[i])

            for i in range(1):
                self.listPortfolio.extend(
                    self.crossover(self.mutation(lastListPortfolio[0]), self.mutation(lastListPortfolio[1])))
                # mut + crois 1
                self.listPortfolio.extend(
                    self.crossover(self.mutation(lastListPortfolio[1]), self.mutation(lastListPortfolio[2])))
                self.listPortfolio.extend(
                    self.crossover(self.mutation(lastListPortfolio[0]), self.mutation(lastListPortfolio[2])))
                self.listPortfolio.extend(
                    self.crossover(self.mutation(lastListPortfolio[0]), self.mutation(lastListPortfolio[3])))
                self.listPortfolio.extend(
                    self.crossover(self.mutation(lastListPortfolio[1]), self.mutation(lastListPortfolio[3])))
                self.listPortfolio.extend(
                    self.crossover(self.mutation(lastListPortfolio[2]), self.mutation(lastListPortfolio[3])))
                self.listPortfolio.extend(
                    self.crossover(self.mutation(lastListPortfolio[0]), self.mutation(lastListPortfolio[4])))
                self.listPortfolio.extend(
                    self.crossover(self.mutation(lastListPortfolio[1]), self.mutation(lastListPortfolio[4])))
                self.listPortfolio.extend(
                    self.crossover(self.mutation(lastListPortfolio[2]), self.mutation(lastListPortfolio[4])))
            for i in range(1):
                indexA = rd.randint(0, 50)
                while True:
                    indexB = rd.randint(0, 10)
                    if indexA != indexB:
                        break

                indexC = rd.randint(0, 50)
                while True:
                    indexD = rd.randint(0, 10)
                    if indexD != indexC:
                        break
                        # print(self.mutation())
                self.listPortfolio.append(self.mutation(lastListPortfolio[indexA]))  # mut1
                self.listPortfolio.append(self.mutation(lastListPortfolio[indexB]))  # mut2
                self.listPortfolio.append(self.mutation(lastListPortfolio[indexC]))  # mut3
                self.listPortfolio.append(self.mutation(lastListPortfolio[indexD]))  # mut4

                self.listPortfolio.extend(
                    self.crossover(lastListPortfolio[indexA], lastListPortfolio[indexB]))  # crossover 1

                self.listPortfolio.extend(
                    self.crossover(lastListPortfolio[indexC], lastListPortfolio[indexD]))  # crossover 2

                self.listPortfolio.extend(self.crossover(self.mutation(lastListPortfolio[indexA]),
                                                         self.mutation(lastListPortfolio[indexB])))  # mut + cross 1
                self.listPortfolio.extend(self.crossover(self.mutation(lastListPortfolio[indexC]),
                                                         self.mutation(lastListPortfolio[indexD])))  # mut + cross 2
            for i in range(15):
                self.listPortfolio.append(self.mutation(lastListPortfolio[i]))

            for i in range(0, 5):
                self.listPortfolio.append(Portfolio(self.listOfAssets, self.amount, self.returnsClient, self.volClient))

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
        newWeights1 = [newWeights1[i]/sum(newWeights1) for i in range(0, len(newWeights1))]
        newWeights2 = [newWeights2[i] / sum(newWeights2) for i in range(0, len(newWeights2))]
        return Portfolio(self.listOfAssets, self.amount, self.returnsClient, self.volClient, newWeights1), \
            Portfolio(self.listOfAssets, self.amount, self.returnsClient, self.volClient, newWeights2)

    def mutation(self, portfolio):
        nbMut = rd.randint(1, 4)
        listIndex = []
        weights = [portfolio.weights[i] for i in range(0, len(portfolio.weights))]
        listWeight = portfolio.shares
        weightsRnd = []
        lastPrices = self.listOfAssets.LastPrices()
        while True:
            if len(listIndex) == nbMut:
                break
            index = rd.randint(0, len(listWeight)-1)
            if index not in listIndex:
                listIndex.append(index)
                weightsRnd.append(rd.randint(5000, 100000) / 100000)
        sharesRnd = [weightsRnd[i]*self.amount / lastPrices[listIndex[i]] for i in range(0, len(listIndex))]
        sharesRnd = [round(sharesRnd[i]) if round(sharesRnd[i]) < sharesRnd[i] else round(sharesRnd[i]) - 1 for i in
                     range(0, len(listIndex))]
        for i in range(0, nbMut):
            weights[listIndex[i]] = sharesRnd[i]*lastPrices[listIndex[i]] / self.amount
        weights = [weights[i]/sum(weights) for i in range(0, len(weights))]
        return Portfolio(self.listOfAssets, self.amount, self.returnsClient, self.volClient, weights)

    def createPortfolio(self, weights):
        return Portfolio(self.listOfAssets, self.amount, self.returnsClient, self.volClient, weights)

    def maxScore(self):
        scores = [self.listPortfolio[i].score for i in range(0, len(self.listPortfolio))]
        maxScore = max(scores)
        return maxScore

    def meanScore(self):
        scores = [self.listPortfolio[i].score for i in range(0, len(self.listPortfolio))]
        meanScore = sum(scores)/len(scores)
        return meanScore

    def sortPopulation(self):
        self.listPortfolio = sorted(self.listPortfolio, key=lambda portfolio: portfolio.score, reverse=True)
