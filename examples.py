import numpy as np

def lorenz_string():
    lorenz_str_func = ['dx/dt = sigma * (y - x)', 'dy/dt = rho * x - y - x * z', 'dz/dt = x * y - beta * z']
    lorenz_str_const = ['sigma = 10e0', 'rho = 28e0', 'beta = 8e0 / 3e0']
    return lorenz_str_func, lorenz_str_const

def lorenz_for_scipy(w, t):
    x, y, z = w

    sigma = 10e0
    rho = 28e0
    beta = 8e0 / 3e0

    w = np.array([sigma * (y - x),rho * x - y - x * z, x * y - beta * z])
    return w


def mechsys_for_scipy(w, t):
    s0, s1, s2, s3, s4, s5, s6 = w

    F = 10
    V_wall = 0
    k1, k2, k3, k4 = 1, 1, 1.0, 1
    m1, m2, m3 = 1.0, 2.0, 3.0
    b1 = 2

    w = np.array([
        s4 / m3 - s5 / m2,
        s5 / m2 - s6 / m1,
        s6 / m1 - V_wall,
        s5 / m2 - V_wall,
        -k4 * s0 + F,
        k4 * s0 - b1 * s5 / m2 - k3 * s1 + b1 * s6 / m1 - k1 * s3,
        b1 * s5 / m2 + k3 * s1 - b1 * s6 / m1 - k2 * s2
    ])

    return w


def lorenz_for_python(x, y, f):
    """
    1st inital condition: (0, 1, 0)
    2nd initial condition: (0, 1.001, 0)

    (a, b) = (0, 50)
    """
    sigma = 10e0
    rho = 28e0
    beta = 8e0 / 3e0

    f[0] = sigma * (y[1] - y[0])
    f[1] = rho * y[0] - y[1] - y[0] * y[2]
    f[2] = y[0] * y[1] - beta * y[2]

    return f

def mechsys_for_python(x, y, f):
    F = 10
    V_wall = 0
    k1, k2, k3, k4 = 1, 1, 1.0, 1
    m1, m2, m3 = 1.0, 2.0, 3.0
    b1 = 2

    f[0] = y[4] / m3 - y[5] / m2
    f[1] = y[5] / m2 - y[6] / m1
    f[2] = y[6] / m1 - V_wall
    f[3] = y[5] / m2 - V_wall
    f[4] = - k4 * y[0] + F
    f[5] = k4 * y[0] - b1 * y[5] / m2 - k3 * y[1] + b1 * y[6] / m1 - k1 * y[3]
    f[6] = b1 * y[5] / m2 + k3 * y[1] - b1 * y[6] / m1 - k2 * y[2]

    return f

def lorenz_for_c(x, y, f):
    sigma = 10e0
    rho = 28e0
    beta = 8e0 / 3e0

    f[0] = sigma * (y[1] - y[0])
    f[1] = rho * y[0] - y[1] - y[0] * y[2]
    f[2] = y[0] * y[1] - beta * y[2]