# Libs
from Asset import *
from Portfolio import *
from Population import *

# Genetic Algorithm Class
class Genetic__Algorithm:
    def __init__(self, df=None, nb_gen=10):
        self.df = df
        self.nb_gen = nb_gen

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

    def genetic_loop(self, individu_pop, current_gen=0):
        if(current_gen < self.nb_gen): # pour l'instant on fait que 5 generation on verra plus tard, sinon c'est trop long
            print('Generation numero {}'.format(current_gen))
            current_gen += 1
            
            #pop_enfant = fonction_de_croisement(pop_mutée) 
            individu_pop.fonction_de_croisement()# croisement
            print("croisement ok")
            
            
            individu_pop.fonction_de_mutation(20) # mutation
            #pop_mutée = fonction_de_mutation(generation,20) # mutation
            print("mutation ok")
            #pop_fusion = fusion(pop_enfant,pop_mutée)
            
            
            individu_pop.fitness() # fit

            individu_pop.tri_selon_score() # tri
            #pop_triée = tri_selon_score(pop_fitée) # tri

            individu_pop.selection(95,5) # séléction 95 meilleur et 5 alea
            #○gene_2 = selection(pop_triée) # séléction
            #gene_2_sans_score = Genetic_Algorithm.recuperation_liste_sans_score(gene_2)  

            return self.genetic_loop(individu_pop, current_gen)

        else:
            return individu_pop