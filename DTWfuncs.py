import numpy as np

def dtw_mars(y,x):
    ### takes one radar depth profile (x) 
    ### and tunes it to another depth profile (y)
    ### note: x and y are 1D arrays, that just contain the power values at each depth. 
    ### returns: 
    
    ### Dynamic time warping algorithm
    ### D is the accumulated distance matrix
    ### w is the optimal path
    ### y is the vector you are testing against
    ### x is the vector you are testing

    N = len(y)
    M = len(x)
    x = np.array(x)
    y = np.array(y)
    
    # g sets punishment multiplier for going off diagonal in the cost matrix
    gd = 1
    gy = 1
    gx = 1
    
    #compute d, a matrix of the squared differences between every value of x and y
    d = np.zeros((N,M))
    for n in range(N): #loop through y's
        for m in range(M): #loop through x's
            d[n,m]=(y[n]-x[m])**2
    
    #compute cost matrix
    
    #traverse cost matrix to find path of least cost
    
    #calculate statistics
    
y=[1,2,3]
x=[1,2,3,4]
        
dtw_mars(y,x)
    
    
    