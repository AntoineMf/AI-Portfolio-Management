# ------------- Genetic Algorithm Class ------------- #
# Libraries
import Asset, Portfolio, Population, Stop_Condition

class Genetic_Algorthm:
    # --- Constructor and Attributes --- #
    def __init__(self, start_population=[], start_date=None, stock_market_index=None, stop_conditions=[]):
        self.start_population = start_population
        self.start_date = start_date
        self.stock_market_index = stock_market_index
        self.stop_conditions = stop_conditions

    # --- Methods --- #
    # Cost Function 1.0: based on ...
    def Cost_Function(self):
        pass
    
    # Mutations and Crossovers
    def Mutate_Population(self):
        pass

    def Crossover_Population(self):
        pass
        
        
