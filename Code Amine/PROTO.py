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
# Libs
import pandas as pd
import random
import math

# Import Classes
from Asset import *
from Portfolio import *
from Population import *


#_________________________________initialisation__________________________

def creation_dassets(df, duree_en_jours):
    ''' 
    Creation de toute les instance de la classe assets 
    '''
    name = df.columns[1:] # Recuperation des noms des actifs
    portfolio = []
    for each in name : 
        assets = Asset(each)
        assets.set_value(df, duree_en_jours)
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

def Population_initiale(list_assets, taille=100):
    '''
    Generation population de depart
    ''' 
    tamp=[]
    for indiv in range(taille): # pop depart = 100 indiv
        tamp.append(creation_portfolio_alea(list_assets))
    pop = Population(tamp)
    return pop
#________________________________________________________________________________

def cov_assets(assets_A, assets_B):
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
                vol_2 = vol_2 + portfolio[assets_i]*portfolio[assets_j]*cov_assets(assets_i, assets_j)
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




# -------- Main --------- #
# Get Data
path = "Data_CAC.csv"
df = pd.read_csv(path, delimiter=";")
print(df)

# Get Assets from data
list_assets = creation_dassets(df, 255) # creation des instance de la classe assets 

# Get a first Portfolio Population pop_0 from the list of Assets
pop_0 = Population_initiale(list_assets, taille=100)
# porfolio = creation_portfolio_alea(list_assets) # creation de l'instance de la classes portfolio

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
    
    
    
    
    
    
    
    
    
    
    
       
   
   
   
   
     