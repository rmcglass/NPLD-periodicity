import numpy as np

def dtw_mars(y,x,qplot)
    ### takes one radar depth profile (x) with radar power as a function of depth
    ### and tunes it to another depth profile (y)
    ### returns: 
    
    ### Dynamic time warping algorithm
    ### D is the accumulated distance matrix
    ### w is the optimal path
    ### y is the vector you are testing against
    ### x is the vector you are testing

    N = len(y)
    M = len(x)
    
    # g sets punishment multiplier for going off diagonal in the cost matrix
    gd = 1
    gy = 1
    gx = 1
    
    