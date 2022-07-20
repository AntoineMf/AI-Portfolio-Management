# ------------- Returns Class ------------- #
# Packages

# Libraries
import pandas as pd


class Returns:
    """
    Set up des returns via les données de la BDD et des parametre rentré en MAIN
    Double boucle For pour la matrice des returns et set up des Names pour les noms des columns.
    """
    def __init__(self, values, rolling_window, names, max_number=0):
        # Periode sur laquelle on calcule les returns
        self.rolling_window = rolling_window
        self.max_number = max_number
        # Definit une taille max pour la matrice si elle n'est pas deja definie
        if max_number == 0:
            self.max_number = len(values) - rolling_window
        # Initialisation de la matrice de returns (vide)
        self.matrixReturns = pd.DataFrame(data=None, index=range(0, self.max_number), columns=names)
        # Remplissage de la matrice
        for j in range(0, len(values.iloc[0])):
            for i in range(0, max_number):
                # Formules des returns
                self.matrixReturns.iloc[i, j] = ((values.iloc[i, j] / values.iloc[i + rolling_window, j]) - 1)

    def __str__(self):
        """
        Permet d'afficher la matrice des returns quand on affiche l'objet
        """
        return str(self.matrixReturns)
