# ------------- Returns Class ------------- #
# Packages

# Libraries
from Functions import Functions
import Singleton


#class Returns(metaclass=Singleton):
class Returns:
    def __init__(self, data, rolling_window, max_number=0):
        if max_number==0:
            max_number = len(data[0]) - rolling_window
        self.matrixReturns = [[0 for i in range(0, len(data)) for i in range(0, len(data[0]) - rolling_window)]]
        for j in range(0, len(data[0])):
            for i in range(0, len(data) - rolling_window):
                if i > max_number:
                    break
                self.matrixReturns[i].append((data[i][j] / data[i + rolling_window][j]) - 1)

    def getReturnsAsset(self, asset):
        list_of_returns = []
        # TODO  index = asset.index (A reflechir: attribut index d un asset pour les matrices de returns et varCov)
        for i in range(0, len(self.matrixReturns)):
            list_of_returns[i] = self.matrixReturns[i][asset]
        return list_of_returns

if __name__ == "__main__":
    data = [1, 1.1, 1.1, 1.2, 0.9, 2]
    ret = Returns(data, 1, )
    pass