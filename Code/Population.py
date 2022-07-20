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
        # Returns souhaites par le client
        self.returnsClient = returnsClient
        # Volatilite souhaite par le client
        self.volClient = volClient
        # Index de la generation
        self.indexGeneration = indexGeneration
        # Liste de portefeuilles
        self.listPortfolio = []
        # Nombre d'individus
        self.numIndividuals = numIndividuals
        # Objet listOfAssets
        self.listOfAssets = listOfAssets
        # Montant a investir
        self.amount = amount
        # Population precedente
        self.lastPop = lastPop
        # Nombre max de generation
        self.maxGeneration = maxGeneration
        # S'il s'agit de la premiere generation on l'initiliase avec n nouveaux portefeuilles aleatoires
        if indexGeneration == 0:
            self.createInitPop()
        # Sinon on se base sur la precedente et on la modifie
        else:
            self.createPop()
        # On trie les portefeuilles selon leur score
        self.sortPopulation()

    def createInitPop(self):
        """
        Initialise la premiere population
        """
        for individu in range(self.numIndividuals):
            # Creation de portefeuilles aleatoires
            self.listPortfolio.append(Portfolio(self.listOfAssets, self.amount, self.returnsClient, self.volClient))

    def createPop(self):
        """
        Creation d'une population a partir de la population precedente en fonction de la generation a laquelle on se
        trouve
        """
        # Precedente liste de portefeuille
        lastListPortfolio = self.lastPop.listPortfolio
        # Si on se trouve a moins de 50 pourcents du nombre de generations total
        if self.indexGeneration / self.maxGeneration < 0.5:
            # On conserve les 10 meilleurs portefeuilles de la generation precedente
            for i in range(0, 10):
                self.listPortfolio.append(lastListPortfolio[i])
            # Croisement des meilleurs portefeuilles mutes
            for i in range(1):
                # Croisement meilleur portefeuille mutee avec le deuxieme meilleur portefeuille mute
                self.listPortfolio.extend(
                    self.crossover(self.mutation(lastListPortfolio[0]), self.mutation(lastListPortfolio[1])))
                # Portefeuille 2 et 3
                self.listPortfolio.extend(
                    self.crossover(self.mutation(lastListPortfolio[1]), self.mutation(lastListPortfolio[2])))
                # Portefeuille 1 et 3
                self.listPortfolio.extend(
                    self.crossover(self.mutation(lastListPortfolio[0]), self.mutation(lastListPortfolio[2])))

            # Creation d'index aléatoire pour les mutation à venir
            for i in range(1):
                # Index A et B differents
                indexA = rd.randint(0, 40)
                while True:
                    indexB = rd.randint(0, 10)
                    if indexA != indexB:
                        break
                # Index C et D differents
                indexC = rd.randint(0, 40)
                while True:
                    indexD = rd.randint(0, 10)
                    if indexD != indexC:
                        break

                # Mutation de portefeuilles generes aleatoirement
                self.listPortfolio.append(self.mutation(lastListPortfolio[indexA]))  # mut1
                self.listPortfolio.append(self.mutation(lastListPortfolio[indexB]))  # mut2
                self.listPortfolio.append(self.mutation(lastListPortfolio[indexC]))  # mut3
                self.listPortfolio.append(self.mutation(lastListPortfolio[indexD]))  # mut4

                # Croisement de portefeuilles selectionnes aleatoirement
                self.listPortfolio.extend(
                    self.crossover(lastListPortfolio[indexA], lastListPortfolio[indexB]))  # crossover 1
                self.listPortfolio.extend(
                    self.crossover(lastListPortfolio[indexC], lastListPortfolio[indexD]))  # crossover 2

                # Croisement de portefeuilles mutes selectionnes aleatoirement
                self.listPortfolio.extend(self.crossover(self.mutation(lastListPortfolio[indexA]),
                                                         self.mutation(lastListPortfolio[indexB])))  # mut + cross 1
                self.listPortfolio.extend(self.crossover(self.mutation(lastListPortfolio[indexC]),
                                                         self.mutation(lastListPortfolio[indexD])))  # mut + cross 2
            # Mutation des 4 meilleurs portefeuilles
            for i in range(4):
                self.listPortfolio.append(self.mutation(lastListPortfolio[i]))
            # Generation de 43 portefeuilles aleatoires
            for i in range(0, 43):
                self.listPortfolio.append(Portfolio(self.listOfAssets, self.amount, self.returnsClient, self.volClient))

        # Si on se trouve entre 50 et 80 pourcents du nombre de generations total
        elif self.indexGeneration / self.maxGeneration < 0.8:
            # On conserve les 15 meilleurs portefeuilles de la generation precedente
            for i in range(0, 15):
                self.listPortfolio.append(lastListPortfolio[i])

            # Croisement des meilleurs portefeuilles mutes
            for i in range(1):
                # Croisement meilleur portefeuille mutee avec le deuxieme meilleur portefeuille mute
                self.listPortfolio.extend(
                    self.crossover(self.mutation(lastListPortfolio[0]), self.mutation(lastListPortfolio[1])))
                # Portefeuille 2 et 3
                self.listPortfolio.extend(
                    self.crossover(self.mutation(lastListPortfolio[1]), self.mutation(lastListPortfolio[2])))
                # Portefeuille 1 et 3
                self.listPortfolio.extend(
                    self.crossover(self.mutation(lastListPortfolio[0]), self.mutation(lastListPortfolio[2])))
                # Portefeuille 1 et 4
                self.listPortfolio.extend(
                    self.crossover(self.mutation(lastListPortfolio[0]), self.mutation(lastListPortfolio[3])))
                # Portefeuille 2 et 4
                self.listPortfolio.extend(
                    self.crossover(self.mutation(lastListPortfolio[1]), self.mutation(lastListPortfolio[3])))
                # Portefeuille 3 et 4
                self.listPortfolio.extend(
                    self.crossover(self.mutation(lastListPortfolio[2]), self.mutation(lastListPortfolio[3])))

            # Creation d'index aléatoire pour les mutation à venir
            for i in range(1):
                # Index A et B differents
                indexA = rd.randint(0, 20)
                while True:
                    indexB = rd.randint(0, 10)
                    if indexA != indexB:
                        break
                # Index C et D differents
                indexC = rd.randint(0, 20)
                while True:
                    indexD = rd.randint(0, 10)
                    if indexD != indexC:
                        break

                # Mutation de portefeuilles generes aleatoirement
                self.listPortfolio.append(self.mutation(lastListPortfolio[indexA]))  # mut1
                self.listPortfolio.append(self.mutation(lastListPortfolio[indexB]))  # mut2
                self.listPortfolio.append(self.mutation(lastListPortfolio[indexC]))  # mut3
                self.listPortfolio.append(self.mutation(lastListPortfolio[indexD]))  # mut4

                # Croisement de portefeuilles selectionnes aleatoirement
                self.listPortfolio.extend(
                    self.crossover(lastListPortfolio[indexA], lastListPortfolio[indexB]))  # crossover 1

                self.listPortfolio.extend(
                    self.crossover(lastListPortfolio[indexC], lastListPortfolio[indexD]))  # crossover 2

                # Croisement de portefeuilles mutes selectionnes aleatoirement
                self.listPortfolio.extend(self.crossover(self.mutation(lastListPortfolio[indexA]),
                                                         self.mutation(lastListPortfolio[indexB])))  # mut + cross 1
                self.listPortfolio.extend(self.crossover(self.mutation(lastListPortfolio[indexC]),
                                                         self.mutation(lastListPortfolio[indexD])))  # mut + cross 2
            # Mutation des 11 meilleurs portefeuilles
            for i in range(11):
                self.listPortfolio.append(self.mutation(lastListPortfolio[i]))

            # Generation de 25 portefeuilles aleatoires
            for i in range(0, 25):
                self.listPortfolio.append(Portfolio(self.listOfAssets, self.amount, self.returnsClient, self.volClient))
        # Si on se trouve a plus de 80 pourcents du nombre de generations total
        else:
            #  On conserve les 25 meilleurs portefeuilles de la generation precedente
            for i in range(0, 25):
                self.listPortfolio.append(lastListPortfolio[i])

            # Croisement des meilleurs portefeuilles mutes
            for i in range(1):
                # Croisement meilleur portefeuille mutee avec le deuxieme meilleur portefeuille mute
                self.listPortfolio.extend(
                    self.crossover(self.mutation(lastListPortfolio[0]), self.mutation(lastListPortfolio[1])))
                # Portefeuille 2 et 3
                self.listPortfolio.extend(
                    self.crossover(self.mutation(lastListPortfolio[1]), self.mutation(lastListPortfolio[2])))
                # Portefeuille 1 et 3
                self.listPortfolio.extend(
                    self.crossover(self.mutation(lastListPortfolio[0]), self.mutation(lastListPortfolio[2])))
                # Portefeuille 1 et 4
                self.listPortfolio.extend(
                    self.crossover(self.mutation(lastListPortfolio[0]), self.mutation(lastListPortfolio[3])))
                # Portefeuille 2 et 4
                self.listPortfolio.extend(
                    self.crossover(self.mutation(lastListPortfolio[1]), self.mutation(lastListPortfolio[3])))
                # Portefeuille 3 et 4
                self.listPortfolio.extend(
                    self.crossover(self.mutation(lastListPortfolio[2]), self.mutation(lastListPortfolio[3])))
                # Portefeuille 1 et 5
                self.listPortfolio.extend(
                    self.crossover(self.mutation(lastListPortfolio[0]), self.mutation(lastListPortfolio[4])))
                # Portefeuille 2 et 5
                self.listPortfolio.extend(
                    self.crossover(self.mutation(lastListPortfolio[1]), self.mutation(lastListPortfolio[4])))
                # Portefeuille 3 et 5
                self.listPortfolio.extend(
                    self.crossover(self.mutation(lastListPortfolio[2]), self.mutation(lastListPortfolio[4])))

            # Creation d'index aléatoire pour les mutation à venir
            for i in range(1):
                # Index A et B differents
                indexA = rd.randint(0, 50)
                while True:
                    indexB = rd.randint(0, 10)
                    if indexA != indexB:
                        break
                # Index A et B differents
                indexC = rd.randint(0, 50)
                while True:
                    indexD = rd.randint(0, 10)
                    if indexD != indexC:
                        break

                # Mutation de portefeuilles generes aleatoirement
                self.listPortfolio.append(self.mutation(lastListPortfolio[indexA]))  # mut1
                self.listPortfolio.append(self.mutation(lastListPortfolio[indexB]))  # mut2
                self.listPortfolio.append(self.mutation(lastListPortfolio[indexC]))  # mut3
                self.listPortfolio.append(self.mutation(lastListPortfolio[indexD]))  # mut4

                # Croisement de portefeuilles selectionnes aleatoirement
                self.listPortfolio.extend(
                    self.crossover(lastListPortfolio[indexA], lastListPortfolio[indexB]))  # crossover 1

                self.listPortfolio.extend(
                    self.crossover(lastListPortfolio[indexC], lastListPortfolio[indexD]))  # crossover 2

                # Croisement de portefeuilles mutes selectionnes aleatoirement
                self.listPortfolio.extend(self.crossover(self.mutation(lastListPortfolio[indexA]),
                                                         self.mutation(lastListPortfolio[indexB])))  # mut + cross 1
                self.listPortfolio.extend(self.crossover(self.mutation(lastListPortfolio[indexC]),
                                                         self.mutation(lastListPortfolio[indexD])))  # mut + cross 2
            # Mutation des 15 meilleurs portefeuilles
            for i in range(15):
                self.listPortfolio.append(self.mutation(lastListPortfolio[i]))

            # Generation de 5 portefeuilles aleatoires
            for i in range(0, 5):
                self.listPortfolio.append(Portfolio(self.listOfAssets, self.amount, self.returnsClient, self.volClient))

    def crossover(self, portfolioA, portfolioB):
        """
        Croisement entre deux portefeuilles
        """
        size = len(portfolioA.shares) / 2
        index = list()
        # Nombre de shares de chacun des titres du portefeuille 1
        newShares1 = [i for i in portfolioA.shares]
        # Nombre de shares de chacun des titres du portefeuille 1
        newShares2 = [i for i in portfolioB.shares]
        # Echange aleatoire du nombre de shares d'un portefeuille avec celui d'un autre
        while True:
            if len(index) == size:
                break
            # Index aleatoire de l'actif
            i = rd.randint(0, len(portfolioA.shares)-1)
            # Si cet actif n'a pas encore ete echange on effectue l'echange
            if i not in index:
                index.append(i)
                newShares1[i] = portfolioB.shares[i]
                newShares2[i] = portfolioA.shares[i]
        # Liste des derniers closing price
        lastPrices = self.listOfAssets.lastPrices()
        # Calcul des poids des enfants
        newWeights1 = [newShares1[i] * lastPrices[i]/self.amount for i in range(0, len(newShares1))]
        newWeights2 = [newShares2[i] * lastPrices[i] / self.amount for i in range(0, len(newShares2))]
        # Normalisation des poids
        newWeights1 = [newWeights1[i]/sum(newWeights1) for i in range(0, len(newWeights1))]
        newWeights2 = [newWeights2[i] / sum(newWeights2) for i in range(0, len(newWeights2))]
        # On rnvoie les 2 enfants
        return Portfolio(self.listOfAssets, self.amount, self.returnsClient, self.volClient, newWeights1), \
            Portfolio(self.listOfAssets, self.amount, self.returnsClient, self.volClient, newWeights2)

    def mutation(self, portfolio):
        """
        Mutation d'un portefeuille, on mute 1 a 4 poids d'actifs
        """
        # Selection aleatoire du nombre d'actifs a modifier
        nbMut = rd.randint(1, 4)
        # Liste des index des actifs a modifier
        listIndex = []
        # Liste des anciens poids
        weights = [portfolio.weights[i] for i in range(0, len(portfolio.weights))]
        # Liste des nouveaux poids aleatoires
        weightsRnd = []
        # Liste des derniers closing price
        lastPrices = self.listOfAssets.lastPrices()
        # Selection des actifs dont on va changer le poids
        while True:
            if len(listIndex) == nbMut:
                break
            index = rd.randint(0, len(weights)-1)
            # Si l'index n'est pas deja dans la liste des index dont il faut changer les poids
            if index not in listIndex:
                listIndex.append(index)
                # Nouveau poids aleatoire
                weightsRnd.append(rd.randint(5000, 100000) / 100000)
        # Calcul du nouveau nombre de shares
        sharesRnd = [weightsRnd[i]*self.amount / lastPrices[listIndex[i]] for i in range(0, len(listIndex))]
        # Arrondi du nombre de shares
        sharesRnd = [round(sharesRnd[i]) if round(sharesRnd[i]) < sharesRnd[i] else round(sharesRnd[i]) - 1 for i in
                     range(0, len(listIndex))]
        # Nouveaux poids calcules a partir du nombre de shares et dernier closing prices
        for i in range(0, nbMut):
            weights[listIndex[i]] = sharesRnd[i]*lastPrices[listIndex[i]] / self.amount
        # Normalisation des poids
        weights = [weights[i]/sum(weights) for i in range(0, len(weights))]
        # On renvoie le nouveau portefeuille mute
        return Portfolio(self.listOfAssets, self.amount, self.returnsClient, self.volClient, weights)

    def sortPopulation(self):
        """
        Classement des portefeuilles de la population en fonction de leurs score
        """
        self.listPortfolio = sorted(self.listPortfolio, key=lambda portfolio: portfolio.score, reverse=True)
