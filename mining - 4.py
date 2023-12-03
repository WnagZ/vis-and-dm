import numpy as np


def f(x):
    return np.argmin(0.5 * x[0] ** 4 - x[0] * x[1] + x[1] ** 2 + x[1] * x[2] + x[2] ** 2)


def argmin_x1(x):
    return np.argmin(2 * x[0] ** 3 - x[1])

    # return (x[1] ** 2 + x[1] * x[2]) / (2 * x[0] ** 3 - 1)


def argmin_x2(x):
    return np.argmin(- x[0] + 2 * x[1] + x[2])
    # return (x[0] ** 2 + x[0] * x[2] - x[0]) / (2 * x[2])


def argmin_x3(x):
    return np.argmin(x[1] + 2 * x[2])
    # return (x[0] * x[1] + 2 * x[2]) / (x[0] ** 2 + x[1] ** 2)


def coordinate_descent(f, argmin, x_0, max_iter=100):
    # y = symbols('y')
    x_t = x_0.copy()
    for i in range(max_iter):
        for j in range(len(x_t)):
            x_t[j] = argmin[j](x_t)
    return x_t


x_0 = [1, 1, 1]
argmin = [argmin_x1, argmin_x2, argmin_x3]
x_min = coordinate_descent(f, argmin, x_0)

print(f(x_0))

print(x_min[1])


# def coordinate_descent(f, argmin, x_0, max_iter=100):
#     # y = symbols('y')
#     for i in range(max_iter):
#         for counter in range(3):
#             # x_0[counter] = y
#             x_0[counter] = argmin_xi(f)
#     return x_0
#
#
# def argmin_xi(x):
#     # diff(f, y)
#     return np.argmin(x)
#
#
# # Perform coordinate descent.
# x_0 = [1, 1, 1]
# f = 0.5 * x_0[0] ** 4 - x_0[0] * x_0[1] + x_0[1] ** 2 + x_0[1] * x_0[2] + x_0[2] ** 2
# coordinate_descent(f, argmin_xi, x_0)

# Print the second coordinate of the minimizer.
# print(x_0[1])
