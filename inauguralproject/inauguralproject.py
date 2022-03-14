clear

import numpy as np
from scipy import optimize

# a. define given parameters and functions

# a.i define parameters
y = 1
p = 0.2
vartheta = -2

# a.ii generate x values
N=100 #number of elements
x_min=0.01 #minimum value
x_max=0.9 #maximum value

x_values=np.linspace(x_min, x_max, N)

# a.iii define utility function
def utility_function(z,vartheta):
    u = (z ** (1 + vartheta))/(1 + vartheta)
    return u

# b. define value function

def insured_value(q, x, y, p):
    V = p*utility_function((y-x+q-p*q),vartheta)+(1-p)*utility_function((y-p*q),vartheta)
    return -V

obj = lambda q: insured_value(q, x, y, p)

for x in x_values:
    q_max = optimize.minimize_scalar(obj, method = 'brent', bounds = (0,x))
    print(q_max.res)
