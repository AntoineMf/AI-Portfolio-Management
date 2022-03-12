# ------------- Main to test the different classes ------------- #

# Packages
import pandas as pd
import numpy as np
import math
from Asset import Asset
from Returns import Returns
from VarCov import VarCov
from ListOfAsset import ListOfAsset
from Portfolio import Portfolio
#from Genetic_Algorithm import Genetic_Algorithm as Ga
from Population import Population as Pop
from Genetic_Algorithm import Genetic_Algorithm
from sqlalchemy import create_engine
from datetime import datetime
from Sql_connection import Sql_connection

def modifyDateFormat(x):
    dateObject = datetime.strptime(str(x),'%Y-%m-%d')
    return dateObject.strftime('%d/%m/%y')


if __name__ == '__main__':
    path = r"C:\Users\alan7\Documents\A4\pi2\final\AI-Portfolio-Management\Code Aurelien\Data_CAC.csv"
    df = pd.read_csv(path, delimiter=";")
    
    dates = df.pop("Date")
    print("CSV Dataframe")
    print(df.head())
    names = df.columns
    nODays = 1
    nORet = 7

    date1='2014/03/01'
    date2='2014/03/27'

    mycursor=Sql_connection()
    rawtitre=mycursor.execute("SELECT * FROM Equity;")
    mycursor.close_connection()

    names=[]
    for i in rawtitre:
        names.append(i[0])

    price=[]
    for i in names:
        resultat=Sql_connection.requete(date1,date2,i)
        price.append(resultat[1])
        dates=resultat[0]

    df = pd.DataFrame(price, index = names).T
    print("DataBase DataFrame")
    print(df.head())

    """
    db_connection_str= 'mysql+pymysql://pi2:pi2@192.168.196.59/PI2'
    db_connection = create_engine(db_connection_str)
    
    dfDB = pd.read_sql('select * from Stock',con=db_connection)
    
    dfDB['Stock_Date']= dfDB['Stock_Date'].apply(modifyDateFormat)"""
    #print(dfDB)
    #print(len(df))
    #print(len(df.iloc[0]))
    returns = Returns(df, nODays, names, nORet)
    #print(returns)

    cov = VarCov(returns.matrixReturns)
    #print(type(cov.matrix))

    assets = ListOfAsset(names, df, dates, returns, cov)
    #print(assets.listAssets[0].values.loc[0])
    #print(len(assets.listAssets))
    #portfolio = Portfolio(assets, 10000)

    aiTest = Genetic_Algorithm(assets,10000000,100)

    #Pop0=Pop(assets,10000,0,100)
    #print(len(Pop0.listPortfolio))
    #print(portfolio.weights)
    #portfolio.ComputeReturns()
    #print(portfolio.returns)
    #print(assets)
    #print(assets.LastPrices())
    #print(assets.ListOfPrices(5))
    #print(len(assets.ListOfPrices(5)))

    #list_assets = Ga.creation_dassets(df, 255)
    #pop_0 = Ga.Population_initiale(100, list_assets)
    """
    #    print(len(pop_0._list_porfolio[1]._list_assets[1]._values))
    #    pop_0_mutée_test = fonction_de_mutation(pop_0,20)
    #    pop_enfant_test = fonction_de_croisement(pop_0) # Je comrpends pas pourquoi parfois len(pop_enfant)<len(pop_parent)
    #    #normalement c'est impossible
    #    pop_fitée = fitness(pop_enfant_test)
    #    #print(max(pop_fitée.keys()))
    #    pop_triée = tri_selon_score(pop_fitée)
    #    gene_2 = selection(pop_triée)
    """
    """
    pop_final = Ga.boucle_génétique(pop_0, 0)
    total = 0
    for assets in pop_final._list_porfolio[0]._list_assets:  # [0] donne le meilleur de la derniere gen
        print('Stock : {} poids {} %'.format(assets._name, assets._weigth * 100))

    print('Sharpe : {} '.format(pop_final._list_porfolio[0]._score))
    print('rendement : {}  %'.format(Ga.rendement_moyen(pop_final._list_porfolio[0])))
    print('vol : {} '.format(pop_final._list_porfolio[0]._volatility))
    """


