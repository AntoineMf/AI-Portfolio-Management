# ------------- Var_Cov Class ------------- #
# Packages

# Libraries
from Functions import Functions
import Singleton
import numpy as np


#class VarCov(metaclass=Singleton):
class VarCov():
    def __init__(self, returns):
        self.matrixVarCov = self.Compute_var_cov(returns)

    def getVol(self):
        """
        Returns the volatility of each asset
        """
        list_of_var = []
        for i in range(0, len(self.matrixVarCov[0])):
            list_of_var.append((self.matrixVarCov[i][i])**0.5)
        return list_of_var


    def Compute_var_cov(self, data):
        data_arr = np.array(data)
        cov_matrix = np.cov(data_arr, rowvar=False)
        return cov_matrix


    def __str__(self):
        return str(self.matrixVarCov)

if __name__ == "__main__":
    vc = VarCov([[1, 2, 3], [2, 3, 4], [4, 5, 6]])
    print(vc)
    print(vc.getVol())