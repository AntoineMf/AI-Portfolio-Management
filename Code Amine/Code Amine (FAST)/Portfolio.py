# Libs
import random as rd
import pandas as pd
from Asset import *

# Class Portfolio (List of assets)
class Portfolio :
    # Constructor and Attributes
    def __init__(self, list_assets):
        self._list_assets = list_assets
        self._rendement = 0
    
    # --- Usefull Methods --- 
    @staticmethod
    def creation_portfolio_alea(list_assets): 
        for asset in list_assets:
            asset.set_alea_weights() # initialisation des poids alea
        portfolio = Portfolio(list_assets)
        portfolio.normalisation_des_poids()
        portfolio.set_volatility()
        return portfolio #c'est un portfolio en faite

    # Usefull Methods
    def Display_Content(self):
        content  = pd.DataFrame(columns=["Asset Name", "Pourcentage"])
        for asset in self._list_assets:
            content = content.append({"Asset Name": asset._name, "Pourcentage": asset._weight*100}, ignore_index=True)
        content = content.sort_values(by=["Pourcentage"], ascending=False).reset_index(drop=True)
        content["Pourcentage"] = content["Pourcentage"].transform(lambda w_p: format(w_p, 'f')[:5] + " %")
        return content


    # --- Calculate Indicators --- #
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
        
    # sumi sumj (wi  wj * cov(return i et j))
    def set_volatility(self, default=0):
        if default == 1:
            return 1
        else:
            self._volatility = sum([asset._weight*asset._volatility for asset in self._list_assets])
            #self._volatility = sum(list_assets_vol)
    
    def Set_vol(self):
        vol_membre_1 = 0 
        vol_membre_2 = 0
        for assets in self._list_assets:
            vol_membre_1 = vol_membre_1 + assets._weight * assets._ecart_type
        for index_i in range(len(self._list_assets)):
            for index_j in range(index_i,len(self._list_assets)):
                vol_membre_2 = vol_membre_2 + self._list_assets[index_i]._weight * self._list_assets[index_j]._weight * Asset.cov_assets(self._list_assets[index_i],self._list_assets[index_j]) 
        self._volatility = vol_membre_1+vol_membre_2
    
    # adaptation de tout les poids pour que ça somme à 1
    def normalisation_des_poids(self):
        total = 0
        for assets in self._list_assets:
            total = total + assets._weight
        for assets in self._list_assets:
            assets._weight = assets._weight/total 
            
    # Score is set as Sharp's ratio
    # rendement moy portfolio / volatility
    def fitness(self): # ratio de sharpe
        rendement = 0
        for asset in self._list_assets:
            rendement += asset._rendement_moy*asset._weight
            #temp = temp + asset._rendement_moy*asset._weight/self._volatility
        self._sharp_score = (rendement/self._volatility)  #calcul du score : Moy(wi*ri/vol) normalement mais on va juste faire moy(wi*ri)
        

    def rendement_moyen(self) : 
        r = 0
        for assets in self._list_assets:
            r = r + assets._rendement_moy * assets._weight
        return r/len(self._list_assets)

    
    """
    def fusion(pop_A,pop_B):
        for index in range(len(pop_B)):
            pop_A.append(pop_B[index])
        return pop_A
    """

    # --- Gen Algo Individual Methods --- #
    def Crossover(self, partner):
        child_asset_list = []  # liste enfant vide
        for idx in range(len(self._list_assets)): # parcours des assets du portefeuille A pour créer l'enfant
            # alea sur hérédité de parent A ou B pour chaque assets (prends le poids de l'assets clé du parent)
            child_asset_list.append(self._list_assets[idx]) if rd.randint(1,2) == 1 else child_asset_list.append(partner._list_assets[idx])
        child_portfolio = Portfolio(list_assets=child_asset_list)
        child_portfolio.normalisation_des_poids()
        child_portfolio.set_volatility() 
        return child_portfolio

    def Mutate(self, df_returns):
        for mut in range((rd.randint(1,3))):
            alea_asset_indx = round(rd.uniform(0, len(self._list_assets)-1))
            self._list_assets[alea_asset_indx].set_alea_weights() # Creation d'un individu aleatoire à l'index aleatoire
            name = self._list_assets[alea_asset_indx]._name
            self._list_assets[alea_asset_indx]._returns_list = df_returns.loc[:, name].tolist()
        self.normalisation_des_poids() # remise de la somme = 1
        self.set_volatility() # remise de la bonne vol
                





















