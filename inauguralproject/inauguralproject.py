import numpy as np
from scipy import optimize

# defining given parameters
y = 1
p = 0.2
theta = -2

# defining utility function
def u_func(z, theta):
    return (z ** (1 + theta))/(1 + theta)

# defining value functions

def uninsured_value(x, y, p):
    return p*u_func((y-x), theta) + (1 - p)*u_func(y, theta)

def insured_value(x, y, p, q):
    return p*u_func((y - x + q - p*q), theta)+(1 - p)*u_func((y - p*q), theta)
    
# defining optimizer
def optimal(x, y, p):
    res = optimize.minimize_scalar(lambda q: -insured_value(x, y, p, q), method = 'bounded', bounds = (0,x))
    return res

#defining value function with fixed pi

def value_pi(pi, q, x, y, p):
     return p*u_func((y - x + q - pi), theta)+(1 - p)*u_func((y - pi), theta)

# we guess the solution of pi

pi_guess = 0.01

def optimal_pi(q, x, y, p, V0):
    # objective function
    def obj(pi):
        return value_pi(pi, q, x, y, p) - V0
    # solving V=V0    
    res = optimize.root(obj, pi_guess, method='hybr')
    return  res

# defining monte carlo function

# setting seed number
np.random.seed(123)

# setting parameters
N = 10000
alpha = 2
beta = 7

def agent_value(x, y, p, gamma, pi):
    return u_func((y - (1 - gamma)*x - pi), theta)

def monte_carlo(y, p, gamma, pi, N):
    xs = np.random.beta(alpha, beta, N) # draws N number of xs from a beta distribution
    return np.mean(agent_value(xs, y, p, gamma, pi)) # return average

# guess the solution
pi_guess_c = 0.01

def optimal_pi_c(y, p, gamma, pi, N, U0):
    # objective function
    def U(pi):
        return monte_carlo(y, p, gamma, pi, N) - U0
    # solving U=U0
    sol = optimize.root(U, pi_guess_c, method = 'broyden1')
    return sol