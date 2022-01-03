

# ------------- Stop Conditions Enumeration ------------- #
# Libraries
from enum import Enum


# Enumeration
class Stop_Condition(Enum):
        MAX_ITER = 1000
        MAX_VOLATILITY = 1000
        MIN_YIELD = 1000