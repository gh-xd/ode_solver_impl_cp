import matplotlib.pyplot as plt 
import numpy as np
import time
from examples import lorenz_for_python

class pyODESolver():
    def __init__(self, f_size=np.float64):
        self._INIT_AB = 0
        self._INIT_H = 0
        self._INIT_EQN = 0
        self._INIT_IVP = 0
        self.f_size = f_size

    def init(self, func, n, ivp, a=0e0, b=1e0, h=5e-2):
        self.n = int((b - a) / h)
        self.a = self.f_size(a)
        self.b = self.f_size(b)
        self.h = self.f_size(h)
        self.hs = [self.h] # list of step h (for recording adaptive step)
        self.f = func
        self.m = n

        self.x = np.array([a + i * self.h for i in range(self.n + 1)], dtype=self.f_size)
        self.y = np.zeros([self.n + 1, self.m], dtype=self.f_size)
        self.y[0] = ivp

    def _set_ab(self, a, b):
        self.a = self.f_size(a)
        self.b = self.f_size(b)
        self._INIT_AB = 1
        self._check_and_set_n()

    def _set_h(self, h):
        self.h = self.f_size(h)
        self.hs = [self.h]
        self._INIT_H = 1
        self._check_and_set_n()

    def _set_func(self, func, eq_n):
        self.f = func
        self.m = eq_n      
        self._INIT_EQN = 1  
        self._check_and_set_xy()
    
    def _set_ivp(self, ivp):
        self.ivp = ivp
        self._INIT_IVP = 1 
        self._check_and_set_xy()


    def _check_and_set_n(self):
        if self._INIT_AB * self._INIT_H == 1:
            self.n = int((self.b - self.a) / self.h)
        else:
            pass

    def _check_and_set_xy(self):
        if self._INIT_AB * self._INIT_H * self._INIT_EQN * self._INIT_IVP == 1:
            self.x = np.array([self.a + i * self.h for i in range(self.n + 1)], dtype=self.f_size)
            self.y = np.zeros([self.n + 1, self.m], dtype=self.f_size)
            self.y[0] = self.ivp
        else:
            pass
    
    def solve(self):
        start_t = time.time()

        self.advance()
        
        ent_t = time.time()
        self.solving_time = (ent_t - start_t)

    def advance(self):
        pass

    def plotn(self, row, column, labels):
        t = self.x
        fig, ax = plt.subplots(row, column, figsize=(12,6))

        for i in range(row):
            for j in range(column):
                # ax[i][j].set_title(f"{labels[i * column + j]}")
                ax[i, j].plot(self.x, self.y[:, i * column + j], color=f"C{i * column + j}", label=f"{labels[i * column + j]}")
                ax[i, j].set_xlabel('Time')
                ax[i, j].set_ylabel(f"{labels[i * column + j]}")
                ax[i, j].legend()
        fig.tight_layout()
        plt.show()

    def plot(self, label):
        plt.figure(figsize=(12, 6))

        for i in range(self.m):
            plt.plot(self.x, self.y[:,i], '--', label=label[i])

        plt.xlabel('t')
        plt.ylabel('Multiple')
        plt.legend()
        plt.show()

    def plotxy(self):
        plt.figure(figsize=(12, 6))


        plt.plot(self.y[:,0], self.y[:,1])

        plt.xlabel('x')
        plt.ylabel('y')
        plt.legend()
        plt.show()   


class pySolver(pyODESolver):
    def advance(self):
        _h = self.f_size(1 / 6)

        for i in range(self.n):
            
            x_i = self.x[i]
            y_i = self.y[i, :]

            y1 = y_i
            f1 = y1.copy()
            k1 = self.h * self.f(x_i, y1, f1)

            y2 = y_i + 0.5 * k1
            f2 = y2.copy()
            k2 = self.h * self.f(x_i + 0.5 * self.h, y2, f2)

            y3 = y_i + 0.5 * k2
            f3 = y3.copy()
            k3 = self.h * self.f(x_i + 0.5 * self.h, y3, f3)


            y4 = y_i + k3
            f4 = y4.copy()
            k4 = self.h * self.f(x_i + self.h, y4, f4)

            for j in range(self.m):
                self.y[i, j] = self.y[i, j] + _h * (k1 + 2 * k2 + 2 * k3 + k4)[j]

            self.y[i+1, :] = self.y[i, :]    


if __name__ == '__main__':
    solver = pySolver()
    solver.init(a=0, b=100, ivp=[0.0, 1.0, 0.0], h=1e-5, func=lorenz_for_python, n=3)
    solver.solve()
    # solver.plotxy()
    print(solver.solving_time) # (0,100, 1e-5) -> 169.2646 s