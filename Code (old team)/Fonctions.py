from datetime import datetime


class Fonctions():
    
    
    def moyenne_tab(a):
        size = len(a)
        tot=0
        for i in range(0,size):
            tot = tot+a[i]
        moy = tot/size
        return moy
    
    def moyenne_score(pop):
        size=len(pop.list_portfolio)
        tot=0
        for i in range(0,size):
            tot += pop.list_portfolio[i].score
        moy = tot/size
        return moy
    
    def covariance(a,b):
        if len(a) != len(b): 
            return 0
        a_mean = Fonctions.moyenne_tab(a) 
        b_mean = Fonctions.moyenne_tab(b) 
        summ = 0 
        for i in range(0, len(a)): 
            summ = summ+ ((a[i] - a_mean) * (b[i] - b_mean)) 
        result = summ/(len(a))
        return result 
    
    
    def carre (a):
        return a*a
    
    
    def fonction_tri(tableau):
        for i in range(1,len(tableau)):
            element = tableau[i]
            j = i
            #décalage des éléments du tableau
            while j>0 and tableau[j-1]>element:
                tableau[j]=tableau[j-1]
                j = j-1
            #on insère l'élément à sa place
            tableau[j]=element
        return tableau         
    
    
    def int_to_date(nb):
        date=datetime.fromtimestamp(nb).strftime("%Y-%m-%d")
        return date
    
    def date_to_int(date): #format en str : 01/01/2010
        date=datetime.strptime(date,"%d/%m/%Y")
        nb = int(date.strftime('%s'))+7200
        return nb
    
if __name__=="__main__":    
    b=1530403200
    print(b)
    c=Fonctions.int_to_date(b)
    print(c)
    a=Fonctions.date_to_int("01/07/2018")
    print(a)
    print(Fonctions.int_to_date(a))