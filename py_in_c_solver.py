import os
import time
import uuid
from odesf import eq_to_cfunc_string
import random
from ctypes import *
import numpy as np
from examples import lorenz_string

class pycSolver():
    def __init__(self, templ_file="/c_solver.templ"):
        self.absdir = os.path.dirname(__file__)
        self.cpp_file = "/temp_file"
        self.h_file = self.absdir + self.cpp_file + ".h"
        self.func_file = self.absdir + self.cpp_file + ".cpp"
        self.templ_file = self.absdir + templ_file
        self.c_file = ""
        self._cpp = self.absdir + self.cpp_file + "_pycsolver.cpp"
        self.start = time.time()
        self.templib = "_temp.so"
        self.templib_file = self.absdir + "/" + self.templib


    def init(self, a, b, h, ivp, func, n):
        self.a = a
        self.b = b
        self.h = h
        self.steps = int((b-a)/h+1e-6)
        self.ivp = tuple(ivp)
        self.n = n
        self.func_str = func()[0]
        self.func_const = func()[1]
        self.__transform()


    def __transform(self):
        self.fs, self.hs = eq_to_cfunc_string(equations=self.func_str, constants=self.func_const)     
        self.fs = f"#include<{self.h_file}>\n" + self.fs

    def __replace(self):
        with open(self.templ_file, 'r', encoding="utf-8") as f:
            for line in f:
                if "__funch__" in line:
                    line = line.replace("__funch__", self.h_file)
                if "__a__" in line:
                    line = line.replace("__a__", f"{self.a}")
                if "__b__" in line:
                    line = line.replace("__b__", f"{self.b}")
                if "__ht__" in line:
                    line = line.replace("__ht__", f"{self.h}")
                if "__n__" in line:
                    line = line.replace("__n__", f"{self.n}")
                if "__ivp__" in line:
                    line = line.replace("__ivp__", ", ".join([str(i) for i in self.ivp]))
                self.c_file += line
        f.close()


    def __generate(self):
        with open(self.h_file, 'a') as f:
            f.write(self.hs)
        f.close()

        with open(self.func_file, 'a') as f:
            f.write(self.fs)
        f.close()

        with open(self._cpp, 'w', encoding="utf-8") as f:
            f.write(self.c_file)
        f.close()

        cm = f'#! /bin/sh\necho "Start compiling..."; g++ {self._cpp} {self.func_file} -I. -std=c++17 -o {self.templib};'
        ex = f"#! /bin/sh\n./{self.templib};"

        self.t_cmfile = f"__{str(uuid.uuid1()) + str(random.randint(0,11)) + str(uuid.uuid4())}__.sh"
        with open(self.t_cmfile, 'a') as f:
            f.write(cm)
        f.close()


    def __delete(self):
        if os.path.exists(self.cmfilepath):
            os.remove(self.cmfilepath)
        else:
            print(f"NOT FOUND: {self.cmfilepath}")

        if os.path.exists(self.h_file):
            os.remove(self.h_file)
        else:
            print(f"NOT FOUND: {self.h_file}")

        if os.path.exists(self.func_file):
            os.remove(self.func_file)
        else:
            print(f"NOT FOUND: {self.func_file}")

        if os.path.exists(self._cpp):
            os.remove(self._cpp)
        else:
            print(f"NOT FOUND: {self._cpp}")

        if os.path.exists(self.templib_file):
            os.remove(self.templib_file)
        else:
            print(f"NOT FOUND: {self.templib_file}")


    def solve(self):
        self.__replace()
        self.__generate()

        self.cmfilepath = self.absdir + "/" + self.t_cmfile
        try:
            per = os.popen('chmod 777 ' + self.cmfilepath)
            per.read()
            data = os.popen(self.cmfilepath)
            print(data.read())


            # data = os.popen(self.exfilepath)

            libfile = cdll.LoadLibrary("./" + self.templib)
            resf = libfile.getResult
            resf.restype = POINTER(POINTER(c_double))

            self.solving_start = time.time()
            print("Start solving...")
            res_c = resf()
            self.solving_end = time.time()
            res_np = np.zeros((self.steps, self.n), dtype=np.float64)

            self.y = res_np
            

        except:
            print("no data")

        print("Start post-processing...")
        self.__delete()
        for i in range(self.steps):
            for j in range(self.n):
                res_np[i,j] = res_c[i][j]

        self.end = time.time()
        self.python_runtime = self.end - self.start
        self.solving_time = self.solving_end - self.solving_start


if __name__ == '__main__':
    lorenz_str_func = ['dx/dt = sigma * (y - x)', 'dy/dt = rho * x - y - x * z', 'dz/dt = x * y - beta * z']
    lorenz_str_const = ['sigma = 10e0', 'rho = 28e0', 'beta = 8e0 / 3e0']
    a = 0e0
    b = 100e0
    h = 1e-5
    n = 3
    ivp = (1e0, 1e0, 1e0)

    sol = pycSolver()
    sol.init(a=a, b=b, h=h, n=n, ivp=ivp, func=lorenz_string)
    sol.solve()
    print(f"Python Runtime: {sol.python_runtime:.4f}")
    print(f"Equation Solving Time (.so): {sol.solving_time:.4f}")
