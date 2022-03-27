# Importing the following packages:
import numpy as np
from scipy import optimize

# We are defining the model:

    # Given parameters in the assignment:
    y = 1
    p = 0.2
    theta = -2

    # Utility function
    def u_func(z, theta):
        
        """ Agents utility of asset:
            
            Args:
                z (input array): input to utility function.
                theta (float): the degree of relative risk aversion (theta = -2).
                
            Returns:
                u (float): utility for given input. 
        """
        return (z ** (1 + theta))/(1 + theta)

    # Value function for both insured and uninsured:

    def uninsured_value(x, y, p):

        """ Expected utility for uninsured agents:
    
            Args:
                y (float):  Total assets of agent. 
                x (float):  Monetary loss in the case of a bad outcome. If x = 0, the agent does not experience any
                            monetary loss (positive outcome).
                p (float):  Probability of monetary loss
        
            Returns:
                Uninsured_value (float): Expected utility without insurance.
        """
        return p*u_func((y-x), theta) + (1 - p)*u_func(y, theta)

    def insured_value(x, y, p, q):
        
        """ Expected utility for insured agents:
    
            Args:
                y (float):  Total assets of agent. 
                x (float):  Monetary loss in the case of a bad outcome. If x = 0, the agent does not experience any
                            monetary loss (positive outcome).
                p (float):  Probability of monetary loss
                q (float):  Coverage amount - (q = 0 as the consumer is not insured)
        
            Returns:
                Insured_value (float): Expected utility with insurance.
        """
        return p*u_func((y - x + q - p*q), theta)+(1 - p)*u_func((y - p*q), theta)

# Question 1: 

    # i. We are defining an function, which returns the optimized coverage amount, q*. The coverage q* maximizes expected
    #    utility for the agents in the case, where the premium is just equal to the expected insurance payout, pi = q*p.

    def optimal(x, y, p): 
        
            """
            Optimal coverage amount, q, for the given monetary loss, x, of the agents.
            
            Args:
                y (float):  Total assets of agent. 
                x (float):  Monetary loss in the case of a bad outcome. The upper bound for x is between (0.01 - 0.9).
                p (float):  Probability of monetary loss
                
            Returns:
                  solution_q (array): Optimal coverage, q*, cannot be higher than the monetary loss. This means that the
                                      bounds for q are (0 - 0.9).
            """
        res = optimize.minimize_scalar(lambda q: -insured_value(x, y, p, q), method = 'bounded', bounds = (0,x))
        return res
    
# Question 2: 

    # i. We are defining value function with fixed pi: 

    def value_pi(pi, q, x, y, p):   
            """
            Expected utility value with fixed pi. 
            
            Args:
            y (float):  Total assets of agent. 
            x (float):  Monetary loss in the case of a bad outcome. The upper bound for x is between (0.01 - 0.9).
            p (float):  Probability of monetary loss
            pi (float): Price of insurance
        
            Returns: 
            Expected utility (float or array): Agent being insured with coverage q and the optimal premium pi.
            """
            return p*u_func((y - x + q - pi), theta)+(1 - p)*u_func((y - pi), theta)

    # ii. we guess the solution of pi_tilde, which is the premium that makes the expected utility of 
    # getting insurance equal to the utility from not getting insurance.

    pi_guess = 0.01

    def optimal_pi(q, x, y, p, V0):
        
            """
            Maximizing premium - solving for the optimal pi:
        
            Args:
            y (float):  Total assets of agent. 
            x (float):  Monetary loss in the case of a bad outcome. The upper bound for x is between (0.01 - 0.9).
            p (float):  Probability of monetary loss
            V0 (float):  Expected utility for uninsured agents.
            
            Returns: 
            result_pi_optimal (float or array): 
        
            """
    # We are defining the objective function and optimizing.
        def obj(pi):
            return value_pi(pi, q, x, y, p) - V0

    # Solving for the expected value to be V = V0    
        res = optimize.root(obj, pi_guess, method='hybr')
        return  res
    
# Question 3: 
    
    # i. Defining monte carlo function by setting seed number and parameters.
    np.random.seed(123)
    N = 10000
    alpha = 2
    beta = 7

    def agent_value(x, y, p, gamma, pi):
        
        """
        A modification of previous function for expected utility, which calculates the
        agent's expected utility, when the loss, x, is drawn from a beta distribution and a fraction, gamma, is covered. 
        
        Args:
            y (float):  Total assets of agent. 
            x (float):  Monetary loss in the case of a bad outcome. The upper bound for x is between (0.01 - 0.9).
            p (float):  Probability of monetary loss
            pi (float): Price of insurance
            gamma (float): Fraction of loss that is covered by insurance. 
            
        Returns: Utility for given gamma and pi
        """
        return u_func((y - (1 - gamma)*x - pi), theta)

    def monte_carlo(y, p, gamma, pi, N):
        
    """
        Function that calculates difference in expected utility from having the full loss 
        covered and only a fraction, gamma, covered.
        
        Args:
            y (float):  Total assets of agent. 
            p (float):  Probability of monetary loss
            pi (float): Price of insurance
            gamma (float): Fraction of loss that is covered by insurance. 
        
        Returns:  
    """
        xs = np.random.beta(alpha, beta, N) # draws N number of xs from a beta distribution
        return np.mean(agent_value(xs, y, p, gamma, pi)) # return average
    
# Question 4: 

    # We begin with setting the interial guess for the solution. 
    
    pi_guess_c = 0.01

    def optimal_pi_c(y, p, gamma, pi, N, U0):
        
        """
        Calculates the profit maximizing premium when insurer acts as a monopolist,
        the client's loss is stochastic and coverage is proportional to the loss.
        
            Args:
            gamma (float): Fraction of loss that is covered by insurance. The parameter is fixed equal to 0.95. 
            x (array): Distribution of losses.
        
            Returns:  
        """
        def U(pi):
            
        """
            This function minizimses the difference between the utility for insured and uninsured agents.  
        
        Args:
            gamma (float): Fraction of loss that is covered by insurance. The parameter is fixed equal to 0.95. 
            x (array): Distribution of losses.
        
        Returns:  
            Solution_utility 
        """
            return monte_carlo(y, p, gamma, pi, N) - U0
        
        # solving the utility for insured agents being equal to uninsured agents. 
        sol = optimize.root(U, pi_guess_c, method = 'broyden1')
        
        return sol