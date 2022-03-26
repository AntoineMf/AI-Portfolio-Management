# ------------- Main to test the different classes ------------- #

# Packages
import pandas as pd
from Returns import Returns
from VarCov import VarCov
from ListOfAsset import ListOfAsset
from Genetic_Algorithm import Genetic_Algorithm
from datetime import datetime
from Sql_connection import Sql_connection
import matplotlib.pyplot as plt

'''Permet de restructurer les dates qu'on traite en DD/MM/AAAA'''


def modifyDateFormat(x):
    dateObject = datetime.strptime(str(x), '%Y-%m-%d')
    return dateObject.strftime('%d/%m/%y')


def Main_Principal(yield_value, vol_value):
    # '''Input utilisateur, c'est ça qu'on doit remettre en Affichage User'''
    # print("Insert your expected return on investment\n5% : 0.05")
    # yield_value = float(input())
    # print("Insert the portfolio volatility you are expecting\n5% : 0.05")
    # vol_value = float(input())

    # path = "Data_CAC.csv"

    # df = pd.read_csv(path, delimiter=";")

    # first_df = pd.read_csv(path, delimiter=";")
    # df = first_df[['Date','DSY FP Equity','CAP FP Equity','ALO FP Equity','VIE FP Equity',
    #             'STM FP Equity','RMS FP Equity']]

    # sprint(df.head())

    # dates = df.pop("Date")
    # names = df.columns
    nODays = 3
    nORet = 5
    # len_df = df.shape[1]
    """
    db_connection_str= 'mysql+pymysql://pi2:pi2@192.168.196.59/PI2'
    db_connection = create_engine(db_connection_str)

    dfDB = pd.read_sql('select * from Stock',con=db_connection)

    dfDB['Stock_Date']= dfDB['Stock_Date'].apply(modifyDateFormat)"""
    # print(dfDB)
    # print(len(df))
    # print(len(df.iloc[0]))
    
    # print(returns)
    # print(type(cov.matrix))
    # print(assets.listAssets[0].values.loc[0])
    # print(len(assets.listAssets))
    # portfolio = Portfolio(assets, 10000)
    
    # dates = df.pop("Date")
    # print("CSV Dataframe")
    # print(df.head())
    # names = df.columns
    # nODays = 1
    # nORet = 7

    date1 = '2018/03/01'
    date2 = '2018/03/27'

    mycursor = Sql_connection()
    rawtitre = mycursor.execute("SELECT * FROM Equity;")
    mycursor.close_connection()

    names = []
    for i in rawtitre:
        names.append(i[0])

    price = []
    for i in names:
        resultat = Sql_connection.requete(date1, date2, i)
        price.append(resultat[1])
        dates = resultat[0]

    # price=[]
    # for i in names:
    #    resultat=Sql_connection.requete(date1,date2,i)
    #    price.append(resultat[1])
    #    dates=resultat[0]

    df = pd.DataFrame(price, index=names).T

    returns = Returns(df, nODays, names, nORet)
    cov = VarCov(returns.matrixReturns)
    assets = ListOfAsset(names, df, dates, returns, cov)
    aiTest = Genetic_Algorithm(assets, 100000, 100, yield_value, vol_value)
    # print("DataBase DataFrame")
    # print(df.head())
    plt.scatter(aiTest.x, aiTest.y, c='blue')
    plt.scatter(vol_value, yield_value, c='red', marker='x')
    plt.scatter(float(aiTest.ResultFloat[1]), float(aiTest.ResultFloat[0]), c='green')

    plt.show()
    return aiTest
    """
    db_connection_str= 'mysql+pymysql://pi2:pi2@192.168.196.59/PI2'
    db_connection = create_engine(db_connection_str)
    
    dfDB = pd.read_sql('select * from Stock',con=db_connection)
    
    dfDB['Stock_Date']= dfDB['Stock_Date'].apply(modifyDateFormat)"""
    """
    #print(dfDB)
    #print(len(df))
    #print(len(df.iloc[0]))
    '''Set up des returns a partir de différents paramètre (à input via JSON normalement)
    à partir des données prices ( df = données Bloomberg )'''
    returns = Returns(df, nODays, names, nORet)
    #print(returns)
    
    ''' 
    Set up de la matrice de Variance Covariance pour les données bloomberg
    l'objet cov.matrix retourne la mat VARCOV et cov.getvol() permet d'avoir la liste des vol de chaque assets. 
    Problème : pas d'indexation claire pr le moment '''
    cov = VarCov(returns.matrixReturns)
    #print(type(cov.matrix))

    '''
    Ici, 2 choses sont faites. Deja création de toute les instance de la classe ASSETS (se fait dans la classe
    ListOfAssets au niveaux du constructeur). ET, création d'une liste de tout les assets comportant leurs
     prices associé aux dates, les returns etc... Tout le necessaire aux calculs.
    '''
    assets = ListOfAsset(names, df, dates, returns, cov)
    #print(assets.listAssets[0].values.loc[0])
    #print(len(assets.listAssets))
    #portfolio = Portfolio(assets, 10000)

    aiTest = Genetic_Algorithm(assets,10000000,100)
    """
    # Pop0=Pop(assets,10000,0,100)
    # print(len(Pop0.listPortfolio))
    # print(portfolio.weights)
    # portfolio.ComputeReturns()
    # print(portfolio.returns)
    # print(assets)
    # print(assets.LastPrices())
    # print(assets.ListOfPrices(5))
    # print(len(assets.ListOfPrices(5)))

    # list_assets = Ga.creation_dassets(df, 255)
    # pop_0 = Ga.Population_initiale(100, list_assets)
    """
    #    print(len(pop_0._list_porfolio[1]._list_assets[1]._values))
    #    pop_0_mutée_test = fonction_de_mutation(pop_0,20)
    #    pop_enfant_test = fonction_de_croisement(pop_0) # Je comrpends pas pourquoi parfois
     len(pop_enfant)<len(pop_parent)
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
