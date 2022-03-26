
from tkinter import *
import Main 
# Packages
import pandas as pd
#import numpy as np
#import math
#from Asset import Asset
from Returns import Returns
from VarCov import VarCov
from ListOfAsset import ListOfAsset
#from Portfolio import Portfolio
# from Genetic_Algorithm import Genetic_Algorithm as Ga
#from Population import Population as Pop
from Genetic_Algorithm import Genetic_Algorithm
#from sqlalchemy import create_engine
from datetime import datetime
from matplotlib.figure import Figure 
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,  
NavigationToolbar2Tk) 


def run_algo():
    vol_value = float(vola.get())
    yield_value = float(ret.get())
    aiTest = Main.Main_Principal(yield_value, vol_value)

    # Creation du plot à intégrer
    fig = Figure(figsize = (5, 5), dpi = 100) 
    plot1 = fig.add_subplot(111) 
    plot1.scatter(aiTest.x, aiTest.y, c='blue')
    plot1.scatter(vol_value, yield_value, c='red',marker='x',s=100)
    plot1.scatter(float(aiTest.ResultFloat[1]), float(aiTest.ResultFloat[0]), c='green')
      

    # AFFICHAGE FINAL
    frame_final = Frame(Menu_princ, bg="#5D5B5B", bd=1, relief=SUNKEN)
    retour_f = Label(frame_final, text=aiTest.Result[0], font=("Arial", 40), bg="#5D5B5B", fg="white")
    retour_f.pack()
    vol_f = Label(frame_final, text=aiTest.Result[1], font=("Arial", 40), bg="#5D5B5B", fg="white")
    vol_f.pack()
    canvas = FigureCanvasTkAgg(fig,master = Menu_princ)   
    canvas.draw()  
    canvas.get_tk_widget().pack()
    toolbar = NavigationToolbar2Tk(canvas, Menu_princ) 
    toolbar.update() 
    canvas.get_tk_widget().pack() 
    
    frame_final.pack(expand=YES)




def run_algo2():
     
    # input box
    vol_value = float(vola.get())
    yield_value = float(ret.get())
    # '''Input utilisateur, c'est ça qu'on doit remettre en Affichage User'''
    # print("Insert your expected return on investment\n5% : 0.05")
    # yield_value=float(input())
    # print("Insert the portfolio volatility you are expecting\n5% : 0.05")
    # vol_value=float(input())

    '''Recupération de certaines datas du CSV, temporaire : normalement on va travailler sur la BD'''
    path = "Data_CAC.csv"
    first_df = pd.read_csv(path, delimiter=";")
    df = first_df[['Date', 'DSY FP Equity', 'CAP FP Equity', 'ALO FP Equity',
                  'VIE FP Equity', 'STM FP Equity', 'RMS FP Equity']]
    
    # sprint(df.head())
    
    '''Setup de certaine parametre : NODAYS NORET et la taille du DF'''
    dates = df.pop("Date")
    names = df.columns
    nODays = 5
    nORet = 22
    len_df = df.shape[1]
    """
    db_connection_str= 'mysql+pymysql://pi2:pi2@192.168.196.59/PI2'
    db_connection = create_engine(db_connection_str)
    
    dfDB = pd.read_sql('select * from Stock',con=db_connection)
    
    dfDB['Stock_Date']= dfDB['Stock_Date'].apply(modifyDateFormat)"""
    # print(dfDB)
    # print(len(df))
    # print(len(df.iloc[0]))
    '''Set up des returns a partir de différents paramètre (à input via JSON normalement)
     à partir des données prices (df = données Bloomberg)'''
    returns = Returns(df, nODays, names, nORet)
    # print(returns)
    
    ''' 
    Set up de la matrice de Variance Covariance pour les données bloomberg
    l'objet cov.matrix retourne la mat VARCOV et cov.getvol() permet d'avoir la liste des vol de chaque assets.
    Problème : pas d'indexation claire pr le moment '''
    cov = VarCov(returns.matrixReturns)
    # print(type(cov.matrix))

    '''
    Ici, 2 choses sont faites. Deja création de toute les instance de la classe ASSETS (se fait dans la classe 
    ListOfAssets au niveau du constructeur). ET, création d'une liste de tout les assets comportant leurs prices 
    associé aux dates, les returns etc... Tout le necessaire aux calculs.
    '''
    assets = ListOfAsset(names, df, dates, returns, cov)
    # print(assets.listAssets[0].values.loc[0])
    # print(len(assets.listAssets))
    # portfolio = Portfolio(assets, 10000)

    '''lancement de la boucle géntique, avec la liste d'assets construite, 
    des paramètre d'itération, et des objectif clients. '''
    aiTest = Genetic_Algorithm(assets, 100000, 100, yield_value, vol_value)
    
    ''' Cette partie de l'affichage ne fonctionne pas, elle est à revoir, mais l'affichage final fonctionne
    for item in aiTest.Historique_gen:
        
        for c in Menu_princ.winfo_children(): # clean window
            c.destroy()

        # AFFICHAGE DE CHAQUE GEN
        frame_gen = Frame(Menu_princ,bg = "#5D5B5B",bd = 1,relief = SUNKEN) # Frame et config
        numero_gen = Label(frame_gen,text = item[0])
        numero_gen.pack()
        first = Label(frame_gen,text = item[1])
        sec = Label(frame_gen,text = item[2])
        thrd = Label(frame_gen,text = item[3])
        first.pack()
        sec.pack()
        thrd.pack()
        frame_gen.pack()
        

    for c in Menu_princ.winfo_children(): # clean console
        c.destroy()
    '''
    
    # AFFICHAGE FINAL
    frame_final = Frame(Menu_princ, bg="#5D5B5B", bd=1, relief=SUNKEN)
    retour_f = Label(frame_final, text=aiTest.Result[0], font=("Arial", 40), bg="#5D5B5B", fg="white")
    retour_f.pack()
    vol_f = Label(frame_final, text=aiTest.Result[1], font=("Arial", 40), bg="#5D5B5B", fg="white")
    vol_f.pack()
    frame_final.pack(expand=YES)

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


def cleaning():  # permet à chaque génération d'éffacer la precédente
    for c in Menu_princ.winfo_children():
        c.destroy()


def Print_Info_Gen(texte, texte_first, texte_sec, texte_thrd):
    frame_gen = Frame(Menu_princ, bg="#5D5B5B", bd=1, relief=SUNKEN)  # Frame et config
    numero_gen = Label(frame_gen, text=texte)
    numero_gen.pack()
    first = Label(frame_gen, text=texte_first)
    sec = Label(frame_gen, text=texte_sec)
    thrd = Label(frame_gen, text=texte_thrd)
    first.pack()
    sec.pack()
    thrd.pack()
    frame_gen.pack()


def Print_Final_Result(print_ret, print_vol):
    frame_final = Frame(Menu_princ, bg="#5D5B5B", bd=1, relief=SUNKEN)
    retour_f = Label(frame_final, text=print_ret)
    retour_f.pack()
    vol_f = Label(frame_final, text=print_vol)
    vol_f.pack()
    frame_final.pack()


if __name__ == '__main__':
    # créer premiere fenêtre 
    Menu_princ = Tk()

    # personnaliser fenetre
    Menu_princ.title("Menu")  # Titre fenetre
    Menu_princ.geometry("1080x720")  # Taille à l'ouverture
    Menu_princ.minsize(480, 360)  # Taille minimal
    Menu_princ.iconbitmap("Logo_esilv_png_blanc.ico")  # logo
    Menu_princ.config(background="#5D5B5B")  # couleur fond

    # creer la frame :
    frame = Frame(Menu_princ, bg="#5D5B5B", bd=1, relief=SUNKEN)  # Frame et config

    # ajouter texte :
    label_title = Label(frame, text="Algo Genetique Markowitz", font=("Arial", 40), bg="#5D5B5B", fg="white")
    label_title.pack()

    # ajouter second texte
    label_sub_title = Label(frame, text="Merci de parametrer l'algorithme",
                            font=("Arial", 25), bg="#5D5B5B", fg="white")
    label_sub_title.pack()

    # ajouter champs de saisie : 
    vol_label = Label(frame, text="Entrez volatilité requise", bg="#5D5B5B", fg="white")
    ret_label = Label(frame, text="Entrez returns requis", bg="#5D5B5B", fg="white")
    vola = Entry(frame)
    ret = Entry(frame)
    vol_label.pack()
    vola.pack()
    ret_label.pack()
    ret.pack()

    # Ajouter un bouton
    Run_code = Button(frame, text="Run code", font=("Arial", 25),
                      bg="white", fg="#5D5B5B", command=run_algo)  # lance le code lorsque on appui sur le bouton
    Run_code.pack(pady=25, fill=X)  # affichage et design

    # ajouter frame
    frame.pack(expand=YES)

    # afficher fenetre 
    Menu_princ.mainloop()
