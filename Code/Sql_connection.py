import mysql.connector


class SqlConnection:

    def __init__(self):
        self.mydb = mysql.connector.connect(
                    host='',
                    user='',
                    password='',
                    database=''
                    )
        self.mycursor = self.mydb.cursor()
    
    def execute(self, requete):
        self.mycursor.execute(requete)
        return self.mycursor.fetchall()
    
    def close_connection(self):
        self.mycursor.close()
        self.mydb.close()
        
    def commit(self):
        self.mydb.commit()

    @staticmethod
    def requete(date1, date2, titre):
        mycursor = SqlConnection()
        x = mycursor.execute("SELECT Stock_Date,Stock_Value FROM PI2.Stock WHERE Equity_Name='"
                             + str(titre)+"' AND  Stock_Date>='" + str(date1)+"' AND Stock_Date<='"
                             + str(date2)+"' ORDER BY Stock_Date ASC;")
        mycursor.close_connection()
        dates = []
        price = []
        for j in x:
            dates.append(j[0])
            price.append(j[1])
        return dates, price
