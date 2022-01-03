import pymysql.cursors  


class Sql_connection():

    '''
    This class allows to make the connection between the database (composed of information about the assets) 
    and python.
    
    It needs only one attribute: an SQL query.
    The function connection allows to return the result of the SQL query
    '''
    
    def __init__(self, database, user, mdp):
        self.database = database
        self.user = user
        self.mdp = mdp
        self.conn = None
        self.cur = None


    def initialisation(self):
        '''
        Function that takes as argument the connection object and allows to open a connection with the database
        '''
        self.conn = pymysql.connect(host='localhost',
                            user=self.user,
                            password=self.mdp,
                            db=self.database,
                            cursorclass=pymysql.cursors.DictCursor)
        self.cur = self.conn.cursor()
    
    
    def execute(self,requete):
        '''
        Function that takes as argument the object connection and
        a request string that corresponds as its name indicates to the request we want to make on the database

        it returns the cursor to access the result returned by the SQL query
        '''
        self.cur.execute(requete)
        return self.cur
    
    
    def close_connection(self):
        '''
        Function that takes as argument the object connection and allows to close the connection with the database
        '''
        self.cur.close()
        self.conn.close()



if __name__=="__main__":
    
    requete ="SELECT * FROM cac"
    connection = Sql_connection('PI2','root','DFCOfoot')
    connection.initialisation()
    cursor = connection.execute(requete)
    for row in cursor:
        print(row)
    connection.close_connection()
        
    
    
