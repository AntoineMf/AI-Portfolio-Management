# ------------- Asset Class ------------- #
# Packages

# Libraries





class Asset:
    # --- Constructor and Attributes --- #
    def __init__(self, name="", price_list=[], weight=0):
        self.name = name
        self.price_list = price_list  # to verify: is it the best way?
        self.weight = weight  # to verify: can they be negative?

    # --- Methods --- #
    # Description of an Asset
    def Describe_Asset(self):
        return "(" + self.name + "\t Price List: " + str(self.price_list) +  "\t Weight: " + str(self.weight) + ")"

    # Calculation of Volatility and Yield of a given Asset
    def Calculate_Volatility(): 
        pass
        
    def Calculate_Yield(): 
        pass
        
        