from examples import lorenz_for_scipy
from scipy.integrate import odeint
import matplotlib.pyplot as plt 
import numpy as np
import time


class ftSolver():
    def init(self, a, b, h, ivp, func, n):
        self.a = a
        self.b = b
        self.h = h
        self.ivp = ivp
        self.func = func
        self.n = n
        self.t = np.arange(a, b, h)
    
    def solve(self):
        self.solving_start = time.time()
        sol = odeint(self.func, self.ivp, self.t)
        self.solving_end = time.time()
        self.solving_time = self.solving_end - self.solving_start
        self.y = sol

    def plotxy(self):
        plt.figure(figsize=(12, 6))
        plt.plot(self.y[:,0], self.y[:,2])
        plt.xlabel('x')
        plt.ylabel('y')
        plt.legend()
        plt.show()  


if __name__ == "__main__":
    a = 0
    b = 100
    h = 1e-5
    ivp = [0.0, 1.0, 0.0]

    func = lorenz_for_scipy

    fts = ftSolver()
    fts.init(a=a, b=b, h=h, ivp=ivp, func=func, n=3)
    fts.solve()
    fts.plotxy()
    print(fts.solving_time) # (0,100, 1e-5) -> 0.5901 s




