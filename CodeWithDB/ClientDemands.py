class ClientDemands:
    def __init__(self, amount, ret=0, vol=0):
        self.amount = amount
        self.ret = ret
        self.vol = vol
        if vol != 0:
            self.sharpe = ret/vol
