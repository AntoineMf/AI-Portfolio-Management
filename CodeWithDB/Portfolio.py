
# ------------- Portfolio Class ------------- #
# Libraries
import random as rd


class Portfolio:
    """
    Creation d'un portefeuille avec tout les parametres demandes du clients et gestion de la fitness
    """
    def __init__(self, listOfAssets, amount, returnsClient, volClient, weights=0):
        """
        Constructeur du portefeuille, si les poids sont nuls de nouveaux sont generes
        """
        self.returnsClient = returnsClient
        self.volClient = volClient
        # Si les demandes du client comprennent une volatilité et le rendement on calcule le sharpe objectif
        if self.volClient != 0 and self.returnsClient != 0:
            self.sharpeClient = returnsClient/volClient
        self.listOfAssets = listOfAssets
        # On selectionne aleatoirement le nombre d'actifs auxquels on va mettre un poids
        self.numberOfAssets = rd.randint(2,len(self.listOfAssets.listAssets))
        # Score a la crati
        self.score = 0
        self.amount = amount
        self.shares = []
        # Si aucun poids n'est fourni a l'initialisation on en genere aleatoirement sinon on affecte les poids donnes
        # en parametre
        self.weights = weights if weights != 0 else self.RandomWeights()

        # Ces fonctions vont calculer les informations dont a besoin pour le scoring du portfeuille
        self.computeShares()
        self.returns = self.ComputeReturns()
        self.vol = self.ComputeVol()
        self.sharpe = self.ComputeSharpe()
        self.avgReturns = sum(self.returns)/len(self.returns)

        # Scoring du portefeuille
        self.fitness()
    # --- Methods --- #
    # Sort a population based on..

    def ChooseAssets(self):
        """
        Selection d'actifs aleatoirement (a integrer dans le portefeuille)
        """
        choices = list()
        index = range(0, len(self.listOfAssets.listAssets))
        while len(choices) < self.numberOfAssets:
            # Choix aleatoire d'un actif parmi la liste des actifs
            val = rd.choices(index)[0]
            # S'il n'est pas deja dans les actifs selectionnes on le rajoute sinon on rerun
            if val not in choices:
                choices.append(val)
        return choices

    def RandomWeights(self):
        """
        Permet de generer aleatoirement les poids des actifs de notre portefeuille (dans le cas ou il n'y avait pas de
        liste de poids au moment de la creation de l'objet
        """
        choices = self.ChooseAssets()
        # poids alea entre 0 et 1 à 0.001 près
        rndWeights = [rd.randint(1000, 100000) / 100000 for i in range(0, self.numberOfAssets)]
        # Normalisation des poids pour que la somme soit egale a 1
        rndWeights = [i / sum(rndWeights) for i in rndWeights]
        # Creation d'une liste temporaire de poids (vide)
        weightsTemp = [0 for i in range(0, len(self.listOfAssets.listAssets))]
        index = 0
        for i in range(0, len(weightsTemp)):
            if i in choices:
                # Attribution de poids aléatoire aux actifs selectionnes
                weightsTemp[i] = rndWeights[index]
                index += 1
        # Recuperation des closing price des actifs pour calculer le nombre de share de chacun des actifs
        lastPrices = self.listOfAssets.LastPrices()

        # Calcul du nombre de shares pour chaque actif
        shares = [weightsTemp[i]*self.amount/lastPrices[i] for i in range(0, len(lastPrices))]
        # On arrondi le nombre de shares pour avoir quelque chose de realiste
        self.shares = [round(shares[i]) - 1 if round(shares[i]) > shares[i] else round(shares[i])
                       for i in range(0, len(shares))]
        # On retourne les nouveaux poids (calcules a partir du nombre de shares arrondi
        return [self.shares[i]*lastPrices[i]/self.amount for i in range(0, len(self.shares))]

    '''liste du nb de share à acheter selon le montant du portefeuille, le poids attribué, et la valeur d'une actions'''
    def computeShares(self):
        # Recuperation des closing price des actifs pour calculer le nombre de share de chacun des actifs
        lastPrices = self.listOfAssets.LastPrices()
        # Calcul du nombre de shares pour chaque actif
        shares = [self.weights[i] * self.amount / lastPrices[i] for i in range(0, len(lastPrices))]
        # On arrondi le nombre de shares pour avoir quelque chose de realiste
        self.shares = [round(shares[i]) - 1 if round(shares[i]) > shares[i] else round(shares[i])
                       for i in range(0, len(shares))]
        # On calcule les nouveaux poids (calcules a partir du nombre de shares arrondi
        self.weights = [self.shares[i]*lastPrices[i]/self.amount for i in range(0, len(self.shares))]

    ''' Renvoie une liste de returns du portefeuille par jours, sachant que chaque jours le rendement est la somme 
    des rendements de chaque assets pondérer par l'investissement propre à chaque assets'''
    def ComputeReturns(self):
        """
        Renvoie une liste de returns du portefeuille sur une periode donnee
        """
        # Nombre d'assets total que le portfeuille peut contenir
        numberOfAssets = len(self.listOfAssets.listAssets)
        # Periode sur laquelle on calcule les return (exemple returns sur 3 jour S3/S0 - 1)
        rollingWindow = self.listOfAssets.returns.rolling_window
        # Nombre de returns max dans la liste
        maxNumber = self.listOfAssets.returns.max_number

        # Liste des closing prices de chacun des actifs sur toutes les dates a partir de la plus recente et de la
        # plus ancienne qui nous permette de calculer le nombre de returns souhaites sur la plage de temps de donnee
        listOfPrices = self.listOfAssets.ListOfPrices(rollingWindow + maxNumber)
        # Le calcul est le suivant on considere la nav (net asset value) du portefeuille a la date i et a la date
        # i moins le nombre de jours sur lequel se base le calcule des returns, on en fait le ratio et on retire 1
        # La nav est calculee en sommant le produit du nombre de shares de chaque actif et la valeur d'une share pour
        # tous les actifs
        returns = [(sum([self.shares[i]*listOfPrices[n][i] for i in range(0, numberOfAssets)]) /
                   sum([self.shares[i]*listOfPrices[n + rollingWindow][i] for i in range(0, numberOfAssets)])) - 1
                   for n in range(0, maxNumber)]
        return returns

    def ComputeVol(self):
        """
        Calcule et retourne la volatilite du portefeuille
        """
        variance = 0
        # Formule basique utilisee dans le cadre du calcul de la variance d'un portefeuille a partir du poids des actifs
        # et de la matrice de covariance des actifs
        for i in range(0, len(self.listOfAssets.listAssets)):
            for j in range(0, len(self.listOfAssets.listAssets)):
                variance += self.weights[i]*self.weights[j]*self.listOfAssets.covMat.matrix.iloc[i, j]
        # La volatilite est la racine carree de la variance
        return variance**0.5

    def ComputeSharpe(self):
        """
        Calcule et retourne le ratio de sharpe du portefeuille
        """
        sum = 0
        # Somme des rendements
        for i in range(0, len(self.returns)):
            sum += self.returns[i]
        # Le ratio de sharpe est calcule en faisant la moyenne des rendements divise par la volatilite du portefeuille
        sharpe = sum / (len(self.returns) * self.vol)
        return sharpe

    def fitness(self):
        self.score = 0
        sumWeights = sum(self.weights)
        if sumWeights < 1:
            self.score -= 0.9 * abs(1 - sumWeights)
        elif sumWeights < 1.05:
            self.score -= 20 * abs(1 - sumWeights)
        else:
            self.score -= 1000 * abs(1 - sumWeights)

        if self.volClient != 0 and self.returnsClient != 0:
            self.score -= abs(self.vol - self.volClient) / self.volClient
            self.score -= abs(self.avgReturns - self.returnsClient) / self.returnsClient
            self.score -= 0.8 * abs(self.sharpe - self.sharpeClient) / self.sharpeClient

        elif self.volClient != 0:
            self.score -= 5 * abs(self.vol - self.volClient) / self.volClient
            self.score += self.sharpe

        elif self.returnsClient != 0:
            self.score -= 5 * abs(self.avgReturns - self.returnsClient) / self.returnsClient
            self.score += self.sharpe
