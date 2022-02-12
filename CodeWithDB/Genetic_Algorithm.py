# ------------- Genetic Algorithm Class ------------- #
# Libraries
import Asset
import Portfolio
from Population import Population
from Asset import Asset


class Genetic_Algorithm:

    # _________________________________initialisation__________________________

    def __init__(self, listOfAssets, amount, nbOfGeneration, returnsClient, volClient):
        self.returnsClient = returnsClient
        self.volClient = volClient

        self.listOfAssets=listOfAssets
        self.amount=amount
        self.nbOfGeneration = nbOfGeneration

        self.listOfPopulation = list()
        self.listOfPopulation.append(Population(listOfAssets,amount,0,75,self.returnsClient,self.volClient))
        print(f"pop : {self.listOfPopulation[0]}")

        for i in range (1,nbOfGeneration):
            print(f"i : {i}")
            self.listOfPopulation.append(Population(self.listOfAssets,self.amount,i,75,self.returnsClient,self.volClient,self.listOfPopulation[i-1]))
            print(f"list of pop iteration {i} : {self.listOfPopulation[i]}")
            print(f"Mean score : {self.listOfPopulation[i].meanScore()}")
            print(f"Max score : {self.listOfPopulation[i].maxScore()}")
            print(self.listOfPopulation[i].listPortfolio[0].score)
            print(self.listOfPopulation[i].listPortfolio[1].score)
            print(self.listOfPopulation[i].listPortfolio[2].score)
            print(f"Sum Weights :{sum(self.listOfPopulation[i].listPortfolio[0].weights)}")
            print(f"Max Returns :{sum(self.listOfPopulation[i].listPortfolio[0].returns)/6}")
            print(self.listOfPopulation[i].listPortfolio[0].vol)






        

    
   