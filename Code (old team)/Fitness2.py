from Asset import Asset
from Portfolio import Portfolio
from Fonctions import Fonctions
import re
from math import sqrt
from Sql_connection2 import Sql_connection



class Fitness():
    
    def __init__(self, portfeuille, date_0):
        self.portfeuille=portfeuille
        self.date_0=date_0
    
    
    def score(portfolio, vola_wanted, rend_wanted,date_0, date_test, connection,mat):
        '''
        Function that takes as argument the portfolio object whose score we want to calculate
        Volatility and return, which are two integers and correspond to the characteristics we want for the portfolio.
        the test_date and the date_0 which are two strings and which correspond to the date on which we launch the program and the date on which we calculate the ratios.
        and finally the object connection of the class Sql_connection and the asset variation matrix

        the fais function calls the different methods of the class and returns the portfolio score as an integer.
        '''
        #score = portfolio.value_portfolio()
        vola=0
        #mat = Fitness.matrice_variation(connection, date_0, date_test)

        v=Fitness.vola_portfolio(portfolio,date_0, date_test, connection,mat)
        vola = Fonctions.carre(v-vola_wanted)
        print("La volatitilité du portfeuille est de :",v,"%")
        r=Fitness.rendement(Fitness.tab_value_portfolio(portfolio,date_0,date_test, connection))
        rend = Fonctions.carre(r-rend_wanted)
        print("Le rendement du portfeuille est de :",r,"%")
        score = vola + rend
        print("Le score du portfeuille est de :",score)
        
        return score
    

    
    def tab_actif(name_actif, date_0, date_test, connection):
        '''
        Function that takes as argument the name of the asset in string, the same test_date and date_0
        and the connection object of the class Sql_connection

        the function returns a list of the values of the asset from date_0 to the test_date
        '''
        tab_actif=[]
        date_0 = Fonctions.date_to_int(date_0)
        date_test = Fonctions.date_to_int(date_test)
        requete = "SELECT * FROM cac where Date>="+str(date_0)+" and Date<"+str(date_test)+";"
        cursor = connection.execute(requete)
        for row in cursor:
            if (row[name_actif]!= 'PX_LAST'):
                value_shares = re.sub('\,+', '.', row[name_actif])
                if (value_shares=='#N/A N/A'):
                    tab_actif.append(1)
                else :
                    tab_actif.append(float(value_shares))
        return tab_actif
    
    
    
#############################################
#Rendement
#############################################

    def tab_value_portfolio(portfeuille,date_0, date_test, connection):
        '''
        Function that takes as argument the object portfolio, the date_test and date_0 
        as well as the connection object of the Sql_connection class.

        the function returns a list of portfolio values of integers from date_0 to test_date
        '''
        tab_value=[]
        tab_name_assets=Asset.create_assets(connection)
        tab_value_p=[]
        i=0
        while i<len(tab_name_assets):
            tab=Fitness.tab_actif(tab_name_assets[i].name,date_0, date_test, connection)
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
        '''
        Function that takes as argument an integer list of portfolio values from one date to another.

        it returns the return of this portfolio in percentage 
        '''
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
    


#############################################
#Volatility
#############################################
        

    def variation_actif(tab_actif):
        '''
        Function that takes as argument a list of integers and 
        returns the variation in value between the different integers of the list
        '''
        tab_var=[]
        size = len(tab_actif)
        for i in range(1,size):
            a=(tab_actif[i-1]/tab_actif[i]-1)
            tab_var.append(a)
        return tab_var



    def matrice_variation(connection, date_0, date_test):
        '''
        Function that takes as argument the connection object of the class Sql_connection 
        as well as the date_test and date_0 in DD/MM/YYYYY format

        the return function a matrix including the variations of each asset between the two dates, 
        it is this matrix that is used throughout the program
        '''
        tab_name_assets=Asset.create_assets(connection)
        matrice_value=[]
        matrice_variation=[]
        for asset in tab_name_assets:
            asseti = Fitness.tab_actif(asset.name, date_0, date_test, connection)
            matrice_value.append(asseti)
        for asset in matrice_value:
            asseti = Fitness.variation_actif(asset)
            matrice_variation.append(asseti)
        return matrice_variation
    
    
    
    def vola_portfolio(portfeuille, date_0, date_test, connection, mat):
        '''
        Function that takes as argument the object portfolio, the date_test and date_0 in DD/MM/YYYYY format
        the connection object of the class Sql_connection
        and the asset variation matrix between the two dates

        it returns the volatility of the portfolio between these two dates in the form of an annual percentage
        '''
        tab=[]
        i=0
        while i<len(mat):
            #name1 = portfeuille.list_assets[i].name
            a=mat[i]
            summ=0
            j=0
            while j<len(mat):
                #name2 = portfeuille.list_assets[j].name
                b=mat[j]
                value = portfeuille.list_assets[i].percentage * portfeuille.list_assets[j].percentage * Fonctions.covariance(a,b)
                summ = summ + value
                j=j+1
            tab.append(summ)
            i=i+1
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
    
    connection = Sql_connection('PI2','root','DFCOfoot')
    connection.initialisation()
    
    date_test="05/07/2019"
    date_0="01/07/2018"
    mat = Fitness.matrice_variation(connection, date_0, date_test)

    max_invest=5000
    portfeuille = Portfolio(Asset.assign_value_assets(Asset.create_assets(connection),date_test,connection),1)
    portfeuille_aléa = portfeuille.create_random_portfolio(max_invest)
    print(portfeuille_aléa)
    Fitness.score(portfeuille_aléa, 15, 5, date_0,date_test, connection,mat)
    connection.close_connection()
    
