# -*- coding: utf-8 -*-
"""
Created on Wed Nov 17 20:45:26 2021

@author: maffe
"""


'''

import pyodbc
conn = pyodbc.connect('Driver={SQL Server};'
                      'Server=localhost:3306;'
                      'Database=Price;'
                      'Trusted_Connection=yes;')
cursor = conn.cursor()
cursor.execute('INSERT INTO Titre("cac")')

import mysql.connector as MC

for date in df['Date']:
    j=0
    for values in df.columns:
        
       
        try:
            conn= MC.connect(host='localhost',database='Price',user='root',password="root")
            cursor = conn.cursor()
            req = 'select * from Titre'
            #req1 = 'INSERT INTO Titre(Titre_Nom) VALUES()'
            #infos=(cursor.lastrowid)
            #infos =(cursor.lastrowid,)
        
            req1 = "INSERT INTO Donnee(Donnee_date,Donnee_Value,Titre_Nom) VALUES('"+str(date)+"',"+str(df[values].iloc[j])+",'"+str(values)+"')"
            
            cursor.execute(req1)
            conn.commit()
            Titrelist = cursor.fetchall()
            for titre in Titrelist:
                print('Titre : {}'.format(titre[0]))
            
            j=j+1
            
        except MC.Error as err:
            print(err)
        finally:
            if(conn.is_connected()):
                cursor.close()
                conn.close()
        
'''
import pandas as pd
import random
import math



#_____________________________ASSETS___________________________________________
class Assets :
    def __init__(self,name, values = [],returns = [],weigth = 0,ecart_type=0,rendement = 0):
        self._name = name
        self._values = values
        self._returns = returns  # je crois que ça sert a rien ça
        self._weigth = weigth
        self._ecart_type = ecart_type
        self._rendement_moy = rendement

    def set_value(self,time_en_jours):
        '''
        recuperation des prices depuis aujd jusqu'a (aujourd'hui - time_en_jours)
        '''
        price_list = list(df[self._name])
        val = []
        for index in range(1,time_en_jours):
            val.append(price_list[-index]) # - index permet de recupérer le dernier, l'avant dernier ... jusqu'a time
        self._values = val
        
#    def set_returns(self,time_en_jours = 256): # je crois que ça sert a rien ça
#        ret = []
#        for comptr in range(1,time_en_jours) :
#            ret.append(0) # Definir les premiers éléments sur 0
#        for index in range(time_en_jours,len(self._values)) : 
#            '''
#            returns selon la rowling windows
#            '''
#            ret.append(self._values[index]/self._values[index-time_en_jours] - 1)
#        self._returns = ret
        
   
    def set_return(self):
        rendement = 0
        for index in range(1,len(self._values)):
            tamp = self._values[index]/self._values[index-1] - 1
            if math.isnan(tamp)==False:
                rendement = rendement + tamp
        # Calcul du rendement moyen sur les donnée dispo ( pas de fenetre parametrable pour le moment) : 
        self._rendement_moy = rendement / (len(self._values)-1)  

    def set_weigth(self,weight):
        self._weigth = weight
        
    def set_weigth_alea(self):
        self._weigth = random.uniform(0,1)
        
    def get_weigth(self):
        return self._weigth
    
    def get_moy(self):
        moy = 0
        for val in self._values:
            moy = moy + val
        return moy / len(self._values)
    
    def set_ecart_type(self):
        '''
        calcul de l'ecart-type des prix de l'assets
        '''
        moy = 0
        for val in self._values:
            moy = moy + val
        moy = moy/len(self._values)
        var = 0        
        for val in self._values:
            var = var + (val-moy)**2
        self._ecart_type = (var)**(1/2)
 
#_____________________________PORTFOLIO___________________________________________    
class Portfolio :
    def __init__(self,list_assets,score= 0,vol = 0):
        self._list_assets = list_assets
        self._score = score
        self._volatility = vol
    
    def set_score(self,score):
        self._score = score

    def get_vol(self):
        print("j'ai pas compris la formule de Vol")
        return 1
    
    def normalisation_des_poids(self):
        '''
        adaptation de tout les poids pour que ça somme à 1
        '''
        total = 0
        for assets in self._list_assets:
            total = total + assets._weigth
        for assets in self._list_assets:
            assets._weigth = assets._weigth/total 
            
            
    def set_score_portfolio(self): # ratio de sharpe
        '''
        calcul du score : Moy(wi*ri/vol) normalement mais pour le proto on va juste faire moy(wi*ri)
        '''
        tamp = 0
        for assets in self._list_assets:
            tamp = tamp + assets._rendement_moy*assets._weigth/self._volatility
        self._score = tamp/len(self._list_assets)
        
    def Set_vol(self):
        vol_membre_1 = 0 
        vol_membre_2 = 0
        for assets in self._list_assets:
            vol_membre_1 = vol_membre_1 + assets._weigth * assets._ecart_type
        for index_i in range(len(self._list_assets)):
            for index_j in range(index_i,len(self._list_assets)):
                vol_membre_2 = vol_membre_2 + self._list_assets[index_i]._weigth * self._list_assets[index_j]._weigth * cov_assets(self._list_assets[index_i],self._list_assets[index_j]) 
        self._volatility = vol_membre_1+vol_membre_2

#_____________________________POPULATION_______________________________

class Population :
    def __init__(self,list_porfolio=[],nb_indiv=0):
        self._list_porfolio = list_porfolio
        self._nb_indiv = len(list_porfolio)
        
    def fonction_de_mutation(self,pourcentage_de_mutation):
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
    
    def fitness(self): # attribution d'un score à chaque portefeuille de la pop
        for portefeuille in self._list_porfolio:
            portefeuille.set_score_portfolio()
        
    def tri_selon_score(self):
        self._list_porfolio.sort(key=lambda v: v._score , reverse=True)
        
    def selection(self,conservation,alea_rescape):
        index_alea = [round(random.uniform(0,len(self._list_porfolio)-1)) for i in range(alea_rescape)]
        rescape = []
        for index in index_alea:
            rescape.append(self._list_porfolio[index]) # on garde aléa
        
        del self._list_porfolio[conservation:]# on garde les "conservation" meilleur
        for portfolio in rescape:
            self._list_porfolio.append(portfolio)
        self._nb_indiv = len(self._list_porfolio) # reparametrage de nb_indiv
        
        # return selection
        
#_________________________________initialisation__________________________

def creation_dassets(df,duree_en_jours):
    ''' 
    Creation de toute les instance de la classe assets 
    '''
    name = df.columns[1:] # Recuperation des noms des actifs
    portfolio = []
    for each in name : 
        assets =  Assets(each)
        assets.set_value(duree_en_jours)
        assets.set_ecart_type()
        assets.set_return()
        portfolio.append(assets)
    return portfolio

def creation_portfolio_alea(list_assets): 
    for assets in list_assets:
        assets.set_weigth_alea() # initialisation des poids alea
    portfolio = Portfolio(list_assets)
    portfolio.normalisation_des_poids()
    portfolio.Set_vol()
    return portfolio #c'est un portfolio en faite

def Population_initiale(taille,list_assets):
    '''
    Generation population de depart
    ''' 
    tamp=[]
    for indiv in range(0,taille) : # pop depart = 100 indiv
        tamp.append(creation_portfolio_alea(list_assets))
    pop = Population(tamp)
    return pop
#________________________________________________________________________________




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


def recuperation_liste_sans_score(list_tuple):
    liste = []
    for tupl in list_tuple:
        liste.append(tupl[1])
    return liste


def boucle_génétique(generation,nb_géné):
    if(nb_géné<100): # pour l'instant on fait que 5 generation on verra plus tard, sinon c'est trop long
        print('Generation numero {}'.format(nb_géné))
        nb_géné += 1
        
        
        
        
        #pop_enfant = fonction_de_croisement(pop_mutée) 
        generation.fonction_de_croisement()# croisement
        print("croisement ok")
        
        
        generation.fonction_de_mutation(20) # mutation
        #pop_mutée = fonction_de_mutation(generation,20) # mutation
        print("mutation ok")
        #pop_fusion = fusion(pop_enfant,pop_mutée)
        
        
        generation.fitness() # fit

        generation.tri_selon_score() # tri
        #pop_triée = tri_selon_score(pop_fitée) # tri

        generation.selection(95,5) # séléction 95 meilleur et 5 alea
        #○gene_2 = selection(pop_triée) # séléction
        #gene_2_sans_score = recuperation_liste_sans_score(gene_2)  

        return boucle_génétique(generation,nb_géné)

    else:
        return generation
    
#    
#def fusion(pop_A,pop_B):
#    for index in range(len(pop_B)):
#        pop_A.append(pop_B[index])
#    return pop_A
def rendement_moyen(portefeuille) : 
    r = 0
    for assets in portefeuille._list_assets:
        r = r + assets._rendement_moy * assets._weigth
    return r/len(portefeuille._list_assets)

if __name__ == '__main__':

    path = "Data_CAC.csv"

    df = pd.read_csv(path,delimiter=";")

    list_assets = creation_dassets(df,255) # creation des instance de la classe assets 
   # porfolio = creation_portfolio_alea(list_assets) # creation de l'instance de la classes portfolio
    pop_0 = Population_initiale(100,list_assets)
#    print(len(pop_0._list_porfolio[1]._list_assets[1]._values))
    
#    pop_0_mutée_test = fonction_de_mutation(pop_0,20)
#    pop_enfant_test = fonction_de_croisement(pop_0) # Je comrpends pas pourquoi parfois len(pop_enfant)<len(pop_parent)
#    #normalement c'est impossible
#    pop_fitée = fitness(pop_enfant_test)
#    #print(max(pop_fitée.keys()))
#    pop_triée = tri_selon_score(pop_fitée)
#    gene_2 = selection(pop_triée)
    
    
    pop_final = boucle_génétique(pop_0,0)
    total = 0   
    for assets in pop_final._list_porfolio[0]._list_assets: # [0] donne le meilleur de la derniere gen
        print('Stock : {} poids {} %'.format(assets._name, assets._weigth*100))
        
    print('Sharpe : {} '.format(pop_final._list_porfolio[0]._score))
    print('rendement : {}  %'.format(rendement_moyen(pop_final._list_porfolio[0])))
    print('vol : {} '.format(pop_final._list_porfolio[0]._volatility))
    
    
    
    
    
    
    
    
    
    
    
       
   
   
   
   
     