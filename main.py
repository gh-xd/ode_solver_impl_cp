from py_solver import pySolver
from scipy_fortran_solver import ftSolver
from py_with_c_solver import pywcSolver
from py_in_c_solver import pycSolver
from examples import *
import time
import matplotlib.pyplot as plt


a = 0
b = 1
h = 1e-5
ivp = [0.0, 1.0, 0.0]

solvers = [
    ("Pure Python", pySolver, lorenz_for_python),
    ("C Lib + Python Callback", pywcSolver, lorenz_for_c),
    ("C Lib by Python", pycSolver, lorenz_string),
    ("Scipy in Python (Fortran)", ftSolver, lorenz_for_scipy)]

rts = []
sts = []

for solution, solver, func in solvers:
    sol_start = time.time()
    sol = solver()
    sol.init(a=a, b=b, ivp=ivp, h=h, func=func, n=3)
    sol.solve()
    sol_end = time.time()

    rt = sol_end-sol_start
    st = sol.solving_time
    rts.append(rt)
    sts.append(st)
    print(f">> [{solution}]")
    print(f"  - Runtime: {rt:.4f} s")
    print(f"  - Solver Time: {st:.4f} s")
