# Libs
import time
from time import strftime, gmtime

# Class Packages
from Asset import *
from Portfolio import *
from Population import *

# Genetic Algorithm Class
class Genetic__Algorithm:
    # --- Constructor and Attributes --- #
    def __init__(self, df=None, nb_gen=10):
        self.df = df
        self.nb_gen = nb_gen

    # --- Useful Methods --- #
    def creation_dassets(self, nb_days):
        ''' 
        Creation de toute les instance de la classe assets 
        '''
        name = self.df.columns[1:] # Recuperation des noms des actifs
        portfolio = []
        for each in name : 
            assets =  Asset(each)
            assets.set_value(self.df, nb_days)
            assets.set_ecart_type()
            assets.set_return()
            portfolio.append(assets)
        return portfolio

    @staticmethod
    def Population_initiale(list_assets, taille=100):
        '''
        Generation population de depart
        ''' 
        tamp=[]
        for indiv in range(taille) : # pop depart = 100 indiv
            tamp.append(Portfolio.creation_portfolio_alea(list_assets))
        pop = Population(tamp)
        return pop

    # --- Genetic Loop --- #
    @staticmethod
    def recuperation_liste_sans_score(list_tuple):
        liste = []
        for tupl in list_tuple:
            liste.append(tupl[1])
        return liste
        
    # Genetic Loop Method
    def genetic_loop(self, individu_pop):
        loop_duration = 0
        for current_gen in range(self.nb_gen):  # pour l'instant on fait que 5 generation on verra plus tard, sinon c'est trop long
            start_time = time.time()
            print("\n" + "-"*23 + "\n\t Gen " + str(current_gen))
            
            # Crossover
            print("- Crossover...")
            individu_pop.fonction_de_croisement()# croisement
            print("Done.")
            #pop_enfant = fonction_de_croisement(pop_mutée) 
            
            # Mutation
            print("- Mutation...")
            individu_pop.fonction_de_mutation(20) # mutation
            print("Done.")
            #pop_mutée = fonction_de_mutation(generation,20) # mutation
            #pop_fusion = fusion(pop_enfant,pop_mutée)
            
            # Fitness and Sort
            individu_pop.fitness() # fit
            individu_pop.tri_selon_score() # tri
            #pop_triée = tri_selon_score(pop_fitée) # tri

            individu_pop.selection(nb_conservation=95, alea_rescape=5) # séléction 95 meilleur et 5 alea
            #○gene_2 = selection(pop_triée) # séléction
            #gene_2_sans_score = Genetic_Algorithm.recuperation_liste_sans_score(gene_2) 

            # Keep Track of duration
            delay = round(time.time() - start_time, 3)
            print("- Duration: " + str(delay) + " seconds.")
            loop_duration += delay
        loop_duration = strftime("%M min(s) %S sec(s)", gmtime(loop_duration))
        return individu_pop, loop_duration
    
    # Genetic Loop Method (Recursive)
    def genetic_loop_rec(self, individu_pop, current_gen=0):
        if(current_gen < self.nb_gen): # pour l'instant on fait que 5 generation on verra plus tard, sinon c'est trop long
            print('Generation numero {}'.format(current_gen))
            
            # Crossover
            individu_pop.fonction_de_croisement()# croisement
            print("croisement ok")
            #pop_enfant = fonction_de_croisement(pop_mutée) 
            
            # Mutation
            individu_pop.fonction_de_mutation(20) # mutation
            print("mutation ok")
            #pop_mutée = fonction_de_mutation(generation,20) # mutation
            #pop_fusion = fusion(pop_enfant,pop_mutée)
            
            # Fitness and Sort
            individu_pop.fitness() # fit
            individu_pop.tri_selon_score() # tri
            #pop_triée = tri_selon_score(pop_fitée) # tri

            individu_pop.selection(nb_conservation=95, alea_rescape=5) # séléction 95 meilleur et 5 alea
            #○gene_2 = selection(pop_triée) # séléction
            #gene_2_sans_score = Genetic_Algorithm.recuperation_liste_sans_score(gene_2)  

            
            return self.genetic_loop(individu_pop, current_gen=current_gen+1)

        else:
            return individu_pop