# -*- coding: utf-8 -*-
"""
Created on Fri Jan  7 23:02:45 2022

@author: alan7
"""

import mysql.connector

class Sql_connection():  

    def __init__(self):
        self.mydb = mysql.connector.connect(
                    host='localhost',
                    user='root',
                    password='root',
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
        
my_connection=Sql_connection()
my_response=my_connection.execute("SELECT * FROM price;")[0]
my_connection.close_connection()

for i in my_response:
    print(i)