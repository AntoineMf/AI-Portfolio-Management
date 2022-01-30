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

# Class Packages
from GeneticAlgorithm import Genetic__Algorithm
from Asset import *
from Portfolio import *
from Population import *
        


# --- Main --- #
# Get Data from source
path = "Data_CAC.csv"
df = pd.read_csv(path,delimiter=";")
print(df)

# Get Asset list and Init start population
gen_algo = Genetic__Algorithm(df, nb_gen=10)
list_assets = gen_algo.creation_dassets(nb_days=255) # creation des instance de la classe assets 
start_population = Genetic__Algorithm.Population_initiale(list_assets, taille=100)
# porfolio = creation_portfolio_alea(list_assets) # creation de l'instance de la classes portfolio

#    print(len(pop_0._list_porfolio[1]._list_assets[1]._values))

#    pop_0_mutée_test = fonction_de_mutation(pop_0,20)
#    pop_enfant_test = fonction_de_croisement(pop_0) # Je comrpends pas pourquoi parfois len(pop_enfant)<len(pop_parent)
#    #normalement c'est impossible
#    pop_fitée = fitness(pop_enfant_test)
#    #print(max(pop_fitée.keys()))
#    pop_triée = tri_selon_score(pop_fitée)
#    gene_2 = selection(pop_triée)


final_population = gen_algo.genetic_loop(start_population)
total = 0   
for assets in final_population._list_porfolio[0]._list_assets: # [0] donne le meilleur de la derniere gen
    print('Stock : {} poids {} %'.format(assets._name, assets._weigth*100))
    
# Print Resultats
print('\nSharpe : {} '.format(final_population._list_porfolio[0]._score) +
        'rendement : {}  %'.format(final_population._list_porfolio[0].rendement_moyen()) +
        'vol : {} '.format(final_population._list_porfolio[0]._volatility))

    