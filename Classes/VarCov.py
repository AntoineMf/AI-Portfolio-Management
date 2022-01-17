# ------------- Var_Cov Class ------------- #
# Packages

# Libraries
from Functions import Functions
import Singleton


class VarCov(metaclass= Singleton):
    def __init__(self, returns):
        self.mat = [[]]

