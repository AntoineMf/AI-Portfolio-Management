# ------------- Var_Cov Class ------------- #
# Packages

# Libraries
from Functions import Functions
import Singleton


class VarCov(metaclass=Singleton):
    def __init__(self, returns):
        self.matrixVarCov = Functions.Compute_var_cov(returns)

    def getVol(self):
        """
        Returns the volatility of each asset
        """
        list_of_var = []
        for i in range(0, len(self.matrixVarCov[0])):
            list_of_var[i] = (self.matrixVarCov[i][i])**0.5
        return list_of_var
