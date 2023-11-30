import numpy as np


def coordinate_descent(equation, argmin, x_0, max_iter=100):
    a = 1
    b = 1
    c = 1
    for i in range(max_iter):
        for x in range(1, 4):
            if x == 1:
                a = a
            if x == 2:
                b = b
            if x == 3:
                c = c

            f = 0.5 * a ** 4 - a * b + b ** 2 + b * c + c ** 2

            if x == 1:
                a = argmin_xi(f)
            if x == 2:
                b = argmin_xi(f)
            if x == 3:
                c = argmin_xi(f)




def argmin_xi(x):
    return np.argmin(x)


# Perform coordinate descent.
coordinate_descent(f, argmin_xi, x_0)

# Print the second coordinate of the minimizer.
print(x[1])