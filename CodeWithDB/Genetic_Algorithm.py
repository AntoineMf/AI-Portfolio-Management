# ------------- Genetic Algorithm Class ------------- #
# Libraries
import Asset
import Portfolio
from Population import Population
from Asset import Asset
import re


class Genetic_Algorithm:

    # _________________________________initialisation__________________________

    def __init__(self, listOfAssets, amount, nbOfGeneration, returnsClient, volClient):
        self.returnsClient = returnsClient
        self.volClient = volClient

        self.listOfAssets = listOfAssets
        self.amount = amount
        self.nbOfGeneration = nbOfGeneration
        self.Historique_gen = list()

        self.listOfPopulation = list()
        self.listOfPopulation.append(Population(listOfAssets, amount, 0, 75, nbOfGeneration,
                                                self.returnsClient, self.volClient))
        self.x = []
        self.y = []

        for i in range(1, nbOfGeneration):
            print(f"\nGeneration : {i}\n")
            self.listOfPopulation.append(Population(self.listOfAssets, self.amount, i, 75, nbOfGeneration,
                                                    self.returnsClient, self.volClient, self.listOfPopulation[i-1]))
            """print(f"list of pop iteration {i} : {self.listOfPopulation[i]}")"""
            meanScore = [self.listOfPopulation[i].listPortfolio[j].score
                         for j in range(0, len(self.listOfPopulation[i].listPortfolio))]
            meanScore = sum(meanScore) / len(meanScore)

            for j in self.listOfPopulation[i].listPortfolio:
                self.x.append(j.vol)
                self.y.append(j.avgReturns)

            print(f"1st returns : {self.listOfPopulation[i].listPortfolio[0].avgReturns}")
            print(f"1st vol : {self.listOfPopulation[i].listPortfolio[0].vol}")
            print(f"2nd returns : {self.listOfPopulation[i].listPortfolio[1].avgReturns}")
            print(f"3rd returns : {self.listOfPopulation[i].listPortfolio[2].avgReturns}")
            print(f"Mean Score: {meanScore}")

        print(f"\nReturns :{self.listOfPopulation[nbOfGeneration-1].listPortfolio[0].avgReturns}")
        print(f"Volatility : {self.listOfPopulation[nbOfGeneration-1].listPortfolio[0].vol}\n")
        assetsSeparated = re.findall("[a-zA-Z]+\s[a-zA-Z]+\s[a-zA-Z]+",
                                     str(self.listOfPopulation[0].listPortfolio[0].listOfAssets))

        returnsList = [[self.listOfPopulation[i].listPortfolio[j].avgReturns for j in
                        range(0, len(self.listOfPopulation[i].listPortfolio))] for i in
                       range(0, len(self.listOfPopulation))]
        volsList = [[self.listOfPopulation[i].listPortfolio[j].vol for j in
                    range(0, len(self.listOfPopulation[i].listPortfolio))] for i in
                    range(0, len(self.listOfPopulation))]

        for j in range(len(assetsSeparated)):
            print(f"{assetsSeparated[j]} : {self.listOfPopulation[0].listPortfolio[0].weights[j]}")

        self.Result = [f"\nReturns :{self.listOfPopulation[nbOfGeneration-1].listPortfolio[0].avgReturns}",
                       f"Volatility : {self.listOfPopulation[nbOfGeneration-1].listPortfolio[0].vol}\n"]
