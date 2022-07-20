# ------------- Var_Cov Class ------------- #


class VarCov:
    """
    Definition de la matrice de covariance direct par la fonction cov
    """
    def __init__(self, returns):
        self.matrix = returns.astype(float).cov()
