# Libs
import random
from Portfolio import *

# Class Population (list of Portfolios)
class Population :
    # --- Constructor and Attributes --- #
    def __init__(self,list_porfolio=[]):
        self._list_porfolio = list_porfolio
        self._nb_indiv = len(list_porfolio)
    
    # --- Useful Methods --- #
    '''
        5 minute pour la vol d'un seul portfolio, on va s'en passer pour le moment
        car le problème c'est qu'on est censé calculer la vol de 100+ portfeuille a chaque generation
        et y'a au moins 1000 gen je pense donc bon
    '''
    def volatility_portfolio(self): # on s'en passe pour le prototype
        vol_1 = 0
        vol_2 = 0 # je separe les 2 membres du calcul de vol pour que ce soit plus clair
        for assets in self.keys():
            vol_1 = vol_1 + self[assets]*assets.get_ecart_type() # en gros somme des poids i * ecart type i
        for assets_i in self.keys():
            for assets_j in self.keys():
                if assets_i != assets_j:
                    vol_2 = vol_2 + self[assets_i]*self[assets_j]*Asset.cov_assets(assets_i,assets_j)
                    #en gros, poid i * poiid j * cov(i,j)
        return vol_1 + vol_2


    # --- Crossover/Mutation Module --- #
    # Mutation
    def fonction_de_mutation(self, pourcentage_de_mutation):
        nb_a_modif = round(len(self._list_porfolio) * pourcentage_de_mutation/100) # % de la population qui sera muté
        list_index_a_modif = [round(random.uniform(0,len(self._list_porfolio)-1)) for i in range(nb_a_modif)] # generation d'indexs aleas
        for index in list_index_a_modif:
            nb_mutation = round(random.uniform(1,3))
            for mut in range(nb_mutation):
                index_assets = round(random.uniform(0,len(self._list_porfolio[index]._list_assets)-1))
                self._list_porfolio[index]._list_assets[index_assets].set_weigth_alea() # Creation d'un individu aleatoire à l'index aleatoire
                self._list_porfolio[index]._list_assets[index_assets].set_return()
            self._list_porfolio[index].normalisation_des_poids() # remise de la somme = 1
            self._list_porfolio[index].Set_vol() # remise de la bonne vol
        # return self._list_porfolio
        
    # Crossover
    def fonction_de_croisement(self):
        '''
        On va faire en sorte que chaque indiv de la pop mere ait une descendance avec un partenaire alea 
        De plus, chaque couple parent pourra avoir aleatoirement 1,2 ou 3 enfants ( ou plus si il est choisi aleatoirement par un autre parent).
        Enfin, chaque enfant recevra une part alea de chaque parent
        '''
        tamp_porfolio_enfant = []
        for portefeuille in self._list_porfolio:# parcours des portfeuille dans la pop
            nb_enfant = round(random.uniform(1,3)) # nb enfant alea
            index_partenaire_alea = round(random.uniform(0,len(self._list_porfolio)-1)) # partenaire alea
            for compteur_denfant in range(1,nb_enfant+1): # parcours du nombre d'enfant par portfeuille
                liste_assets_enfant = []  # liste enfant vide
                for index_assets in range(0,len(portefeuille._list_assets)): # parcours des assets du portefeuille pour créer l'enfant
                    A_ou_B = round(random.uniform(1,2)) # alea sur hérédité de parent A ou B pour chaque assets
                    if A_ou_B == 1:
                        liste_assets_enfant.append(portefeuille._list_assets[index_assets])
                        # on prends le poids de l'assets clé du parent A
                    elif A_ou_B == 2:
                        liste_assets_enfant.append(self._list_porfolio[index_partenaire_alea]._list_assets[index_assets])
                        # on prends le poids de l'assets clé du parent alea B
                    else:
                        print("erreur sur A_ou_B")
                enfant = Portfolio(liste_assets_enfant)
                enfant.normalisation_des_poids()
                enfant.Set_vol() 
                tamp_porfolio_enfant.append(enfant)
        for enfant in tamp_porfolio_enfant: # j'ai fait cette 2 eme boucle for car sinon on ajouter un enfant à chaque fois et donc for portfeuille in self._list_porfolio ne sarreter jamais
            self._list_porfolio.append(enfant)
        
        self._nb_indiv = len(self._list_porfolio)  # reparametrage de nb_indiv
        # return pop_enfant
    


    # --- Fitness Module --- #
    def fitness(self): # attribution d'un score à chaque portefeuille de la pop
        for portefeuille in self._list_porfolio:
            portefeuille.set_score_portfolio()
        
    def tri_selon_score(self):
        self._list_porfolio.sort(key=lambda v: v._score , reverse=True)
        
    def selection(self, nb_conservation, alea_rescape):
        index_alea = [round(random.uniform(0,len(self._list_porfolio)-1)) for i in range(alea_rescape)]
        rescape = []
        for index in index_alea:
            rescape.append(self._list_porfolio[index]) # on garde aléa
        
        del self._list_porfolio[nb_conservation:]# on garde les "conservation" meilleur
        for portfolio in rescape:
            self._list_porfolio.append(portfolio)
        self._nb_indiv = len(self._list_porfolio) # reparametrage de nb_indiv
        
        # return selection
    
