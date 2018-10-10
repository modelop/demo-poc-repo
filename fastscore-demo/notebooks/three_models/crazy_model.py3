# fastscore.schema.0: dubs
# fastscore.schema.1: dubs


import numpy as np
from numpy.linalg import inv

def action(x):
    dim = 10 # just dial this number up to increase the pain!
    for x in range(0, 10000000):
        x = x + x
    X = np.random.rand(dim, dim)
    y = inv(X)
    yield y[0,0]
