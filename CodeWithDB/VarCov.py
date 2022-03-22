# ------------- Var_Cov Class ------------- #
# Packages

# Libraries
from Functions import Functions
import numpy as np


class VarCov:
    '''Definition de la matrice de covariance direct par la fonction cov'''
    def __init__(self, returns):
        self.matrix = returns.astype(float).cov()
    
    '''Recuperation de la Variance de chaque assets à partir de la Mat de VARCOV ( donc recupération de la diagonal en faite ) sous forme de tableau'''
    def getVol(self):
        """
        Returns the volatility of each asset
        """
        list_of_var = []
        for i in range(0, len(self.matrixVarCov[0])):
            list_of_var.append((self.matrixVarCov[i][i])**0.5)
        return list_of_var

    '''Renvoie la matrice de VARCOV d'une serie stat "data" sous forme de tableau Numpy
    Ne concerne pas du tout self donc : pourquoi est-ce dans cette classe : la mette dans Functions ???'''
    def Compute_var_cov(self, data):
        data_arr = np.array(data)
        cov_matrix = np.cov(data_arr, rowvar=False)
        return cov_matrix

    '''Surcharge du Print()'''
    def __str__(self):
        return str(self.matrixVarCov)

if __name__ == "__main__":
    vc = VarCov([[1, 2, 3], [2, 3, 4], [4, 5, 6]])
    print(vc)
    print(vc.getVol())