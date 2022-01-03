'''import pymysql.cursors  


class Sql_connection():

    
    def __init__(self, requete):
        self.requete=requete

    def initialisation():
        connection = pymysql.connect(host='localhost',
                            user='root',
                            password='DFCOfoot',
                            db='PI2',
                            cursorclass=pymysql.cursors.DictCursor)
        cursor = connection.cursor()
        return cursor
    
    
    def connection(requete,cursor):
        cursor.execute(requete)
        return cursor
    
    
    def close_connection(cursor):
        return cursor.close()



if __name__=="__main__":
    
    requete ="SELECT * FROM cac"
    conn = Sql_connection.initialisation()
    cursor=Sql_connection.connection(requete,conn)
    
    row=cursor.fetchone()
    for row in cursor:
        print(row)

'''


import pymysql.cursors  


class Sql_connection():

    
    def __init__(self, requete):
        self.requete=requete

    def connection(self):
        connection = pymysql.connect(host='localhost',
                            user='root',
                            password='DFCOfoot',
                            db='PI2',
                            cursorclass=pymysql.cursors.DictCursor)
        cursor = connection.cursor()
        cursor.execute(self.requete)
        return cursor
    
    def close_connection(self,cursor):
        return cursor.close()



if __name__=="__main__":
    
    requete ="SELECT * FROM cac"
    conn = Sql_connection(requete)
    
    cursor = conn.connection()
    row=cursor.fetchone()
    for row in cursor:
        print(row)
 







'''
    This class allows to make the connection between the database (composed of information about the assets) 
    and python.
    
    It needs only one attribute: an SQL query.
    The function connection allows to return the result of the SQL query
    '''
