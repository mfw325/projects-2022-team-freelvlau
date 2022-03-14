def square(x):
    """ square numpy array
    
    Args:
    
        x (ndarray): input array
        
    Returns:
    
        y (ndarray): output array
    
    """
    
    y = x**2
    return y


def utility_function(z,t):
    return (z ** (1 - t))/(1 - t)

def insured_expenditures(q):
        return p((y - x + q[0] - (p * q[0])) ** (1 + vartheta)) / (1 + vartheta) + (1-p)((y - (p * q[0])) ** (1 + vartheta)) / (1 + vartheta)