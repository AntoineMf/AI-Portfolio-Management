# ------------- Genetic Algorithm Class ------------- #
# Libraries
import Asset
import Portfolio
from Population import Population
from Asset import Asset


class Genetic_Algorithm:

    # _________________________________initialisation__________________________

    def __init__(self, listOfAssets, amount, nbOfGeneration):

        self.listOfAssets=listOfAssets
        self.amount=amount
        self.nbOfGeneration = nbOfGeneration

        self.listOfPopulation = list()
        self.listOfPopulation.append(Population(listOfAssets,amount,0,100))


        for i in range (1,nbOfGeneration):
            self.listOfPopulation.append(Population(self.listOfAssets,self.amount,i,100,self.listOfPopulation[i-1]))
            print(f"list of pop iteration {i} : {self.listOfPopulation[i]}")






        

    
   