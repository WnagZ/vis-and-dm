import numpy as np
from sympy import symbols, diff

def coordinate_descent(f, argmin, x_0, max_iter=100):
    # y = symbols('y')
    for i in range(max_iter):
        for counter in range(3):
            # x_0[counter] = y
            x_0[counter] = argmin_xi(f)
    return x_0

def argmin_xi(x):
    #diff(f, y)
    return np.argmin(x)


# Perform coordinate descent.
x_0 = [1, 1, 1]
f = 0.5 * x_0[0] ** 4 - x_0[0] * x_0[1] + x_0[1] ** 2 + x_0[1] * x_0[2] + x_0[2] ** 2
coordinate_descent(f, argmin_xi, x_0)

# Print the second coordinate of the minimizer.
print(x_0[1])