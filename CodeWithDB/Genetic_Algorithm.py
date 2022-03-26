# ------------- Genetic Algorithm Class ------------- #
# Libraries

from Population import Population
import re


class GeneticAlgorithm:

    # _________________________________initialisation__________________________

    def __init__(self, listOfAssets, amount, nbOfGeneration, returnsClient, volClient):
        self.returnsClient = returnsClient
        self.volClient = volClient

        self.listOfAssets = listOfAssets
        self.amount = amount
        self.nbOfGeneration = nbOfGeneration
        self.Historique_gen = list()

        # Crée une liste des différentes populations générées en fonction des générations.
        self.listOfPopulation = list()

        self.listOfPopulation.append(Population(listOfAssets, amount, 0, 75, nbOfGeneration,
                                                self.returnsClient, self.volClient))
        self.x = []
        self.y = []
        indexOfGeneration = 0
        for i in range(1, nbOfGeneration):
            indexOfGeneration = i
            print(f"\nGeneration : {i}\n")
            self.listOfPopulation.append(Population(self.listOfAssets, self.amount, i, 75, nbOfGeneration,
                                                    self.returnsClient, self.volClient, self.listOfPopulation[i-1]))
            # Calcul le score moyen du portefeuille
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

            if self.listOfPopulation[i].listPortfolio[0].score >= -0.02:
                break

        print(f"\nReturns :{self.listOfPopulation[indexOfGeneration].listPortfolio[0].avgReturns}")
        print(f"Volatility : {self.listOfPopulation[indexOfGeneration].listPortfolio[0].vol}\n")
        # Crée une liste qui contient les noms des différents assets utilisés
        assetsSeparated = re.findall(r"[a-zA-Z]+\s[a-zA-Z]+\s[a-zA-Z]+",
                                     str(self.listOfPopulation[0].listPortfolio[0].listOfAssets))

        # Affiche le poids attribué (pour chaque asset) pour le meilleur portefeuille de la génération
        for j in range(len(assetsSeparated)):
            print(f"{assetsSeparated[j]} : {self.listOfPopulation[0].listPortfolio[0].weights[j]}")

        # Création d'une variable contenant la volatilité et le rendement du meilleur portefeuille de la génération
        # sous format string
        self.Result = [f"\nReturns :{self.listOfPopulation[indexOfGeneration].listPortfolio[0].avgReturns}",
                       f"Volatility : {self.listOfPopulation[indexOfGeneration].listPortfolio[0].vol}\n"]
        # Création d'une variable contenant la volatilité et le rendement du meilleur portefeuille de la génération
        # pour rajouter le point du meilleur portefeuille en evidence sur le graphique
        self.ResultFloat = [self.listOfPopulation[indexOfGeneration].listPortfolio[0].avgReturns,
                            self.listOfPopulation[indexOfGeneration].listPortfolio[0].vol]
