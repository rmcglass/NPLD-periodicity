import numpy as np

def dtw_mars(y,x):
    ### takes one radar depth profile (x) 
    ### and tunes it to another depth profile (y)
    ### note: x and y are 1D arrays, that just contain the power values at each depth. 
    ### returns:
    ### Written by Riley McGlasson, February 2022
    ### Based on Matlab code by Mike Sori
    
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
    g = 1
    
    #compute d, a matrix of the squared differences between every value of x and y
    d = np.zeros((N,M))
    for n in range(N): #loop through y's
        for m in range(M): #loop through x's
            d[n,m]=(y[n]-x[m])**2
    
    #if you want to constrain the age, set the last row? column? to zeros. I'm not sure which, ask Mike
    #I think it's both
    zero_col = np.zeros((d.shape[0], 1))  # zeros column as 2D array
    d = np.hstack((d, zero_col))
    zero_row = np.zeros((1,d.shape[1]))
    d = np.vstack((d, zero_row))
    
    N = d.shape[0]
    M = d.shape[1]
    
    #COMPUTE COST MATRIX, D
    
    # We want to know the path from element (0,0) to element (N,M) that involves
    # the least total cost.  This begins by setting the first element at (0,0)
    # equal to the first element from d, because this is simply the starting
    # point.  
    
    D=np.zeros(d.shape)
    D[0,0]=d[0,0]
    
    # Construct first row/column of D. This will just be the accumulated sum of the element of d
    # to the left/up of it (because the only way to get to (N,0) or (0,M) is straight down or across.
    
    for n in range(1,N):
        D[n,0] = d[n,0]+D[n-1,0]
    for m in range(1,M):
        D[0,m] = d[0,m]+D[0,m-1]
        
    # Fill in the rest of the matrix D. Each element can be reached from the left, above, or upper-left.
    # Each element of D is set to the minimum of the cost of these three elements (from D), plus the 
    # new cost associated with accessing that element (from d). If the g-factor is used to punish leaving the diagonal,
    # it is multiplied in before the value from d is added.
    
    for n in range(1,N):
        for m in range(1,M):
            D[n,m] = d[n,m]+ min(g*D[n-1,m], D[n-1,m-1], g*D[n,m-1])
    
    
    #TRAVERSE COST MATRIX TO FIND PATH OF LEAST COST
    
    #calculate statistics
    
y=[6,3,2]
x=[5,1,2,4]
        
dtw_mars(y,x)
    
    
    