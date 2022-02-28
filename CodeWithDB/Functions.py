import numpy as np


class Functions:
    ''' Boite à outils pour les calculs récurents de l'algorithme'''

    def Compute_mean(list):
        mean = 0
        for i in range(0, len(list)):
            mean += list[i]
        mean /= len(list)
        return mean

    def Compute_standard_deviation(list):
        mean = Functions.Compute_mean(list)
        var = 0
        for i in range(0, len(list)):
            var += pow(list[i] - mean, 2)
        var /= len(list)
        std = pow(var, 1/2)
        return std



if __name__ == "__main__":
    list = [1, 2, 3, 4]
    print(Functions.Compute_mean(list))
    print(Functions.Compute_standard_deviation(list))
