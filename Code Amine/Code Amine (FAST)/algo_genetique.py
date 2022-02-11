# --------- IA: Approximation de fonction par Algorithme genetique --------- #
# Libraries
from math import pow, cos, pi
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import random as rd
import time

# Work
# --- Methods --- #
def is_Valid_Combination(combinaison):
    a, b, c = combinaison
    return (a > 0 and a < 1) and (b >= 1 and b <= 20) and (c >= 1 and c <= 20)

# Get the real values
def get_real_ts(nom_fichier):
    f = pd.read_csv(nom_fichier, sep=";")
    temperatures_dict = dict(zip(list(f[f.columns[0]]), list(f[f.columns[1]]))).items()
    return dict(sorted(temperatures_dict))

# Weierstrass Fuction (a € ]0,1[, b € [1,20], c € [1,20])
def t(i, combinaison):
    weierstrass_val = 0
    a, b, c = combinaison
    for n in range(c+1):
        weierstrass_val += pow(a, n) * cos( pow(b, n) * pi * i)
    return weierstrass_val

# Display Weierstrass Function (from a to b passing by 20 points)
def display_Weierstrass(combinaison, temperatures_dict):
    observations, real_ts = list(temperatures_dict.keys()), list(temperatures_dict.values())
    fitness = fitness_function(combinaison, temperatures_dict)

    # Display in an interval
    weierstrass_ts = []
    xs = np.linspace(0, 5, 500)
    for i in xs:
        weierstrass_ts.append(t(i, combinaison))
    plt.plot(xs, weierstrass_ts, "b", label="Weierstrass estimations")
    plt.plot(observations, real_ts, "xr", label="Real observations")
    plt.legend()
    plt.xlabel("time (secs)")
    plt.ylabel("t(i) in °")
    plt.grid()
    plt.show()

    # Superposition of the real temperatures and the Weierstrass values
    weierstrass_ts = []
    for i in observations:
        weierstrass_ts.append(t(i, combinaison))
    plt.plot(observations, weierstrass_ts, "b", label="Weierstrass estimations")
    plt.plot(observations, real_ts, "xr", label="Real observations")
    plt.legend()
    plt.title("Best combinaison: " + str(combinaison) + " with a cost function: " + str(round(fitness, 5)))
    plt.xlabel("time (secs)")
    plt.ylabel("t(i) in °")
    plt.grid()
    plt.show()
    
# Cost/Fitness Function (for a Combination) knowing the real temperatures: should be minimized
def fitness_function(combinaison, temperatures_dict):
    observations, real_ts = list(temperatures_dict.keys()), list(temperatures_dict.values())
    score_errors = 0
    for i in range(len(observations)):
        j = observations[i]
        score_errors += abs(real_ts[i] - t(j, combinaison))
        #score_errors += pow(abs(real_ts[i] - t(j, combinaison)), 2) / len(observations)
    return score_errors

# Mutation et croisement
def mutation_Individu_Combinaison(combinaison, redundancy):
    a, b, c = combinaison
    if not redundancy[0]: a = round(rd.uniform(0.001, 0.999), 3)
    if not redundancy[0]: b = rd.randint(1, 20)
    if not redundancy[1]: c = rd.randint(1, 20)
    return (a, b, c)

"""
def Croisement_Individus_Combinaisons(combinaison_1, combinaison_2):
    a1, b1, c1 = combinaison_1
    a2, b2, c2 = combinaison_1
    return (a1, c1, b2)
"""

# Faire plusieurs Muation jusqu'a atteindre un minimum local (voir global)
def find_Best_Combination(start_combination, nbr_iterations, temperatures_dict, redundancy):
    # Initialize a combination (Individu)
    meilleur_Individu = start_combination

    # Iterate to find a better combination
    iterations = 0
    cnt_mutations = 0
    while iterations < nbr_iterations:
        # Try a mutation, check if its valid and compare its fitness to the current best fitness
        a, b, c = mutation_Individu_Combinaison(meilleur_Individu, redundancy)
        if redundancy[0]:
            a = round(rd.uniform(meilleur_Individu[0]-0.1, meilleur_Individu[0]+0.1), 3)
        new_combination = (a, b, c)
        if is_Valid_Combination(new_combination):
            cnt_mutations += 1
            if fitness_function(new_combination, temperatures_dict) < fitness_function(meilleur_Individu, temperatures_dict):
                meilleur_Individu = new_combination
                iterations = 0
            else:
                # On avance en nbr d'iteration (si le meilleure individu est le meme apres x itération, on a atteint un minimum local voir global)
                iterations += 1
        else:
            break
    return meilleur_Individu, cnt_mutations

# Update the algorithm until it finds the best (a, b, c)
"""
def find_Best_Combination_Bis(nbr_iterations, temperatures_dict):
    # Initialize a combination
    individu_combinaison = (0.01, 1, 1)
    meilleur_Individu = individu_combinaison
    a, b, c = meilleur_Individu

    # Check the combinations ((0 if a), (1 if b) and (2 if c))
    i = 0
    while i < 3:

        # Try mutations of a, b or c and compare
        iterations = 0
        while iterations < nbr_iterations:
            if i == 0:
                a = round(a+0.05, 2)
            elif i == 1:
                b += 1
            elif i == 2:
                c += 1

            # Set the new combination and compare its fitness to the current best fitness
            new_combination = (a, b, c)
            if is_Valid_Combination(new_combination):
                if fitness_function(new_combination, temperatures_dict) < fitness_function(meilleur_Individu, temperatures_dict):
                    meilleur_Individu = new_combination
                    iterations = 0
                else:
                    # On avance en nbr d'iteration (si le meilleure individu est le meme apres x itération, on a atteint un minimum local voir global)
                    iterations += 1
            else:
                break
        i += 1
        a, b, c = meilleur_Individu
    return meilleur_Individu
"""

def redundancy_counter(start_combination, best_combination, a_counter, b_counter, c_counter):
    if abs(start_combination[0] - best_combination[0]) < 00.1:
        a_counter += 1
    else:
        a_counter = 0
    if start_combination[1] == best_combination[1]:
        b_counter += 1
    else:
        b_counter = 0
    if start_combination[2] == best_combination[2]:
        c_counter += 1
    else:
        c_counter = 0
    return a_counter, b_counter, c_counter

# Save the best recorded combination in a txt file
def save_recorded_combination(nom_fichier, combination):
    f = open(nom_fichier, 'w')
    a, b, c = combination
    f.write(str(a) + ";" + str(b) + ";" + str(c))
    f.close()



# --- Main --- #
# Get the real temperatures (open the whole folder in order to read the csv without writing the hole path)
temperatures_dict = get_real_ts("temperature_sample.csv")

# Run the A.I
# Initialize the parameters
max_iterations = 600
nb_executions = 9
start_combination = (0.1, 10, 15)

# redundancy
a_counter = b_counter = c_counter = 0
max_redundancy_a, max_redundancy_b, max_redundancy_c  = 3, 3, 8  # This means a redundancy of b or c after 3 executions of 2000 ≈ 6000 iterations to find the best combination
redundancy = [False, False, False]
total_mutations = 0

# Process
print("Processing...")
start_time = time.time()
for i in range(nb_executions):
    # Get the best combination in the i'th execution
    best_combination, cnt_mutations = find_Best_Combination(start_combination, max_iterations, temperatures_dict, redundancy)
    total_mutations += cnt_mutations

    # Verify the redundancy of a, b and c and adapt the mutation
    a_counter, b_counter, c_counter = redundancy_counter(start_combination, best_combination, a_counter, b_counter, c_counter)
    redundancy[0] = a_counter >= max_redundancy_a  # a is redundent
    redundancy[1] = b_counter >= max_redundancy_b  # b is redundent
    redundancy[2] = c_counter >= max_redundancy_c  # c is redundent

    # Save best combination as a start combination to unsure at least and equal if not a best result in the i+1'th execution
    start_combination = best_combination
delay = round((time.time() - start_time), 3)

# Save the best combination (0.141;19;2) and display few results
save_recorded_combination("moussa_amine.txt", best_combination)
best_fitness = fitness_function(best_combination, temperatures_dict)
rounded_error = best_fitness / len(list(temperatures_dict.keys()))
print("- Best combinaison: " + str(best_combination) 
  + "\n- Cost function: " + str(round(best_fitness, 5)) + " (Avg error between real values and estimations: ±" + str(round(rounded_error, 5)) + ")"
  + "\n- Processing time: " + str(delay) + " seconds" 
  + "\n- Total Mutations: " + str(total_mutations) + " mutations")
display_Weierstrass(best_combination, temperatures_dict)



i = 1.017
print(t(i, best_combination))


