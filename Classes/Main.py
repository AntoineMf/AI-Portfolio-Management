# ------------- Main to test the different classes ------------- #
"""
    Remarks:





"""
# Packages
from Genetic_Algorithm import *
from Database import *
from Stop_Condition import *

from Asset import *
from Portfolio import *
from Population import *

# Libraries
import datetime as dt


# Main
a1, a2 = Asset("BNP action", price_list=[52, 44, 3], weight=0.11), Asset("Amazon action", price_list=[100, 3500], weight=0.57)
p1 = Portfolio(asset_list=[a1, a2])
p1.Display_Portfolio()

db = Database(name="database_00", ids=[])
db.Connect()

p2 = Portfolio()
p2.Generate_Random(available_assets=db.Import_Assets(), n_assets=5)


# Create the model
stop = [Stop_Condition.MAX_ITER, Stop_Condition.MIN_YIELD]
gen_algo = Genetic_Algorthm(start_population=Population([p1, p2]), start_date=dt.datetime(2000, 12, 12), stock_market_index="x", stop_conditions=stop)
gen_algo.Mutate_Population()


