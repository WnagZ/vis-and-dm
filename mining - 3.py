import numpy as np

# Defines the given function
def f(x):
    return x[0]**4 + 2*x[0]*x[1] + 4*x[1]**2 + x[0]

# Calculates gradient of f at point x=(x1, x2)
def gradient_f(x):
    x1, x2 = x #defines point x
    df_dx1 = 4 * x1**3 + 2 * x2 + 1  #derivative w.r.t. x1
    df_dx2 = 2 * x1 + 8 * x2 #derivative w.r.t. x2
    return np.array([df_dx1, df_dx2])

# Implements function gradient descent which performs max_iter gradient descent steps
def gradient_descent(f, grad_f, eta, x_0, max_iter=100):
    x_t = x_0
    for t in range(max_iter):
        gradient = grad_f(x_t)
        x_t = x_t - eta(t) * gradient #applies iteration for each step
    return x_t

# Returns constant c as step size
def eta_const(t, c=0.1):
    return c

# Returns computed step size
def eta_sqrt(t, c=0.1):
    return c / np.sqrt(t + 1)

# Multistep step size policy
def eta_multistep(t, milestones, c=0.5, eta_init=0.1):
    if t < milestones[0]:
        return eta_init # if t is less than the milestone, returns initial stepsize
    for i in range(1, len(milestones)):
        if milestones[i - 1] <= t < milestones[i]:
            return c**i * eta_init #if t is between two milestones, it returns the computed stepsize
    return c**len(milestones) * eta_init #if t is g.t.eq. to the last milestone, returns the computed stepsize

# Initial point
x_0 = np.array([1, -1])

# Number of iterations
max_iter = 100


#Solving question a)
# Performs gradient descent
result_eta_const = gradient_descent(f, gradient_f, eta_const, x_0, max_iter)

# Evaluates the function at x_100
f_x_100_eta_const = f(result_eta_const)

# Prints the result
print("Result using eta_const:", np.round(f_x_100_eta_const, 3))

#Solving question b)
# Performs gradient descent
result_eta_sqrt = gradient_descent(f, gradient_f, eta_sqrt, x_0, max_iter)

# Evaluates the function at x_100
f_x_100_eta_sqrt = f(result_eta_sqrt)

# Prints the result
print("Result using eta_sqrt:", np.round(f_x_100_eta_sqrt, 3))


#Solving question c)
# Performs gradient descent
result_eta_multistep = gradient_descent(f, gradient_f, lambda t: eta_multistep(t, [10, 60, 90], c=0.5, eta_init=0.1), x_0, max_iter)
# Evaluates the function at x_100
f_x_100_eta_multistep = f(result_eta_multistep)
# Prints the result
print("Result using eta_multistep:", np.round(f_x_100_eta_multistep, 3))
