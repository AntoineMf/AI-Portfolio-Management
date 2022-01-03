from Asset import Asset
from Portfolio import Portfolio
from Fonctions import Fonctions
import re
from math import sqrt
from Sql_connection import Sql_connection



class Fitness():
    
    def __init__(self, portfeuille, date_0):
        self.portfeuille=portfeuille
        self.date_0=date_0
    
    
    def score(portfolio, vola_wanted, rend_wanted,date_0, date_test):
        #score = portfolio.value_portfolio()
        vola=0
        
        v=Fitness.vola_portfolio(portfolio,date_0, date_test)
        vola = Fonctions.carre(v-vola_wanted)
        print("La volatitilité du portfeuille est de :",v,"%")
        r=Fitness.rendement(Fitness.tab_value_portfolio(portfolio,date_0,date_test))
        rend = Fonctions.carre(r-rend_wanted)
        print("Le rendement du portfeuille est de :",r,"%")
        score = vola + rend
        
        return score
    

    
    def tab_actif(name_actif, date_0, date_test):
        tab_actif=[]
        date_0 = Fonctions.date_to_int(date_0)
        date_test = Fonctions.date_to_int(date_test)
        requete = "SELECT * FROM cac where Date>="+str(date_0)+" and Date<"+str(date_test)+";"
        conn = Sql_connection(requete)
        cursor = conn.connection()
        for row in cursor:
            if (row[name_actif]!= 'PX_LAST'):
                value_shares = re.sub('\,+', '.', row[name_actif])
                if (value_shares=='#N/A N/A'):
                    tab_actif.append(1)
                else :
                    tab_actif.append(float(value_shares))
        conn.close_connection(cursor)
        return tab_actif
    
    
    
#############################################
#Rendement
#############################################

    def tab_value_portfolio(portfeuille,date_0, date_test):
        tab_value=[]
        tab_name_assets=Asset.create_assets()
        tab_value_p=[]
        '''requete ="SELECT count(*) from cac40 where Date>="+date_0+";"
        conn = Sql_connection(requete)
        cursor = conn.connection()
        row=cursor.fetchone()
        nb_row = row['count(*)']
        conn.close_connection(cursor)
        '''
        i=0
        while i<len(tab_name_assets):
            tab=Fitness.tab_actif(tab_name_assets[i].name,date_0, date_test)
            tab_value.append(tab)
            i=i+1
        t=0
        while t<len(tab_value[0]):
            j=0
            total=0
            while j<len(tab_value):
                a=portfeuille.list_assets[j].nb_shares*tab_value[j][t]
                total=total+a
                j=j+1
            tab_value_p.append(total)
            t=t+1
        return tab_value_p
    

    def rendement(tab):
        i=0
        res=1
        tab_rend=[]
        while i<len(tab)-1:
            b=(tab[i+1]-tab[i])/(tab[i])
            tab_rend.append(b)
            i=i+1
            
        j=0
        while j<len(tab_rend):
            res=res*(1+tab_rend[j])
            j=j+1
        return (res-1)*100
    

    '''def rendement (portfeuille, date_0):
        value0_assets = Asset.assign_value_assets(Asset.create_assets(),date_0)
        value1_assets = portfeuille.list_assets
        i=0
        value0_portfolio=0
        value1_portfolio=0
        while i<len(value1_assets):
            value0_portfolio = value0_portfolio + value1_assets[i].nb_shares*value0_assets[i].value
            value1_portfolio = value1_portfolio + value1_assets[i].nb_shares*value1_assets[i].value
            i=i+1
        a = value0_portfolio
        b = value1_portfolio
        R = ((b-a)/a)*100
        return R'''


#############################################
#Volatility
#############################################
        

    def variation_actif(tab_actif):
        tab_var=[]
        size = len(tab_actif)
        for i in range(1,size):
            a=(tab_actif[i-1]/tab_actif[i]-1)
            tab_var.append(a)
        return tab_var



    def vola_portfolio(portfeuille, date_0, date_test):
        size=len(portfeuille.list_assets)
        tab=[]
        for i in range(0,size):
            name1 = portfeuille.list_assets[i].name
            a=Fitness.variation_actif(Fitness.tab_actif(name1,date_0, date_test))
            summ=0
            for j in range (0,size):
                name2 = portfeuille.list_assets[j].name
                b=Fitness.variation_actif(Fitness.tab_actif(name2,date_0, date_test))
                value = portfeuille.list_assets[i].percentage * portfeuille.list_assets[j].percentage * Fonctions.covariance(a,b)
                summ = summ + value
            tab.append(summ)
        var_potrfolio=0
        for t in range (0,len(tab)):
            var_potrfolio=var_potrfolio+tab[t]
        volatility_portfolio = sqrt(var_potrfolio)*100*sqrt(252)
        return volatility_portfolio
           

#############################################
#Var historique
#############################################

'''
def VaR_historique(portfolio, confidence_level):

    #récupérer dans un tableau les gains et pertes quotidiens sur les 500 derniers jours
    historique_rendements = []
    for i in range(500) :
        historique_rendements[i] = Fitness.rendement(portfolio, date - (500-i))


    #classer le tableau obtenu par ordre croissant
    returns_croissant = historique_rendements.sort()

    #en fonction de l'intervalle de confiance choisi, on doit récupérer le nième élément de la liste ainsi triée
    position = 500 * (1-(confidence_level/100))
    VaR = returns_croissant[position]
    return VaR
'''

#############################################
#Calmar_ratio
#############################################

'''
#computes the maximum drawdown for a portfolio
def max_drawdown(portfolio):                
    maxdd = 0
    list_returns=Portfolio.list_portfolio_returns
    peak = list_returns[0]
    for return_ in list_returns:
        if return_ > peak: 
            peak = return_
        drawdown = (peak - return_) / peak
        if drawdown > maxdd:
            maxdd = drawdown
    return maxdd  

#computes the calmar ratio of a portfolio
def compute_calmar_ratio(portfolio):
    rp=Return.compute_portfolio_return
    rf=-0.0059              #the risk free rate, its the value on october 27th over 1mo
    return (rp-rf) / max_drawdown(portfolio)

#creates a list of calmar ratio for each portfolio in a population    
def create_list_calmar():
    list_portfolio=Population.list_portfolio
    list_calmar_ratio=[]
    for port in list_portfolio:
        list_calmar_ratio.append(compute_calmar_ratio(port))
    return list_calmar_ratio
'''




if __name__=="__main__":
    
    date_test="05/07/2019"
    date_0="01/07/2018"
    
    max_invest=5000
    portfeuille = Portfolio(Asset.assign_value_assets(Asset.create_assets(),date_test),1)
    portfeuille_aléa = portfeuille.create_random_portfolio(max_invest)
    print(portfeuille_aléa)

    #portfeuille_aléa.score=Fitness.score(portfeuille_aléa,15,5)
    #print(portfeuille_aléa)
    print(Fitness.score(portfeuille_aléa, 15, 5, date_0,date_test))
    #print(Fitness.vola_portfolio(portfeuille_aléa,date_0))
    
