# ------------- Returns Class ------------- #
# Packages

# Libraries
from Functions import Functions


class Returns:
    __instance = None

    def __init__(self, data):


    def Get_instance(data):
        if Returns.__instance is None:
            Returns.__instance = Returns(data)
        return Returns.__instance
