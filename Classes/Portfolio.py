# ------------- Portfolio Class ------------- #
# Libraries
import random as rd


class Portfolio:
    # --- Constructor and Attributes --- #
    def __init__(self, asset_list=[], max_investement=0, score=0):
        self.asset_list = asset_list
        self.max_investement = max_investement
        self.score = score

    # --- Methods --- #
    # Generate a random porftolio with random assets from the available assets of the database
    def Generate_Random(self, available_assets, n_assets):
        self.asset_list = rd.sample(available_assets, n_assets)  # if its random, should we choose the num of assets?
        self.max_investement = rd.uniform(0, 1000)   # how can a random score be generated
        self.score = rd.uniform(0, 1000)  # how can a random score be generated
    
    # Display the assets of the portfolio and other attributes
    def Display_Portfolio(self): 
        asset_list_display = ""
        for asset in self.asset_list:
            asset_list_display += "\t" + asset.Describe_Asset() + "\n"
        print("-" * 75 + "\nPortfolio Content:\n" +
              "\n- Max Investement: " + str(self.max_investement) +
              "\n- Score: " + str(self.score) +
              "\n- Asset List:\n" + str(asset_list_display) + 
              "-" * 75)

    # Calculate the score of a Portofilio based on..
    def Calculate_Score():
        pass  # based on asset list?
        
        