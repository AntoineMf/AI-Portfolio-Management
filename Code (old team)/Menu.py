from Algo_Genetique import Algo_Genetique
from Sql_connection2 import Sql_connection
from Fitness2 import Fitness

def menu(connection):
    print("##############################################################################")
    print("                                  Projet PI2")
    print("##############################################################################")
    print("Quelle est la taille de la population que vous souhaitez ? ")
    taille_pop = int(input())
    print("Sur combien de génération l'algorithme génétique doit fonctionner ? ")
    nb_tour=int(input())
    print("Quel est en terme de score votre objectif à atteindre pour un portfeuille ?")
    objectif = float(input())
    print("Quelle est la somme que vous voulez investir pour constituer votre portfeuille ?")
    max_invest=int(input())
    print("Quelle est la date à laquelle vous voulez lancer l'algorithme ? Format : DD/MM/AAAA")
    date_test=input()
    print("Quelle est la volatilité que vous souhaitez pour votre portfeuille ?")
    vola_wanted=int(input())
    print("Quel est le rendement que vous souhaitez pour votre portfeuille ?")
    rend_wanted=int(input())
    print("Jusqu'à quelle date voulez vous que nos ratios prennent en compte les valeurs ? Format : DD/MM/AAAA")
    date_0=input()
    print("##############################################################################")
    print("                                  Chargement")
    print("##############################################################################")
    algo = Algo_Genetique(taille_pop, nb_tour, objectif, max_invest,date_test, vola_wanted, rend_wanted,date_0)
    mat = Fitness.matrice_variation(connection, date_0, date_test)
    pop_finale=algo.run_algo(connection,mat)
    print("##############################################################################")
    print("                                  Résultat")
    print("##############################################################################")
    print("Le portfeuille idéal selon vos critères est :")
    print(pop_finale[1])
    return 0




connection = Sql_connection('PI2','root','DFCOfoot')
connection.initialisation()

menu(connection)
connection.close_connection()
