# Libs
import time
from time import strftime, gmtime
from tracemalloc import start
import copy

# Class Packages
from Asset import *
from Portfolio import *
from Population import *

# Genetic Algorithm Class
class Genetic__Algorithm:
    # --- Constructor and Attributes --- #
    def __init__(self, nb_gen=10):
        self.nb_gen = nb_gen

    # --- Genetic Loop Module --- #
    @staticmethod
    def recuperation_liste_sans_score(list_tuple):
        liste = []
        for tupl in list_tuple:
            liste.append(tupl[1])
        return liste
    
    # Get Crossover-Mutation Results
    # Crossover
    def get_crossover_result(self, population):
        child_portfolio_list = []
        for portfolio in population._list_portfolio:# parcours des portfeuille dans la pop
            alea_B_index = rd.randrange(0, len(population._list_portfolio)-1) # partenaire alea
            child_portfolio_list_i = [portfolio.Crossover(partner=population._list_portfolio[alea_B_index]) for i in range(rd.randrange(1,3))]
            child_portfolio_list.extend(child_portfolio_list_i)
        population._list_portfolio.extend(child_portfolio_list)
        return population
    
    # Mutation
    def get_mutation_result(self, population, df_returns, mutation_rate):
        nb_modif = round(len(population._list_portfolio) * mutation_rate/100) # % de la population qui sera muté
        list_index_a_modif = [rd.randrange(0,len(population._list_portfolio)-1) for i in range(nb_modif)] # generation d'indexs aleas
        for index in list_index_a_modif:
            population._list_portfolio[index].Mutate(df_returns=df_returns)
        return population
    
    # Genetic Loop Method
    # Faire plusieurs Muation jusqu'a atteindre un minimum local (voir global)
    def genetic_loop(self, start_population, df_returns, mutation_rate=20, max_iter=100):
        start_time = time.time()
        # Set the best Population as the start population
        best_indv_population = copy.deepcopy(start_population)

        # Iterate to find a better combination
        iterations = 0
        crossover_mutation_counter  = 0
        pop_size = len(start_population._list_portfolio)
        while iterations < max_iter:
            # Crossover/Mutation + compare its fitness to the current best fitness
            child_population = self.get_crossover_result(population=copy.deepcopy(best_indv_population))
            child_population = self.get_mutation_result(df_returns=df_returns, population=child_population, mutation_rate=mutation_rate)
            crossover_mutation_counter += 1

            # Calculate the fitness of the new population's Individuals
            [portfolio.fitness() for portfolio in child_population._list_portfolio]
            child_population._list_portfolio.sort(key=lambda portfolio: portfolio._sharp_score, reverse=True)
            if child_population.get_best_portfolio_fitness() > best_indv_population.get_best_portfolio_fitness():
                best_indv_population = copy.deepcopy(child_population)
                best_indv_population._list_portfolio = best_indv_population._list_portfolio[:pop_size]
                iterations = 0  # Reset iteration counter until if a new best is found (as far as it didnt reach max iter)
            else:
                iterations += 1  # Increment counter until it reaches max iter or until it is reset 
        return best_indv_population, crossover_mutation_counter, round(time.time() - start_time, 3)
