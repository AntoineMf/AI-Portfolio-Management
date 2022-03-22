# ------------- Genetic Algorithm Class ------------- #
# Libraries
import Asset
import Portfolio
from Population import Population
from Asset import Asset
import re
#from InterFace import cleaning,Print_Info_Gen,Print_Final_Result



class Genetic_Algorithm:

    # _________________________________initialisation__________________________

    def __init__(self, listOfAssets, amount, nbOfGeneration, returnsClient, volClient):
        self.returnsClient = returnsClient
        self.volClient = volClient

        self.listOfAssets=listOfAssets
        self.amount=amount
        self.nbOfGeneration = nbOfGeneration
        self.Historique_gen = list()

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
            print(f"1st returns : {self.listOfPopulation[i].listPortfolio[0].avgReturns}")
            print(f"1st vol : {self.listOfPopulation[i].listPortfolio[0].vol}")
            print(f"2nd returns : {self.listOfPopulation[i].listPortfolio[1].avgReturns}")
            print(f"3rd returns : {self.listOfPopulation[i].listPortfolio[2].avgReturns}")
            print(f"Mean Score: {meanScore}")

            #print(f"Mean score : {self.listOfPopulation[i].meanScore()}")
            #print(f"Sum Weights :{sum(self.listOfPopulation[i].listPortfolio[0].weights)}")
        print(f"\nReturns :{self.listOfPopulation[nbOfGeneration-1].listPortfolio[0].avgReturns}")
        print(f"Volatility : {self.listOfPopulation[nbOfGeneration-1].listPortfolio[0].vol}\n")
    #cleaning()
        #Print_Final_Result(f"\nReturns :{sum(self.listOfPopulation[nbOfGeneration-1].listPortfolio[0].returns)/6}",f"Volatility : {self.listOfPopulation[nbOfGeneration-1].listPortfolio[0].vol}\n")

        assetsSeparated=re.findall("[a-zA-Z]+\s[a-zA-Z]+\s[a-zA-Z]+",str(self.listOfPopulation[0].listPortfolio[0].listOfAssets)) # ???
        #print(assetsSeparated)
        
        
        for j in range(len(assetsSeparated)):
            print(f"{assetsSeparated[j]} : {self.listOfPopulation[0].listPortfolio[0].weights[j]}")
        
        self.Result = [f"\nReturns :{sum(self.listOfPopulation[nbOfGeneration-1].listPortfolio[0].returns)/6}",f"Volatility : {self.listOfPopulation[nbOfGeneration-1].listPortfolio[0].vol}\n"]

''' self.listOfPopulation.append(Population(listOfAssets,amount,0,75,self.returnsClient,self.volClient)) # création Pop_0
        #print(f"pop : {self.listOfPopulation[0]}")

        for i in range (1,nbOfGeneration):
            #cleaning() #efface le contenue de la fenetre de la gen precedente.

            
            #print(f"\nGeneration : {i}\n")
            Num_gen = f"\nGeneration : {i}\n"
            
            #C'est dans cette ligne que les croisement mutation et fitness intervienne en tache de fond ( via Population puis Via Portfolio )
            self.listOfPopulation.append(Population(self.listOfAssets,self.amount,i,75,self.returnsClient,self.volClient,self.listOfPopulation[i-1]))
            """print(f"list of pop iteration {i} : {self.listOfPopulation[i]}")"""
            #Print_Info_Gen(f"\nGeneration : {i}\n",f"1st : {sum(self.listOfPopulation[i].listPortfolio[0].returns)/6}",f"2nd : {sum(self.listOfPopulation[i].listPortfolio[1].returns)/6}",f"3rd : {sum(self.listOfPopulation[i].listPortfolio[2].returns)/6}")
            #print(f"Max score : {self.listOfPopulation[i].maxScore()}")
            #print(f" self.listOfPopulation[i].listPortfolio[0].score)
            
            #print(f"1st : {sum(self.listOfPopulation[i].listPortfolio[0].returns)/6}")
            #print(f"2nd : {sum(self.listOfPopulation[i].listPortfolio[1].returns)/6}")
            #print(f"3rd : {sum(self.listOfPopulation[i].listPortfolio[2].returns)/6}")

            first = f"1st : {sum(self.listOfPopulation[i].listPortfolio[0].returns)/6}"
            sec = f"2nd : {sum(self.listOfPopulation[i].listPortfolio[1].returns)/6}"
            thrd = f"3rd : {sum(self.listOfPopulation[i].listPortfolio[2].returns)/6}"

            self.Historique_gen.append([Num_gen,first,sec,thrd])

            #print(f"Mean score : {self.listOfPopulation[i].meanScore()}")
            #print(f"Sum Weights :{sum(self.listOfPopulation[i].listPortfolio[0].weights)}")
        
        self.Result = [f"\nReturns :{sum(self.listOfPopulation[nbOfGeneration-1].listPortfolio[0].returns)/6}",f"Volatility : {self.listOfPopulation[nbOfGeneration-1].listPortfolio[0].vol}\n"]
        #print(f"\nReturns :{sum(self.listOfPopulation[nbOfGeneration-1].listPortfolio[0].returns)/6}")
        #print(f"Volatility : {self.listOfPopulation[nbOfGeneration-1].listPortfolio[0].vol}\n")
>>>>>>> UeserI'''



    
    

       






        

    
   