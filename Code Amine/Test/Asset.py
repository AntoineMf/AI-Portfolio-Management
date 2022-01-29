# ------------- Asset Class ------------- #
# Packages

# Libs
import math, random

# Asset Class
class Asset :
    def __init__(self,name, values = [],returns = [],weigth = 0,ecart_type=0,rendement = 0):
        self._name = name
        self._values = values
        self._returns = returns  # je crois que ça sert a rien ça
        self._weigth = weigth
        self._ecart_type = ecart_type
        self._rendement_moy = rendement

    def set_value(self, df, time_en_jours):
        '''
        recuperation des prices depuis aujd jusqu'a (aujourd'hui - time_en_jours)
        '''
        price_list = list(df[self._name])
        val = []
        for index in range(1,time_en_jours):
            val.append(price_list[-index]) # - index permet de recupérer le dernier, l'avant dernier ... jusqu'a time
        self._values = val
        
#    def set_returns(self,time_en_jours = 256): # je crois que ça sert a rien ça
#        ret = []
#        for comptr in range(1,time_en_jours) :
#            ret.append(0) # Definir les premiers éléments sur 0
#        for index in range(time_en_jours,len(self._values)) : 
#            '''
#            returns selon la rowling windows
#            '''
#            ret.append(self._values[index]/self._values[index-time_en_jours] - 1)
#        self._returns = ret
        
   
    def set_return(self):
        rendement = 0
        for index in range(1,len(self._values)):
            tamp = self._values[index]/self._values[index-1] - 1
            if math.isnan(tamp)==False:
                rendement = rendement + tamp
        # Calcul du rendement moyen sur les donnée dispo ( pas de fenetre parametrable pour le moment) : 
        self._rendement_moy = rendement / (len(self._values)-1)  

    def set_weigth(self,weight):
        self._weigth = weight
        
    def set_weigth_alea(self):
        self._weigth = random.uniform(0,1)
        
    def get_weigth(self):
        return self._weigth
    
    def get_moy(self):
        moy = 0
        for val in self._values:
            moy = moy + val
        return moy / len(self._values)
    
    def set_ecart_type(self):
        '''
        calcul de l'ecart-type des prix de l'assets
        '''
        moy = 0
        for val in self._values:
            moy = moy + val
        moy = moy/len(self._values)
        var = 0        
        for val in self._values:
            var = var + (val-moy)**2
        self._ecart_type = (var)**(1/2)