from Sql_connection2 import Sql_connection
from Population import Population
import matplotlib.pyplot as plt
from Fitness2 import Fitness
from Fonctions import Fonctions

class Algo_Genetique():
    
    '''
    This class allows to create an Algo_genetic object which is composed of two stopping conditions :
        - A number of turns that the algorithm must perform at the maximum.
        - An objective being a stopping condition of the algorithm if the objective is reached.
    The amount invested as well as the size of the population.

    With this class we can run the genetic algorithm according to the shutdown conditions.
    '''
    
    
    def __init__(self, taille_pop, nb_tour, objectif, max_invest,date_test, vola_wanted, rend_wanted,date_0):
        self.nb_tour=nb_tour
        self.objectif=objectif
        self.max_invest=max_invest
        self.taille_pop=taille_pop
        self.date_test=date_test
        self.date_0=date_0
        self.vola_wanted=vola_wanted
        self.rend_wanted=rend_wanted
        
        

    def run_algo(self,connection,mat):
        '''
        Function that takes as argument the population object, 
        the connection object as well as the asset variation matrix 
        that is calculated in the fitness class.

        It runs the genetic algorithm on the number of periods we want
        and returns the last population generation and the best portfolio according to our criteria. 
        '''
        pop = Population.create_population_random(self.taille_pop, self.max_invest,self.date_test, self.vola_wanted, self.rend_wanted, self.date_0,connection,mat)
        tour = 0
        list_score=[]
        list_moy=[]
        best_portfolio = pop.list_portfolio[0]
        while tour<self.nb_tour:
            pop= pop.sort_population()
            if (pop.list_portfolio[0].score < best_portfolio.score):
                best_portfolio = pop.list_portfolio[0]
            list_score.append(pop.list_portfolio[0].score)
            list_moy.append(Fonctions.moyenne_score(pop))
            if (pop.list_portfolio[0].score<=self.objectif):
                print("L'objectif a été atteint")
                #Algo_Genetique.afficher(list_score)
                break
            pop = pop.crossover('crossover2',self.date_test,connection,mat)
            tour = tour +1
            print("################ Population : "+str(tour)+" ########################")
        
        pop= pop.sort_population()
        list_score.append(pop.list_portfolio[0].score)  
        list_score.append(best_portfolio.score) 
        list_moy.append(Fonctions.moyenne_score(pop))
        print(Fitness.score(best_portfolio,self.vola_wanted, self.rend_wanted, self.date_0, self.date_test,connection, mat))
        
        Algo_Genetique.afficher(list_moy,list_score,best_portfolio)
        return pop,best_portfolio
    
    
    def afficher(list_moy,list_score,best_portfolio):
        '''
        Function that takes as argument an integer array containing the average scores of the populations 
        at each generation, another integer array taking as argument the score of the best portfolio
        at each generation and taking as argument the best portfolio in the form of an object.

        It allows to display the different graphs that allow to make different tests. 
        '''
        plt.plot(list_moy,color="blue")
        plt.ylabel('Moyenne du score de chaque population')
        plt.xlabel("Nombre de générations de population")
        plt.title("Test")
        plt.savefig("test_moy.png")
        plt.show()
        plt.close()
        plt.plot(list_score,color="red")
        plt.ylabel('Score du meilleur portfeuille')
        plt.xlabel("Nombre de générations de population")
        plt.title("Test1, score du meilleur portfeuille : "+str(round(best_portfolio.score,4))+"")
        plt.savefig("test_score.png")
        plt.show()
        plt.close()
        return 0

    
if __name__=="__main__":
    
    connection = Sql_connection('PI2','root','DFCOfoot')
    connection.initialisation()
    
    taille_pop=10
    nb_tour=50
    objectif=0.001
    max_invest=250000
    date_test="01/07/2019"
    date_0="01/07/2018"
    vola_wanted = 14
    rend_wanted = 4
    mat = Fitness.matrice_variation(connection, date_0, date_test)
    a = Algo_Genetique(taille_pop,nb_tour,objectif,max_invest,date_test, vola_wanted, rend_wanted, date_0)
    pop_finale=a.run_algo(connection,mat)


    connection.close_connection()



# Crossover1 mutation1 : 0.06583549491264232
# Corssover2 mutation2 : 0.01462711673515445