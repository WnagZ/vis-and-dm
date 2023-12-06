from scipy.optimize import minimize_scalar

def f(x):
    return 0.5 * x[0] ** 4 - x[0] * x[1] + x[1] ** 2 + x[1] * x[2] + x[2] ** 2

def argmin_x1(x):
    result = minimize_scalar(lambda a: f([a, x[1], x[2]]))
    return result.x

def argmin_x2(x):
    result = minimize_scalar(lambda b: f([x[0], b, x[2]]))
    return result.x

def argmin_x3(x):
    result = minimize_scalar(lambda c: f([x[0], x[1], c]))
    return result.x

def coordinate_descent(f, argmin, x_0, max_iter=100):
    x_t = x_0.copy()
    for i in range(max_iter):
        for j in range(len(x_t)):
            x_t[j] = argmin[j](x_t)
    return x_t

x_0 = [1, 1, 1]
argmin = [argmin_x1, argmin_x2, argmin_x3]
x_min = coordinate_descent(f, argmin, x_0)

print(x_min[1])