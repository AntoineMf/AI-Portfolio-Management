# Libs
import imp
from Asset import *

# Class Portfolio (List of assets)
class Portfolio :
    def __init__(self,list_assets,score= 0,vol = 0):
        self._list_assets = list_assets
        self._score = score
        self._volatility = vol
    
    def set_score(self,score):
        self._score = score

    def get_vol(self):
        print("j'ai pas compris la formule de Vol")
        return 1
    
    def normalisation_des_poids(self):
        '''
        adaptation de tout les poids pour que ça somme à 1
        '''
        total = 0
        for assets in self._list_assets:
            total = total + assets._weigth
        for assets in self._list_assets:
            assets._weigth = assets._weigth/total 
            
            
    def set_score_portfolio(self): # ratio de sharpe
        '''
        calcul du score : Moy(wi*ri/vol) normalement mais pour le proto on va juste faire moy(wi*ri)
        '''
        tamp = 0
        for assets in self._list_assets:
            tamp = tamp + assets._rendement_moy*assets._weigth/self._volatility
        self._score = tamp/len(self._list_assets)
        

    def Set_vol(self):
        vol_membre_1 = 0 
        vol_membre_2 = 0
        for assets in self._list_assets:
            vol_membre_1 = vol_membre_1 + assets._weigth * assets._ecart_type
        for index_i in range(len(self._list_assets)):
            for index_j in range(index_i,len(self._list_assets)):
                vol_membre_2 = vol_membre_2 + self._list_assets[index_i]._weigth * self._list_assets[index_j]._weigth * Asset.cov_assets(self._list_assets[index_i],self._list_assets[index_j]) 
        self._volatility = vol_membre_1+vol_membre_2

    @staticmethod
    def creation_portfolio_alea(list_assets): 
        for assets in list_assets:
            assets.set_weigth_alea() # initialisation des poids alea
        portfolio = Portfolio(list_assets)
        portfolio.normalisation_des_poids()
        portfolio.Set_vol()
        return portfolio #c'est un portfolio en faite


    #def fusion(pop_A,pop_B):
    #    for index in range(len(pop_B)):
    #        pop_A.append(pop_B[index])
    #    return pop_A
    def rendement_moyen(self) : 
        r = 0
        for assets in self._list_assets:
            r = r + assets._rendement_moy * assets._weigth
        return r/len(self._list_assets)