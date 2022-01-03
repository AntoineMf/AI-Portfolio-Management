from Sql_connection2 import Sql_connection
from Portfolio import Portfolio
from Asset import Asset
from Fitness2 import Fitness
import random

class Population() :

    '''
    This class allows to create a population object which is composed of a list of object portfolio.

    With this class you can create a random population, sort it according to a fitness function.
    It is also possible to execute a mutation on the population as well as a cross over.
    And finally we can display the population.
    '''
    
    def __init__(self, list_portfolio, max_invest, vola_wanted, rend_wanted,date_0):
        self.list_portfolio=list_portfolio
        self.max_invest=max_invest
        self.vola_wanted=vola_wanted
        self.rend_wanted=rend_wanted
        self.date_0=date_0
        
        
    def crossover(self, text, date_test,connection,mat):
        '''
        Function that takes as argument the object population, 
        a text format (either crossover1 or crossover2), 
        the test date in string format (DD/MM/YYYYY) 
        as well as the asset variation matrix of the fitness class.

        the function allows to execute either the crossover1 
        or the crossover2 method according to the text variable as argument. 
        '''
        if (text=='crossover1'):
            return self.crossover1(date_test,connection,mat)
        elif (text=='crossover2'):
            return self.crossover1(date_test,connection,mat)
        return 0


    def sort_population(self):
        '''
        Function that takes as argument the object population
        and which allows to sort the portfolios according to their scores.

        it returns the sorted population
        '''
        i=0
        while i<len(self.list_portfolio)-1:
            value1=self.list_portfolio[i].score
            value2=self.list_portfolio[i+1].score
            if(value2<value1):
                a=self.list_portfolio[i]
                self.list_portfolio[i]=self.list_portfolio[i+1]
                self.list_portfolio[i+1]=a
                if (i==0):
                    i=i-1
                else :
                    i=i-2
            i=i+1
        return self
    
    
    def mutation1(self):
        '''
        Function that takes as argument the object population and
        randomly modifies the number of shares of an asset in each portfolio

        it returns the modified portfolio
        '''
        for portfolio in self.list_portfolio :
            asset=random.randint(0,len(portfolio.list_assets)-1)
            portfolio.list_assets[asset].nb_shares=random.randint(0,self.max_invest//(portfolio.list_assets[asset].value*2))
        return self
    
    
    def mutation2(self):
        '''
        Function that takes as argument the object population and
        randomly modifies the number of shares of an asset of one portfolio

        it returns the modified portfolio
        '''
        portfolio_chosen = random.randint(0,len(self.list_portfolio)-1)
        asset_chosen = random.randint(0,len(self.list_portfolio[portfolio_chosen].list_assets)-1)
        a = random.randint(0,self.max_invest//(self.list_portfolio[portfolio_chosen].list_assets[asset_chosen].value*2))
        self.list_portfolio[portfolio_chosen].list_assets[asset_chosen].nb_shares= a
    
    
    def crossover1(self, date_test, connection, mat):
        '''
        Function that takes as argument the object population
        the test_date in the format (DD/MM/YYYY),
        the connection object which corresponds to the class Sql_connection
        as well as the asset variation matrix of the Fitness class
        It allows to perform a crossover on the object population, 
        more precisely a crossover between half of the portfolios of the population according to their score, 
        the other half is replaced by random portfolios.
        
        It calls the mutation function to modify the population just before the return.
        '''
        sort_pop=self.sort_population()
        l=[]
        size_portfolio = len(self.list_portfolio[0].list_assets)
        size_pop=len(self.list_portfolio)
        middle_portfolio = size_portfolio//2
        i=0
        while i<size_pop//2+1:
            j=0
            portfolioo=[]
            while j<middle_portfolio:
                portfolioo.append(sort_pop.list_portfolio[i].list_assets[j])
                j=j+1
            while j<size_portfolio:
                portfolioo.append(sort_pop.list_portfolio[i+1].list_assets[j])
                j=j+1
            i=i+1
            p_ortfolio = Portfolio(portfolioo,1)
            l.append(p_ortfolio)            
        nb_portfolio_random = size_pop-i
        n=0
        while n<nb_portfolio_random:
            list_asset = Asset.assign_value_assets(Asset.create_assets(connection),date_test,connection)
            portfeuille = Portfolio(list_asset,1)
            portfeuille = portfeuille.create_random_portfolio(self.max_invest)
            #portfeuille.score=Fitness.score(portfeuille,self.vola_wanted,self.rend_wanted,self.date_0,date_test,connection)
            l.append(portfeuille)
            n=n+1
        pop=Population(l, self.max_invest, self.vola_wanted, self.rend_wanted, self.date_0)
        #pop.mutation1()
        pop.mutation2()
        i=1
        for portfolio in pop.list_portfolio :
            print("Portfeuille :",i)
            portfolio.score = Fitness.score(portfolio,self.vola_wanted,self.rend_wanted,self.date_0,date_test,connection,mat)
            i=i+1
        return pop
    

    def crossover2(self, date_test, connection, mat):
        '''
        Function that takes as argument the object population
        the test_date in the format (DD/MM/YYYY),
        the connection object which corresponds to the class Sql_connection
        and the asset variation matrix of the Fitness class
        It allows to perform a crossover on the object population, 
        more precisely a crossover between 3/4 of the portfolios of the population according to their score, 
        the other part is replaced by random portfolios.
        
        It calls the mutation function to modify the population just before the return.
        '''
        sort_pop=self.sort_population()
        l=[]
        size_portfolio = len(self.list_portfolio[0].list_assets)
        size_pop=len(self.list_portfolio)
        middle_portfolio = size_portfolio//2
        i=0
        
        while i<(size_pop*3//4+1):
            portfolioo=[]
            if (i%2==0):
                j=0
                while j<middle_portfolio:
                    portfolioo.append(sort_pop.list_portfolio[i].list_assets[j])
                    j=j+1
                while j<size_portfolio:
                    portfolioo.append(sort_pop.list_portfolio[i+1].list_assets[j])
                    j=j+1
            else :
                j=0
                while j<middle_portfolio:
                    portfolioo.append(sort_pop.list_portfolio[i+1].list_assets[j])
                    j=j+1
                while j<size_portfolio:
                    portfolioo.append(sort_pop.list_portfolio[i].list_assets[j])
                    j=j+1
            i=i+1
            p_ortfolio = Portfolio(portfolioo,1)
            l.append(p_ortfolio)   
            
        nb_portfolio_random = size_pop-i
        n=0
        while n<nb_portfolio_random:
            list_asset = Asset.assign_value_assets(Asset.create_assets(connection),date_test,connection)
            portfeuille = Portfolio(list_asset,1)
            portfeuille = portfeuille.create_random_portfolio(self.max_invest)
            #portfeuille.score=Fitness.score(portfeuille,self.vola_wanted,self.rend_wanted,self.date_0,date_test,connection)
            l.append(portfeuille)
            n=n+1
        pop=Population(l, self.max_invest, self.vola_wanted, self.rend_wanted, self.date_0)
        #pop.mutation1()
        pop.mutation2()
        i=1
        for portfolio in pop.list_portfolio :
            print("Portfeuille :",i)
            portfolio.score = Fitness.score(portfolio,self.vola_wanted,self.rend_wanted,self.date_0,date_test,connection,mat)
            i=i+1
        return pop
        
        

    def afficher_population(self):
        '''
        Function that takes the population object as argument and displays a population in the console
        '''
        i=0 
        list_portfolio=self.list_portfolio
        list_asset = self.list_portfolio[0].list_assets
        #print(dict(population))
        while i<len(list_portfolio):
            print("######################################################################")
            print("Portfolio "+str(i+1))
            print("######################################################################")
            j=0
            while j < len(list_asset):
                print(self.list_portfolio[i].list_assets[j].name,",", self.list_portfolio[i].list_assets[j].value,",", self.list_portfolio[i].list_assets[j].nb_shares, ",", self.list_portfolio[i].list_assets[j].percentage)
                j=j+1
            print(self.list_portfolio[i].score)
            i=i+1
        return 0


    def create_population_random(nb_portfolio, max_invest, date_test,vola_wanted, rend_wanted, date_0,connection,mat):
        '''
        Function that takes as an argument the number of portfolios desired in a population in the form of an integer.
        the maximum you want to invest in a portfolio in the form of an integer
        the test date in the form of a string with the format: DD/MM/YYYY
        the volatility and return we wish to have for our portfolio as a whole
        the date_0 in the form of a string with the format: DD/MM/YYYY corresponding to the date on which the ratios are calculated
        the connection object from the Sql_connection class
        and the asset variation matrix of the Fitness class

        this function allows to create a random population according to the above arguments
        it returns the object population

        '''
        list_portfolio=[]
        i=0
        while i<nb_portfolio:
            list_asset = Asset.assign_value_assets(Asset.create_assets(connection), date_test,connection)
            portfeuille = Portfolio(list_asset,1)
            p = portfeuille.create_random_portfolio(max_invest)
            p.score=Fitness.score(p,vola_wanted,rend_wanted,date_0,date_test,connection,mat)
            list_portfolio.append(p)
            i=i+1
            print("create pop :" ,i)
        pop = Population(list_portfolio,max_invest,vola_wanted, rend_wanted, date_0)
        return pop
    
    
    def __repr__(self):
        return "{0}".format(self.list_portfolio) 



if __name__=="__main__":
    
    connection = Sql_connection('PI2','root','DFCOfoot')
    connection.initialisation()
    
    nb_portfolio=5
    max_invest=5000
    date_test="05/07/2019"
    date_0="01/07/2018"
    vola_wanted=15
    rend_wanted=10
    choix="crossover2"
    
    mat = Fitness.matrice_variation(connection, date_0, date_test)
    population_test = Population.create_population_random(nb_portfolio, max_invest, date_test,vola_wanted, rend_wanted, date_0,connection,mat)
    population_test_sort = population_test.sort_population()
    print(population_test_sort)
    population_test_next_generation = population_test_sort.crossover(choix,date_test,connection,mat)
    print(population_test_next_generation)
    #population_test_next_generation.afficher_population()
    
    
    connection.close_connection()