# ------------- Main to test the different classes ------------- #

# Packages
import pandas as pd
from Returns import Returns
from VarCov import VarCov
from ListOfAsset import ListOfAsset
from Genetic_Algorithm import GeneticAlgorithm
from datetime import datetime
from Sql_connection import SqlConnection
import matplotlib.pyplot as plt


def modifyDateFormat(x):
    dateObject = datetime.strptime(str(x), '%Y-%m-%d')
    return dateObject.strftime('%d/%m/%y')


def Main_Principal(yield_value, vol_value):

    # Remplacer la partie base de donnee par ce qui est en commentaire (pour pouvoir executer le code)
    """
    path = "Data_CAC.csv"
    df = pd.read_csv(path, delimiter=";")
    sprint(df.head())
    dates = df.pop("Date")
    names = df.columns
    """
    # Periode sur laquelle on calcule les returns
    nODays = 3
    # Nombre de returns a calculer
    nORet = 5

    # Dates entre lesquelles sont calculees les returns
    date1 = '2018/03/01'
    date2 = '2018/03/27'

    # Partie Base de donnee a commenter
    mycursor = SqlConnection()
    rawtitre = mycursor.execute("SELECT * FROM Equity;")
    mycursor.close_connection()

    names = []
    for i in rawtitre:
        names.append(i[0])

    price = []
    for i in names:
        resultat = SqlConnection.requete(date1, date2, i)
        price.append(resultat[1])
        dates = resultat[0]

    df = pd.DataFrame(price, index=names).T
    # Fin de la partier a commenter

    returns = Returns(df, nODays, names, nORet)
    cov = VarCov(returns.matrixReturns)
    assets = ListOfAsset(names, df, dates, returns, cov)
    aiTest = GeneticAlgorithm(assets, 100000, 100, yield_value, vol_value)

    plt.scatter(aiTest.x, aiTest.y, c='blue')
    plt.scatter(vol_value, yield_value, c='red', marker='x')
    plt.scatter(float(aiTest.ResultFloat[1]), float(aiTest.ResultFloat[0]), c='green')

    plt.show()
    return aiTest
