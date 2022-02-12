# Libs
import imp
from Asset import *

# Class Portfolio (List of assets)
class Portfolio :
    # Constructor and Attributes
    def __init__(self,list_assets,score= 0,vol = 0):
        self._list_assets = list_assets
        self._score = score
        self._volatility = vol
    
    # --- Useful Methods --- #
    '''
        5 minute pour la vol d'un seul portfolio, on va s'en passer pour le moment
        car le problème c'est qu'on est censé calculer la vol de 100+ portfeuille a chaque generation
        et y'a au moins 1000 gen je pense donc bon
    '''
    def volatility_portfolio(self): # on s'en passe pour le prototype
        vol_1 = 0
        vol_2 = 0 # je separe les 2 membres du calcul de vol pour que ce soit plus clair
        for assets in self.keys():
            vol_1 = vol_1 + self[assets]*assets.get_ecart_type() # en gros somme des poids i * ecart type i
        for assets_i in self.keys():
            for assets_j in self.keys():
                if assets_i != assets_j:
                    vol_2 = vol_2 + self[assets_i]*self[assets_j]*Asset.cov_assets(assets_i,assets_j)
                    #en gros, poid i * poiid j * cov(i,j)
        return vol_1 + vol_2
        
    def set_score(self, score):
        self._score = score

    def set_volatility(self, default=0):
        if default == 1:
            return 1
        else:
            self._volatility = sum([asset._weight*asset._ecart_type for asset in self._list_assets])
            #self._volatility = sum(list_assets_vol)
    
    
    # adaptation de tout les poids pour que ça somme à 1
    def normalisation_des_poids(self):
        total = 0
        for assets in self._list_assets:
            total = total + assets._weigth
        for assets in self._list_assets:
            assets._weigth = assets._weigth/total 
            
    # Score is set as Sharp's ratio
    def set_score_portfolio(self): # ratio de sharpe
        tamp = 0
        for asset in self._list_assets:
            tamp = tamp + asset._rendement_moy*asset._weigth/self._volatility
        self._score = tamp/len(self._list_assets)  #calcul du score : Moy(wi*ri/vol) normalement mais on va juste faire moy(wi*ri)
        

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


    """
    def fusion(pop_A,pop_B):
        for index in range(len(pop_B)):
            pop_A.append(pop_B[index])
        return pop_A
    """

    def rendement_moyen(self) : 
        r = 0
        for assets in self._list_assets:
            r = r + assets._rendement_moy * assets._weigth
        return r/len(self._list_assets)