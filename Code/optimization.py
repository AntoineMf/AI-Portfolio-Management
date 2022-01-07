import pandas as pd
import random
import math


path = "./Stock_Data/Data_CAC.csv"
df = pd.read_csv(path,delimiter=";")
df.head()
class Assets :
    def __init__(self,name, values = [],returns = []):
        self._name = name
        self._values = values
        self._returns = returns  # je crois que ça sert a rien ça

    def set_value(self):
        price_list = df[self._name]
        val = []
        for index in range(0,len(price_list)):
            val.append(price_list[index])
        self._values = val
        
    def set_returns(self,rowling_windows = 256): # je crois que ça sert a rien ça
        ret = []
        for comptr in range(1,rowling_windows) :
            ret.append(0) # Definir les premiers éléments sur 0
        for index in range(rowling_windows,len(self._values)) : 
            '''
            returns selon la rowling windows
            '''
            ret.append(self._values[index]/self._values[index-rowling_windows] - 1)
        self._returns = ret
    def get_return(self):
        rendement = 0
        for index in range(1,len(self._values)):
            tamp = self._values[index]/self._values[index-1] - 1
            if math.isnan(tamp)==False:
                rendement = rendement + tamp
        # Calcul du rendement moyen sur les donnée dispo ( pas de fenetre parametrable pour le moment) : 
        return rendement / (len(self._values)-1)  

    def get_moy(self):
        moy = 0
        for val in self._values:
            moy = moy + val
        return moy / len(self._values)
    
    def get_ecart_type(self):
        '''
        calcul de la moyenne
        '''
        moy = 0
        for val in self._values:
            moy = moy + val
        var = 0        
        for val in self._values:
            var = var + (val-moy)**2
        return (var)**(1/2)
    
def creation_liste_dassets():
    ''' 
    Creation de toute les instance de la classe assets 
    '''
    name = df.columns[1:] # Recuperation des noms des actifs
    portfolio = []
    for each in name : 
        assets_test =  Assets(each)
        assets_test.set_value()
        portfolio.append(assets_test)
    return portfolio
def creation_individu():
    list_wi = [random.uniform(0,1) for i in range(len(list_assets))] # Generation des poids aléa
    Total = sum(list_wi)
    list_wi = [i/Total for i in list_wi] # La c'est juste pour s'assurer que les poids somme à 1
    
    couple_assets_poids = {} # On va faire sous forme de dictionnaire ça va etre plus simple
    index_poids = 0 
    for assets in list_assets:
        couple_assets_poids[assets] = list_wi[index_poids]
        index_poids += 1
    return couple_assets_poids #c'est un portfolio en faite
def Population_initiale(list_assets):
    '''
    Generation population de depart
    ''' 
    pop = []
    for indiv in range(0,99) : # pop depart = 100 indiv
        pop.append(creation_individu())
    return pop

def fonction_de_mutation(pop_mere,pourcentage_de_mutation):
    nb_a_modif = round(len(pop_mere) * pourcentage_de_mutation/100) # % de la population qui sera muté
    list_index_a_modif = [round(random.uniform(0,len(pop_mere)-1)) for i in range(nb_a_modif)] # generation d'indexs aleas
    for index in list_index_a_modif:
        pop_mere[index] = creation_individu() # Creation d'un individu aleatoire à l'index aleatoire
    return pop_mere

def fonction_de_croisement(pop_A):
    '''
    On va faire en sorte que chaque indiv de la pop mere ait une descendance avec un partenaire alea 
    De plus, chaque couple parent pourra avoir aleatoirement 1,2 ou 3 enfants ( ou plus si il est choisi aleatoirement par un autre parent).
    Enfin, chaque enfant recevra une part alea de chaque parent
    '''
    pop_enfant=[]
    for indiv_A in pop_A:
        nb_enfant = round(random.uniform(1,3)) # nb enfant alea
        index_partenaire_alea = round(random.uniform(0,len(pop_A)-1)) # partenaire alea
        for compteur_denfant in range(1,nb_enfant+1):
            enfant = {} # enfant vide
            for clé in indiv_A.keys():
                A_ou_B = round(random.uniform(1,2)) # alea sur hérédité de parent A ou B pour chaque assets
                if A_ou_B == 1:
                    enfant[clé] = indiv_A[clé] # on prends le poids de l'assets clé du parent A
                elif A_ou_B == 2:
                    enfant[clé] = pop_A[index_partenaire_alea][clé]# on prends le poids de l'assets clé du parent alea B
                else:
                    print("erreur sur A_ou_B")
            pop_enfant.append(enfant)
    return pop_enfant

def cov_assets(assets_A,assets_B):
    moy_A = assets_A.get_moy()
    moy_B = assets_B.get_moy()
    
    cov = 0
    for index in range(len(assets_A._values)):
        cov = cov + (assets_A._values[index]-moy_A)*(assets_B._values[index]-moy_B)
    return cov/len(assets_A._values)

'''
     5 minute pour la vol d'un seul portfolio, on va s'en passer pour le moment
     car le problème c'est qu'on est censé calculer la vol de 100+ portfeuille a chaque generation
     et y'a au moins 1000 gen je pense donc bon
'''
def volatility_portfolio(portfolio): # on s'en passe pour le prototype
    vol_1 = 0
    vol_2 = 0 # je separe les 2 membres du calcul de vol pour que ce soit plus clair
    for assets in portfolio.keys():
        vol_1 = vol_1 + portfolio[assets]*assets.get_ecart_type() # en gros somme des poids i * ecart type i
    for assets_i in portfolio.keys():
        for assets_j in portfolio.keys():
            if assets_i != assets_j:
                vol_2 = vol_2 + portfolio[assets_i]*portfolio[assets_j]*cov_assets(assets_i,assets_j)
                #en gros, poid i * poiid j * cov(i,j)
    
    return vol_1 + vol_2
        

def score_portfolio(portfolio):
    '''
    calcul du score : Moy(wi*ri/vol) normalement mais pour le proto on va juste faire moy(wi*ri)
    '''
    score = 0
    for assets in portfolio.keys():
        score = score + assets.get_return()*portfolio[assets]
    return score/len(portfolio)

def fitness(pop): # attribution d'un score à chaque portefeuille
    portoflio_et_score = {}
    for indiv in pop:
        score_indiv = score_portfolio(indiv)
        portoflio_et_score[score_indiv] = indiv
    return portoflio_et_score

def tri_selon_score(pop_fitée):
    sortedDict = sorted(pop_fitée.items(), key=lambda x: x[0], reverse=True)
    return sortedDict

def selection(pop_trié):
    selection = []
    for index in range(95):
        selection.append(pop_trié[index])# on garde les 95 meilleur
    index_alea = [round(random.uniform(0,len(pop_trié)-1)) for i in range(5)]
    for index in index_alea:
        selection.append(pop_trié[index]) # on garde 5 aléa
    return selection

def recuperation_liste_sans_score(list_tuple):
    liste = []
    for tupl in list_tuple:
        liste.append(tupl[1])
    return liste


def boucle_génétique(generation,nb_géné):
    if(nb_géné<5): # pour l'instant on fait que 5 generation on verra plus tard, sinon c'est trop long
        print('Generation numero {}'.format(nb_géné))
        nb_géné += 1
        
        pop_mutée = fonction_de_mutation(generation,20) # mutation
        pop_enfant = fonction_de_croisement(pop_mutée) # croisement
        pop_fusion = fusion(pop_enfant,pop_mutée)
        pop_fitée = fitness(pop_fusion) # fit
        pop_triée = tri_selon_score(pop_fitée) # tri
        gene_2 = selection(pop_triée) # séléction
        gene_2_sans_score = recuperation_liste_sans_score(gene_2)  
        return boucle_génétique(gene_2_sans_score,nb_géné)
    else:
        return generation
    
    
def fusion(pop_A,pop_B):
    for index in range(len(pop_B)):
        pop_A.append(pop_B[index])
    return pop_A

if __name__ == '__main__':
    list_assets = creation_liste_dassets()
    pop_0 = Population_initiale(list_assets)
    
#    pop_0_mutée_test = fonction_de_mutation(pop_0,20)
#    pop_enfant_test = fonction_de_croisement(pop_0) # Je comrpends pas pourquoi parfois len(pop_enfant)<len(pop_parent)
#    #normalement c'est impossible
#    pop_fitée = fitness(pop_enfant_test)
#    #print(max(pop_fitée.keys()))
#    pop_triée = tri_selon_score(pop_fitée)
#    gene_2 = selection(pop_triée)
    
    
    pop_final = boucle_génétique(pop_0,0)
         
    for assets in pop_final[0].keys() : # [0] donne le meilleur de la derniere gen
        print('Stock : {} poids {} %'.format(assets._name, pop_final[0][assets]*100))