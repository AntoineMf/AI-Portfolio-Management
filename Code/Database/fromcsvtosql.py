# -*- coding: utf-8 -*-
import pandas as pd
import pyodbc
import mysql.connector as MC

path = r".\Stock_Data\Data_CAC.csv"
df = pd.read_csv(path,delimiter=";")
df.head()

"""
conn = pyodbc.connect('Driver={SQL Server};'
                      'Server=localhost:3306;'
                      'Database=Price;'
                      'Trusted_Connection=yes;')
cursor = conn.cursor()
cursor.execute('INSERT INTO Titre("cac")')

""" 
try:
    conn= MC.connect(host='localhost',database='Price',user='root',password="root")
    cursor = conn.cursor()
    compteur=0
    for colname in df.columns:
        j=0
        for date in df["Date"]:
            
            #print(colname)
            #print(date)
            #print(df[colname][j])
            req1 = "INSERT INTO Donnee(Donnee_date,Donnee_Value,Titre_Nom) VALUES('"+str(date)+"',"+str(df[colname][j])+",'"+str(colname)+"')"
            cursor.execute(req1)
            j=j+1
            compteur=compteur +1
            conn.commit()
            Titrelist = cursor.fetchall()
            for titre in Titrelist:
                print('Titre : {}'.format(titre[0]))
    print(compteur)
    #req = 'select * from Titre'
    #req1 = 'INSERT INTO Titre(Titre_Nom) VALUES()'
    #infos=(cursor.lastrowid)
    #infos =(cursor.lastrowid,)
    
    #req1 = "INSERT INTO Donnee(Donnee_date,Donnee_Value,Titre_Nom) VALUES('"+str(date)+"',"+str(df[line].iloc[j])+",'"+str(line)+"')"
    #print(req1)
    
    #cursor.execute(req1)
    """conn.commit()
    Titrelist = cursor.fetchall()
    for titre in Titrelist:
        print('Titre : {}'.format(titre[0]))
    
    j=j+1
    """
except MC.Error as err:
    print(err)
finally:
    
    
    print("ok")
"""
compteur=0
j=0
for colname in df.columns:
    j=0
    for date in df["Date"]:
        print(colname)
        print(date)
        print(df[colname][j])
        req1 = "INSERT INTO Donnee(Donnee_date,Donnee_Value,Titre_Nom) VALUES('"+str(date)+"',"+str(df[colname][j])+",'"+str(colname)+"')"
        j=j+1
        compteur=compteur +1
except MC.Error as err:
    print(err)
finally:
    if(conn.is_connected()):
        cursor.close()
        conn.close()

print(compteur)
  
liste=[]
for date in df['Date']:
    j=0
    for data in df[3:40]:
        print(data)
  for line in df.iterrows():
        test = str(line).split()
        #print(len(test))
        for k in range(len(test)):    
            if(test[k]!=" "):
                liste.append(test[k])
            #print(test)
        j=j+1
print(liste)
        #req1 = "INSERT INTO Donnee(Donnee_date,Donnee_Value,Titre_Nom) VALUES('"+str(date)+"',"+str(df[line].iloc[j])+",'"+str(line)+"')"
        #"INSERT INTO Donnee(Donnee_date,Donnee_Value,Titre_Nom) VALUES('"+str(date)+"',"+str(df[values].iloc[j])+",'"+str(values)+"')"
        #print(req1)
try:
            conn= MC.connect(host='localhost',database='Price',user='root',password="root")
            cursor = conn.cursor()
            req = 'select * from Titre'
            #req1 = 'INSERT INTO Titre(Titre_Nom) VALUES()'
            #infos=(cursor.lastrowid)
            #infos =(cursor.lastrowid,)
            
            req1 = "INSERT INTO Donnee(Donnee_date,Donnee_Value,Titre_Nom) VALUES('"+str(date)+"',"+str(df[line].iloc[j])+",'"+str(line)+"')"
            print(req1)
            
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
        
"""
         
"""           
for line in df.iterrows():
 """
    


"""
Created on Wed Nov 17 20:45:26 2021

@author: maffe


import pandas as pd


path = r"C:\Users\maffe\Downloads\Data_CAC.csv"
df = pd.read_csv(path,delimiter=";")
df.head()

import pyodbc

conn = pyodbc.connect('Driver={SQL Server};'
                      'Server=localhost:3306;'
                      'Database=Price;'
                      'Trusted_Connection=yes;')
cursor = conn.cursor()
cursor.execute('INSERT INTO Titre("cac")')
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
        

         
        
for line in df.iterrows():
    
    """