import mysql.connector

class Sql_connection():  

    def __init__(self):
        self.mydb = mysql.connector.connect(
                    host='192.168.196.59',
                    user='pi2',
                    password='pi2',
                    database='PI2'
                    )
        self.mycursor = self.mydb.cursor()
    
    def execute(self,requete):
        self.mycursor.execute(requete)
        return self.mycursor.fetchall()
    
    def close_connection(self):
        self.mycursor.close()
        self.mydb.close()
        
    def commit(self):
        self.mydb.commit()

    def requete(date1,date2,titre):
        mycursor=Sql_connection()
        x=mycursor.execute("SELECT Stock_Date,Stock_Value FROM PI2.Stock WHERE Equity_Name='"+str(titre)+"' AND  Stock_Date>='"+str(date1)+"' AND Stock_Date<='"+str(date2)+"' ORDER BY Stock_Date ASC;")
        mycursor.close_connection()
        dates=[]
        price=[]
        for j in x:
            dates.append(j[0])
            price.append(j[1])
        return dates,price