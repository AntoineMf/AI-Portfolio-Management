from Sql_connection2 import Sql_connection
import  random
from Asset import Asset

class Portfolio():
    
    '''
    This class allows you to create a portfolio object, it is composed of a list of object assets.

    With this class we can obtain the value of a portfolio, create a portfolio containing randomly purchased assets,
    and we can display this portfolio.
    '''
    
    def __init__(self, list_assets, score):
        self.list_assets=list_assets
        self.score=score
    
    
    def value_portfolio(self):
        '''
        Function that takes as argument the portfolio object and 
        calculates the value of the portfolio according to the weight assigned to each asset.
        it returns this value as an integer
        '''
        #It allows to calculate the value of the partoflio
        list_assets=self.list_assets
        value=0
        size = len(list_assets)
        i=0
        while i<size:
            # It allows to replace ',' by '.' to be able to use the value of the shares
            #value_shares = re.sub('\,+', '.', list_assets[i].value)
            value = value + list_assets[i].value*int(list_assets[i].nb_shares)
            i=i+1
        return value
    
    
    def create_random_portfolio(self, max_invest):
        '''
        Function that takes as argument the wallet object,
        and an integer representing the value you wish to invest in a portfolio.

        the function "fills" a portfolio object by randomly assigning a weight to each asset
        it returns the wallet object 
        '''
        # Create a random portfolio
        list_assets = self.list_assets
        # We don't have to go past the max that we have to invest 
        i=0
        size= len(list_assets)
        while i<size:
            list_assets[i].nb_shares=0
            i=i+1
        while(self.value_portfolio()<max_invest):
            # We take randomly the shares to buy
            choice_assets= random.randint(0,len(list_assets)-1)
            # We chose randomly the number of shares to buy
            max_value = max_invest//((list_assets[choice_assets].value)*(size/2))
            #max_value = max_invest//(list_assets[choice_assets].value)
            nb_shares = random.randint(0,max_value)
            list_assets[choice_assets].nb_shares=nb_shares
        i=0
        while i<len(list_assets):
            poids = list_assets[i].value * list_assets[i].nb_shares
            percentage = poids/self.value_portfolio()
            self.list_assets[i].percentage=percentage
            i=i+1
        return self



    def __repr__(self):
        return "{0}\nScore of the portfolio : {1}\n\n".format(self.list_assets,self.score) 


if __name__=="__main__":
    
    connection = Sql_connection('PI2','root','DFCOfoot')
    connection.initialisation()
    
    date_test="01/07/2013"
    max_invest=5000
    Portfeuille = Portfolio(Asset.assign_value_assets(Asset.create_assets(connection),date_test,connection),1)
    Portfeuille_aléa = Portfeuille.create_random_portfolio(max_invest)
    #Portfeuille_aléa.afficher_portfolio()
    print(Portfeuille_aléa)
    
    connection.close_connection()
