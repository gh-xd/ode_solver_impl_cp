from ctypes import *
from examples import lorenz_for_c
import numpy as np
import time
import matplotlib.pyplot as plt


class pywcSolver():
    def __init__(self, libname="./c_solver.so"):
        self.lib = cdll.LoadLibrary(libname)
        self.solver = self.lib.Solver
        self.solver.restype = POINTER(POINTER(c_double))

    def init(self, a, b, h, ivp, n, func):
        self.a = c_double(a)
        self.b = c_double(b)
        self.h = c_double(h)
        self.steps = int((b-a)/h+1e-6)
        c_ivp = c_double * n
        py_ivp = tuple(ivp)
        self.ivp = c_ivp(*py_ivp)
        self.n = c_int32(n)
        self._n = n
        c_func_py = CFUNCTYPE(None, c_double, POINTER(c_double), POINTER(c_double))
        self.func = c_func_py(func)

    def solve(self):
        self.solving_start = time.time()
        res_c = self.solver(self.a, self.b, self.h, self.ivp, self.n, self.func)
        res_np = np.zeros((self.steps, self._n), dtype=np.float64)
        self.solving_end = time.time()
        self.solving_time = self.solving_end - self.solving_start
        for i in range(self.steps):
            for j in range(self._n):
                res_np[i, j] = res_c[i][j]

        self.y = res_np

    def plotxy(self):
        plt.figure(figsize=(12, 6))

        plt.plot(self.y[:,0], self.y[:,1])

        plt.xlabel('x')
        plt.ylabel('y')
        plt.legend()
        plt.show()   



if __name__ == '__main__':
    run_start = time.time()
    sol = pywcSolver(libname="./c_solver.so")
    py_func = lorenz_for_c
    sol.init(a=0, b=100, ivp=[0.0, 1.0, 0.0], h=1e-5, func=py_func, n=3)
    sol.solve()
    run_end = time.time()
    sol.plotxy()
    print(f"Python Runtime: {run_end - run_start: .4f}")
    print(f"Equation Solving Time (.so + Python callback): {sol.solving_time:.4f}") # 21.3909 s