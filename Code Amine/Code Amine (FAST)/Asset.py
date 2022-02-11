# Libs
import random, math
import numpy as np

# Class of a single Asset
class Asset :
    # --- Constructor and Attributes --- #
    def __init__(self,name, prices = [], returns_list=[], weight=0, rendement_moy=0):
        self._name = name
        self._prices = prices
        self._returns_list = returns_list 
        self._rendement_moy = rendement_moy
        self._weight = weight
        self._volatility = 1 # ???   astype(float).cov()

    # --- Usefull Methods --- #
    # recuperation des prices depuis aujd jusqu'a (aujourd'hui - time_en_jours)
    def set_value(self, df, time_en_jours):
        price_list = list(df[self._name])
        val = []
        for index in range(1,time_en_jours):
            val.append(price_list[-index]) # - index permet de recupérer le dernier, l'avant dernier ... jusqu'a time
        self._prices = val
    
    # Calculate Returns for volatility
#    def set_returns(self,time_en_jours = 256): # je crois que ça sert a rien ça
#        ret = []
#        for comptr in range(1,time_en_jours) :
#            ret.append(0) # Definir les premiers éléments sur 0
#        for index in range(time_en_jours,len(self._prices)) : 
#            '''
#            returns selon la rowling windows
#            '''
#            ret.append(self._prices[index]/self._prices[index-time_en_jours] - 1)
#        self._returns = ret

    # Calculate Returns and Avg-Yield
    def set_avg_yield_returns(self):
        rendement = 0
        for t in range(1, len(self._prices)):
            temp = ((self._prices[t]/self._prices[t-1]) -1)*100  # x100 ???
            rendement = rendement + temp
            self._returns.append(temp)
        self._rendement_moy = (rendement / len(self._prices))*100  # x100 ?
    
    # Calculate Volatility based on returns
    def set_volatility(self, default=0):
        if default==1:
            return 1
        else:
            self._volatility = math.sqrt(np.cov(self._returns))  # list returns:   vol = sum des diags
        

    def set_weight(self, weight):
        self._weight = weight
        
    def set_alea_weights(self):
        self._weight = random.uniform(0,1)
        
    def get_weight(self):
        return self._weight
    
    def get_moy(self):
        moy = 0
        for val in self._prices:
            moy = moy + val
        return moy / len(self._prices)
    
    def set_ecart_type(self):
        '''
        calcul de l'ecart-type des prix de l'assets
        '''
        moy = 0
        for val in self._prices:
            moy = moy + val
        moy = moy/len(self._prices)
        var = 0        
        for val in self._prices:
            var = var + (val-moy)**2
        self._ecart_type = (var)**(1/2)

    @staticmethod
    def cov_assets(assets_A, assets_B):
        moy_A = assets_A.get_moy()
        moy_B = assets_B.get_moy()
        
        cov = 0
        for index in range(len(assets_A._prices)):
            cov = cov + (assets_A._prices[index]-moy_A)*(assets_B._prices[index]-moy_B)
        return cov/len(assets_A._prices)