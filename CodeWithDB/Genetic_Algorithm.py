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

        self.listOfAssets=listOfAssets
        self.amount=amount
        self.nbOfGeneration = nbOfGeneration

        self.listOfPopulation = list()
        self.listOfPopulation.append(Population(listOfAssets,amount,0,75,nbOfGeneration,self.returnsClient,self.volClient))
        #print(f"pop : {self.listOfPopulation[0]}")

        for i in range (1,nbOfGeneration):
            print(f"\nGeneration : {i}\n")
            self.listOfPopulation.append(Population(self.listOfAssets,self.amount,i,75, nbOfGeneration,self.returnsClient,self.volClient,self.listOfPopulation[i-1]))
            """print(f"list of pop iteration {i} : {self.listOfPopulation[i]}")"""
            meanScore = [self.listOfPopulation[i].listPortfolio[j].score for j in range(0, len(self.listOfPopulation[i].listPortfolio))]
            meanScore = sum(meanScore) / len(meanScore)
            #print(f"Max score : {self.listOfPopulation[i].maxScore()}")
            #print(f" self.listOfPopulation[i].listPortfolio[0].score)
            print(f"1st : {self.listOfPopulation[i].listPortfolio[0].avgReturns}")
            print(f"1st : {self.listOfPopulation[i].listPortfolio[0].vol}")
            print(f"2nd : {self.listOfPopulation[i].listPortfolio[1].avgReturns}")
            print(f"3rd : {self.listOfPopulation[i].listPortfolio[2].avgReturns}")
            print(f"Mean Score: {meanScore}")

            #print(f"Mean score : {self.listOfPopulation[i].meanScore()}")
            #print(f"Sum Weights :{sum(self.listOfPopulation[i].listPortfolio[0].weights)}")
        print(f"\nReturns :{self.listOfPopulation[nbOfGeneration-1].listPortfolio[0].avgReturns}")
        print(f"Volatility : {self.listOfPopulation[nbOfGeneration-1].listPortfolio[0].vol}\n")

        assetsSeparated=re.findall("[a-zA-Z]+\s[a-zA-Z]+\s[a-zA-Z]+",str(self.listOfPopulation[0].listPortfolio[0].listOfAssets))
        #print(assetsSeparated)
        

        for j in range(len(assetsSeparated)):
            print(f"{assetsSeparated[j]} : {self.listOfPopulation[0].listPortfolio[0].weights[j]}")






        

    
   