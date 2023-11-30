import numpy as np


def coordinate_descent(equation, argmin, x_0, max_iter=100):
    x = (1, 1, 1)
    f = 0.5 * x[0] ** 4 - x[0] * x[1] + x[1] ** 2 + x[1] * x[2] + x[2] ** 2
    for i in range(max_iter):
        for counter in range(3):
            x[counter] = argmin_xi(f)




def argmin_xi(x):
    return np.argmin(x)


# Perform coordinate descent.
coordinate_descent(f, argmin_xi, x_0)

# Print the second coordinate of the minimizer.
print(x[1])