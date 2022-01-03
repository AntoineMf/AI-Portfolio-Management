from Sql_connection2 import Sql_connection
from Fonctions import Fonctions
import re


class Asset():
        
    '''
    This class allows you to create an object asset, it is composed of its name, its price, 
    the number of shares purchased of this asset and the weight it represents in the portfolio in percentage.

    The create_asset function allows you to create as many assets as there are different actions 
    in the database and they are stock in a list.
    The assign_value_asset function allows to assign to each asset its value at a date t
    '''
    
    def __init__(self, name, value, nb_shares, percentage):
        self.name=name
        self.value=value
        self.nb_shares=nb_shares
        self.percentage=percentage


    def create_assets(connection):
        '''
        Function that takes as argument the connection object of the Sql_connection class and 
        returns a list of Asset objects with as information only the name of each asset
        '''
        list_asset=[]
        requete ="SELECT Column_Name FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = 'cac'"
        cursor = connection.execute(requete)
        row=cursor.fetchone()
        for row in cursor:
            if (row['COLUMN_NAME']!='Date'):
                action=Asset(row['COLUMN_NAME'], 0, 0, 0)
                list_asset.append(action)
        return list_asset


    def assign_value_assets(list_asset, date_test, connection):
        '''
        Function that takes as argument a list of object asset (empty except for the names of the assets) 
        the date_test in string with the format DD/MM/YYYYYY corresponding to the date on which the program is launched.
        and the connection object of the class Sql_connection

        the function returns the list of object assets having filled the value of each asset at the test_date.
        '''
        size = len(list_asset)  
        i=0
        date_test = Fonctions.date_to_int(date_test)
        while i<size:
            requete="SELECT "+"`"+str(list_asset[i].name)+"`"+" FROM cac where Date="+str(date_test)+";"
            cursor = connection.execute(requete)
            row=cursor.fetchone()
            value_shares = re.sub('\,+', '.', row[list_asset[i].name])
            list_asset[i].value=float(value_shares)
            i=i+1
        return list_asset
    
    
    def __repr__(self):
        return "Name : {0}, Value : {1}, Nb_shares : {2}, Percentage : {3}\n".format(self.name,self.value, self.nb_shares, self.percentage) 
    
    
    
if __name__=="__main__":
    
    connection = Sql_connection('PI2','root','DFCOfoot')
    connection.initialisation()

    date_test="24/07/2013"
    list_asset = Asset.create_assets(connection)
    list_asset_with_value = Asset.assign_value_assets(list_asset,date_test,connection)
    for Asset in list_asset_with_value:
        print(Asset)
    
    connection.close_connection()