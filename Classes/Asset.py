# ------------- Asset Class ------------- #
# Packages

# Libraries
from Functions import Functions




class Asset:
    # --- Constructor and Attributes --- #
    def __init__(self, name="", price_list=[], weight=0):
        self.name = name
        self.price_list = price_list  # to verify: is it the best way?
        self.weight = weight  # to verify: can they be negative?
        self.returns_list = []

    # --- Methods --- #
    # Description of an Asset
    def Describe_Asset(self):
        return "(" + self.name + "\t Price List: " + str(self.price_list) +  "\t Weight: " + str(self.weight) + ")"


        
    def Compute_returns(self, rolling_window = 1):
        if rolling_window > 0:
            for i in range(len(self.price_list), rolling_window, -1):
                self.returns_list[len(self.price_list) - i] = \
                    (self.price_list[i] / self.price_list[i - rolling_window]) - 1
    """
            for i in range(0, len(self.price_list) - rolling_window):
                self.returns_list[i] = \
                    (self.price_list[i] / self.price_list[i + rolling_window]) - 1
    """

    def Compute_mean_returns(self, size = 0):
        if size == 0 or size > len(self.returns_list):
            size = len(self.returns_list)
        return Functions.Compute_mean(list(self.returns_list[0:size]))

    # Calculation of Volatility and Yield of a given Asset
    def Compute_volatility(self, size = 0):
        if size == 0 or size > len(self.returns_list):
            size = len(self.returns_list)
        return Functions.Compute_standard_deviation(list(self.returns_list[0:size]))
        
        