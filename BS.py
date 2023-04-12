class BS:
    def __init__(self, type="permanent"):
        if type == "permanent":
            self.range = 50
            self.elevation = 10
            self.f = 2600
            self.k = 2
            self.TXP = 3
            self.X = 0
            self.Y = 0
        else:
            self.range = 30
            self.elevation = 00
            self.f = 2600
            self.k = 2
            self.TXP = 3
            self.X = 0
            self.Y = 0
