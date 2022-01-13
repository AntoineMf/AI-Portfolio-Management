import pandas as pd
import pyodbc
import mysql.connector as MC

path = "../Stock_Data/Data_CAC.csv"
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
    
    for i in df.columns:

        req = "INSERT INTO Titre(Titre_nom) VALUES('"+i+"')"
        
        cursor.execute(req)
        
        compteur=compteur +1
        conn.commit()
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