# --- Libs --- #
import random as rd
import numpy as np
from Portfolio import *
import copy

# Class Population (list of Portfolios)
class Population :
    # --- Constructor and Attributes --- #
    def __init__(self, list_portfolio=[]):
        self._list_portfolio = list_portfolio

    # --- Crossover/Mutation Module --- #
    # Crossover
    def get_crossover_result(self):
        child_portfolio_list = []
        for portfolio in self._list_portfolio:# parcours des portfeuille dans la pop
            alea_B_index = rd.randrange(0, len(self._list_portfolio)-1) # partenaire alea
            child_portfolio_list_i = [portfolio.Crossover(partner=self._list_portfolio[alea_B_index]) for i in range(rd.randrange(1,3))]
            child_portfolio_list.extend(child_portfolio_list_i)
        list_portfolio = [portfolio for portfolio in self._list_portfolio]
        list_portfolio.extend(child_portfolio_list)
        return Population(list_portfolio=list_portfolio)

    # Mutation
    def get_mutation_result(self, df_returns, mutation_rate, best_indv_population):
        nb_modif = round(len(self._list_portfolio) * mutation_rate/100) # % de la population qui sera muté
        list_index_a_modif = [round(rd.uniform(0,len(self._list_portfolio)-1)) for i in range(nb_modif)] # generation d'indexs aleas
        list_portfolio = [portfolio for portfolio in self._list_portfolio]
        print("best during Mutation (before mutate function) = " + str(best_indv_population.fitness_Al()))
        list_portfolio = [list_portfolio[index].Mutate(df_returns=df_returns) for index in list_index_a_modif]
        return Population(list_portfolio=list_portfolio)


    # --- Fitness Module --- #
    def get_best_portfolio_fitness(self):
        return round(self._list_portfolio[0]._sharp_score, 5)
    
    def selection(self, nb_conservation, alea_rescape):
        #index_alea = [round(rd.uniform(0,len(self._list_portfolio)-1)) for i in range(alea_rescape)]
        index_alea = rd.sample(range(len(self._list_portfolio)-1), alea_rescape)
        rescape = []
        for index in index_alea:
            rescape.append(self._list_portfolio[index]) # on garde aléa
        
        self._list_portfolio[nb_conservation:]# on garde les "conservation" meilleur
        for portfolio in rescape:
            self._list_portfolio.append(portfolio)
        self._nb_indiv = len(self._list_portfolio) # reparametrage de nb_indiv
        
        # return selection
    
