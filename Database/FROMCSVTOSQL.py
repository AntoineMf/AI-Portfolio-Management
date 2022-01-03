# -*- coding: utf-8 -*-
"""
Created on Wed Nov 17 20:45:26 2021

@author: maffe
"""

import pandas as pd


path = "Data_CAC.csv"
df = pd.read_csv(path,delimiter=";")
df.head()

"""import pyodbc

conn = pyodbc.connect('Driver={SQL Server};'
                      'Server=localhost:3306;'
                      'Database=Price;'
                      'Trusted_Connection=yes;')
cursor = conn.cursor()
cursor.execute('INSERT INTO Titre("cac")')"""
import mysql.connector as MC

for date in df['Date']:
    j=0
    for values in df.columns:
        
       
        try:
            conn= MC.connect(host='localhost',database='Price',user='root',password="root")
            cursor = conn.cursor()
            req = 'select * from Titre'
            #req1 = 'INSERT INTO Titre(Titre_Nom) VALUES()'
            #infos=(cursor.lastrowid)
            #infos =(cursor.lastrowid,)
        
            req1 = "INSERT INTO Donnee(Donnee_date,Donnee_Value,Titre_Nom) VALUES('"+str(date)+"',"+str(df[values].iloc[j])+",'"+str(values)+"')"
            
            cursor.execute(req1)
            conn.commit()
            Titrelist = cursor.fetchall()
            for titre in Titrelist:
                print('Titre : {}'.format(titre[0]))
            
            j=j+1
            
        except MC.Error as err:
            print(err)
        finally:
            if(conn.is_connected()):
                cursor.close()
                conn.close()
        

         
        

    