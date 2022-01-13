# -*- coding: utf-8 -*-
import pandas as pd
import pyodbc
import mysql.connector as MC
import datetime

path = r".\Data_CAC.csv"
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
def whileNan(val,colname,df):
    if df[colname][val]=="nan":
        newval=whileNan(val-1,colname,df)
    return newval

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
            if(str(colname)!='Date'):
                d2=datetime.datetime.strptime(date,'%d/%m/%y').strftime('%Y/%m/%d')
                if(str(df[colname][j])=="nan"):
                    pass
                    #req1 = "INSERT INTO Donnee(Donnee_date,Donnee_Value,Titre_Nom) VALUES('"+str(d2)+"',"+str(valprice)+",'"+str(colname)+"')"
                else:
                    req1 = "INSERT INTO Donnee(Donnee_date,Donnee_Value,Titre_Nom) VALUES('"+str(d2)+"',"+str(df[colname][j])+",'"+str(colname)+"')"

                    print(req1)
                    cursor.execute(req1)
                    j=j+1
                    compteur=compteur +1
                    conn.commit()
                #Titrelist = cursor.fetchall()
                #for titre in Titrelist:
                #    print('Titre : {}'.format(titre[0]))
    
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

