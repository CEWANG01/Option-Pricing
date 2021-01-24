import math, stock
class AmPut:
    def __init__(self, r, sigma, T, S0, K, Nstep):
        self.r = r
        self.sigma = sigma
        self.T = T
        self.S0 = S0
        self.K = K
        self.Nstep = Nstep
        self.pathtree = []
        self.optiontree = []
        self.delta_t = T/Nstep
        self.u = math.exp(sigma * math.sqrt(self.delta_t))
        self.d = math.exp(-sigma * math.sqrt(self.delta_t))
        self.p = (math.exp(r * self.delta_t) - self.d) / (self.u - self.d)
        self.discount = math.exp(-r * self.delta_t)
        self.stock_tree = stock.Stock_binary_tree(self.r, self.sigma, self.T, self.S0, self.K, self.Nstep)
        self.option_tree = stock.Stock_binary_tree(self.r, self.sigma, self.T, self.S0, self.K, self.Nstep)
        

    def generate(self):
        self.stock_tree.generate()
        self.option_tree.generate()

    def evaluate_layer(self, layer):#if Nstep = 4 then layer = 0 1 2 3
        if layer == len(self.option_tree.paths) - 1:
            for i in range(0, layer + 1):
                self.option_tree.paths[layer][i] = max(0, self.K - self.option_tree.paths[layer][i])
        else:
            for i in range(0, layer + 1):
                holding_before_discount = self.p * self.option_tree.paths[layer + 1][i] + (1 - self.p) * self.option_tree.paths[layer + 1][i + 1]
                holding_after_discount = holding_before_discount * self.discount
                exercising = max(0, self.K - self.option_tree.paths[layer][i])
                self.option_tree.paths[layer][i] = max(holding_after_discount, exercising)


    def evaluate(self):
        for i in range(self.Nstep):
            self.evaluate_layer(self.Nstep - i - 1)

    def get_price(self):
        self.generate()
        self.evaluate()
        return self.option_tree.paths[0][0]
            
            


    


    



    
