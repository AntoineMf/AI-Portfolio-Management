# ------------- Genetic Algorithm Class ------------- #
# Libraries
import Portfolio
import Population
from Asset import Asset


class Genetic_Algorithm:

    # _________________________________initialisation__________________________
    def __init__(self, df, nb_days):
        pass

    @staticmethod
    def creation_dassets(df, nb_days):
        '''
        Creation de toute les instance de la classe assets
        '''
        name = df.columns[1:]  # Recuperation des noms des actifs
        portfolio = []
        for each in name:
            asset = Asset(each)
            asset.set_value(nb_days)
            asset.set_ecart_type()
            asset.set_return()
            portfolio.append(asset)
        return portfolio

    def creation_portfolio_alea(self, list_assets):
        for assets in list_assets:
            assets.set_weigth_alea()  # initialisation des poids alea
        portfolio = Portfolio(list_assets)
        portfolio.normalisation_des_poids()
        portfolio.Set_vol()
        return portfolio  # c'est un portfolio en faite

    def Population_initiale(self, taille, list_assets):
        '''
        Generation population de depart
        '''
        tamp = []
        for indiv in range(0, taille):  # pop depart = 100 indiv
            tamp.append(self.creation_portfolio_alea(list_assets))
        pop = Population(tamp)
        return pop

    # ________________________________________________________________________________
    @staticmethod
    def cov_assets(assets_A, assets_B):
        moy_A = assets_A.get_moy()
        moy_B = assets_B.get_moy()

        cov = 0
        for index in range(len(assets_A._values)):
            cov = cov + (assets_A._values[index] - moy_A) * (assets_B._values[index] - moy_B)
        return cov / len(assets_A._values)

    '''
         5 minute pour la vol d'un seul portfolio, on va s'en passer pour le moment
         car le problème c'est qu'on est censé calculer la vol de 100+ portfeuille a chaque generation
         et y'a au moins 1000 gen je pense donc bon
    '''

    def volatility_portfolio(self, portfolio):  # on s'en passe pour le prototype
        vol_1 = 0
        vol_2 = 0  # je separe les 2 membres du calcul de vol pour que ce soit plus clair
        for assets in portfolio.keys():
            vol_1 = vol_1 + portfolio[assets] * assets.get_ecart_type()  # en gros somme des poids i * ecart type i
        for assets_i in portfolio.keys():
            for assets_j in portfolio.keys():
                if assets_i != assets_j:
                    vol_2 = vol_2 + portfolio[assets_i] * portfolio[assets_j] * Genetic_Algorithm.cov_assets(assets_i, assets_j)
                    # en gros, poid i * poiid j * cov(i,j)

        return vol_1 + vol_2

    def recuperation_liste_sans_score(self, list_tuple):
        liste = []
        for tupl in list_tuple:
            liste.append(tupl[1])
        return liste

    @staticmethod
    def boucle_génétique(generation, nb_géné):
        if (nb_géné < 100):  # pour l'instant on fait que 5 generation on verra plus tard, sinon c'est trop long
            print('Generation numero {}'.format(nb_géné))
            nb_géné += 1

            # pop_enfant = fonction_de_croisement(pop_mutée)
            generation.fonction_de_croisement()  # croisement
            print("croisement ok")

            generation.fonction_de_mutation(20)  # mutation
            # pop_mutée = fonction_de_mutation(generation,20) # mutation
            print("mutation ok")
            # pop_fusion = fusion(pop_enfant,pop_mutée)

            generation.fitness()  # fit

            generation.tri_selon_score()  # tri
            # pop_triée = tri_selon_score(pop_fitée) # tri

            generation.selection(95, 5)  # séléction 95 meilleur et 5 alea
            # ○gene_2 = selection(pop_triée) # séléction
            # gene_2_sans_score = recuperation_liste_sans_score(gene_2)

            return Genetic_Algorithm.boucle_génétique(generation, nb_géné)

        else:
            return generation

    #
    # def fusion(pop_A,pop_B):
    #    for index in range(len(pop_B)):
    #        pop_A.append(pop_B[index])
    #    return pop_A
    def rendement_moyen(self, portefeuille):
        r = 0
        for assets in portefeuille._list_assets:
            r = r + assets._rendement_moy * assets._weigth
        return r / len(portefeuille._list_assets)
