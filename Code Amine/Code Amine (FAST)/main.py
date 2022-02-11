'''

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
        
'''
# Libs
from numpy import average
import pandas as pd
from time import strftime, gmtime


# Class Packages
from GeneticAlgorithm import Genetic__Algorithm
from Asset import *
from Portfolio import *
from Population import *
        
# --- Methods --- #
def data_preprocessing(path):
    df = pd.read_csv(path, delimiter=";")
    df['Date'] = pd.to_datetime(df['Date'], format='%d/%m/%y')
    df = df.sort_values(df.columns[0], ascending=True)
    return df.iloc[:, 1:]

# Creation de toute les instance de la classe assets 
def get_Asset_List(df, nb_days): 
    df_extracted = df.tail(nb_days).copy()
    # Returns df
    df_returns = (df_extracted / df_extracted.shift(1)).tail(-1) -1
    print(df_returns)
    asset_list = []
    for asset_name in df.columns:
        # Name and Prices
        prices = list(df_extracted.loc[:, asset_name])
        asset = Asset(name=asset_name, prices=prices)
        # Returns 
        asset._returns_list = df_returns.loc[:, asset_name].tolist()
        # Avg Yield and Volatility
        asset._rendement_moy = average(asset._returns_list)
        asset._volatility = math.sqrt(np.cov(asset._returns_list))
        # Add to the asset_list
        asset_list.append(asset)
    return asset_list, df_returns

# Start Population
def generate_Start_Population(asset_list, size=100): # Generation population de depart
        # pop depart = 100 indiv
        alea_list_portfolio = [Portfolio.creation_portfolio_alea(asset_list)  for i in range(size)]
        pop = Population(list_portfolio=alea_list_portfolio)
        return pop




# --- Main --- #
# Get Data from source
df = data_preprocessing(path="Data_CAC.csv")
print(df)

# Get the list of all assets and Generate a start population
asset_list, df_returns = get_Asset_List(df, nb_days=21) # creation des instance de la classe assets
start_pop = generate_Start_Population(asset_list, size=100)

# Sort the best Population by fitness (to compare it to the future candidates)
[portfolio.fitness() for portfolio in start_pop._list_portfolio]
start_pop._list_portfolio.sort(key=lambda portfolio: portfolio._sharp_score, reverse=True)

# Create the genetic algorithm instance
gen_algo = Genetic__Algorithm(nb_gen=10)

#  START OF THE GENETIC LOOPS
print("\nProcessing...")
total_crossover_mutation_cnt, total_duration = 0, 0
for current_gen in range(gen_algo.nb_gen):
    # Display Message
    print("\n" + "-"*45 + "\n" + "\t\tGenration " + str(current_gen))

    # Get the best Individual's Population in the i'th generation and display results
    best_indv_pop, crossover_mutation_cnt, duration = gen_algo.genetic_loop(start_pop, df_returns, mutation_rate=30, max_iter=200)
    print("- Start pop Sharpe (of current gen): " + str(start_pop.get_best_portfolio_fitness()) +
        "\n- Best  pop Sharpe (of current gen): " + str(best_indv_pop.get_best_portfolio_fitness()) +
          "\n--> Gen Duration: " + str(duration) + " seconds")

    # Verify the redundancy (To do)

    # Save best combination as a start combination to unsure at least and equal result in the i+1'th gen (Increment duration)
    start_pop = best_indv_pop
    total_duration += duration 
    crossover_mutation_cnt += crossover_mutation_cnt

# Save Time
ms = int(math.modf(total_duration)[0] *1000)
total_duration = strftime("%M min(s), %S sec(s)", gmtime(int(total_duration))) + ", and " + str(ms) + " ms(s)"

# RESULTS OF THE GENETIC LOOPS
best_portfolio = best_indv_pop._list_portfolio[0]
print("\n" + "-"*45 + 
      "\n- Best Sharpe: " + str(best_portfolio._sharp_score) +
      "\n- Avg Yield: " + str(best_portfolio.rendement_moyen()) +
      "\n- volatility: " + str(best_portfolio._volatility) +
      "\n- Total Crossovers-Mutations: " + str(crossover_mutation_cnt) + "\n"
      "\n--> Best Portfolio content:\n" + str(best_portfolio.Display_Content()) + "\n" +
      "\n--> Genetic Loop took " + str(total_duration) + " for " + str(gen_algo.nb_gen) + " generations")




