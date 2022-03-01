import numpy as np

def interpPH(x1, y1, x2):
    ### based on Matlab code by Mike Sori
    ### By Riley McGlasson, February 2022
    ### Interpolating in a rational way.
    ### inputs must be row vectors
    ### returns interpolated vector y2, with length = len(tx)
    
    if len(x1) != len(y1):
        raise Exception("input vectors are not the same length")
    y2 = np.zeros(len(tx))
    
    for i in range(len(x2)):
        pl1 = np.where(x1 >= x2[i])[0]
        if len(pl1)==0:
            y2[i] = np.nan
        else:
            pl = pl1[0]
        if x2[i] == x1[pl]:
            y2[i] = y1[pl]
        elif pl==0:
            y2[i] = np.nan ##???
        else:
            y2[i]=(x2[i]-x1[pl-1])*(y1[pl]-y1[pl-1])/(x1[pl]-x1[pl-1])+y1[pl-1]
    return y2


def normPH(idata):
    ### demeans and normalizes a given input function to unit std.
    ### Written by Riley McGlasson, February 2022
    ### Based on Matlab code by Mike Sori
    
    odata = idata - np.nanmean(idata)
    odata = odata/np.nanstd(odata)
    
    return odata
    
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
    
    ty = np.arange(len(y))
    tx1 = np.arange(len(x))
    
    tx = np.linspace(min(tx1),max(tx1),length(y))
    x = interpPH(tx1,x,tx)
    
    x = normPH(x)
    y = normPH(y)
    
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
    
    #If we assume that the surface return of both depth profiles corresponds to the same age -- roughly the present,
    # but we don't know if the bottoms are the same, then we will set the last row and column to be zeros. 
    # That way, it allows for the best path to end before (N,M) if necessary.  
    
    zero_col = np.zeros((d.shape[0], 1))  # zeros column as 2D array
    d = np.hstack((d, zero_col))
    zero_row = np.zeros((1,d.shape[1]))
    d = np.vstack((d, zero_row))
    d = np.vstack((d, zero_row))
    
    N = d.shape[0]
    M = d.shape[1]
    
    #COMPUTE COST MATRIX, D
    
    # We want to know the path from element (0,0) to element (N,M) that involves
    # the least total cost.  This begins by setting the first element at (0,0)
    # equal to the first element from d, because this is simply the starting
    # point (under the assumption that the starting signals are from roughyly the same time).  
    
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
    
    print(D)
    #TRAVERSE COST MATRIX TO FIND PATH OF LEAST COST
    # Construct W, a matrix of 2 columns which contains the optimal path from (0,0) to (N,M). 
    # Each row in W is a set of coordinates that the path follows.
    
    n=N-1
    m=M-1
    
    W = [[n,m]]
    
    while n+m > 0:
        steps = [D[n-1,m], D[n-1,m-1], D[n,m-1]]
        if n == 0:
            m = m-1
        elif m == 0:
            n = n-1
        elif steps.index(min(steps)) == 0:
            n = n-1
        elif steps.index(min(steps)) == 1:
            n = n-1
            m = m-1
        elif steps.index(min(steps)) == 2:
            m = m-1
        W = np.vstack((W, [n,m])) 
    
    #calculate statistics
    
    xtune = interpPH(ty[W[:,0]], x[W[0,1]], ty) ##look into how this works better
    
    
    
y=[6,3,2]
x=[5,1,2,4]
        
#dtw_mars(y,x)
tx1 = [0,1,2,3]
x = [5,1,2,4]
tx = np.linspace(min(tx1),max(tx1),8)
interpPH(tx1,x,tx)
normx = normPH(x)
print(np.mean(normx))
print(np.std(normx))
print(normx)
    