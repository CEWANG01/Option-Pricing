import math
class Stock_binary_tree:
    def __init__(self, r, sigma, T, S0, K, Nstep):
        self.Nstep = Nstep
        self.paths = []
        for i in range(Nstep):
            new_layer = [0] * (i + 1)
            self.paths.append(new_layer)
        self.r = r
        self.sigma = sigma
        self.T = T
        self.S0 = S0
        self.K = K
        self.delta_t = T/Nstep
        self.u = math.exp(sigma * math.sqrt(self.delta_t))
        self.d = math.exp(-sigma * math.sqrt(self.delta_t))
        self.p = (math.exp(r * self.delta_t) - self.d) / (self.u - self.d)

    def generate(self):
        self.paths[0][0] = self.S0
        for i in range(1, self.Nstep):
            for j in range(0, i):
                new_price = self.paths[i-1][j] * self.u
                self.paths[i][j] = new_price
            new_price = self.paths[i-1][-1] * self.d
            self.paths[i][-1] = new_price
                 
                
        
            
