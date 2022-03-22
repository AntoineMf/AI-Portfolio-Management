# ------------- Asset Class ------------- #
# Packages

# Libraries
from Functions import Functions
import random
import math

class Asset:
    
    # --- Constructor and Attributes --- #
    def __init__(self, name, values, dates):
        self.name = name
        self.values = values
        self.dates = dates

        # --- Methods --- #
    # Description of an Asset