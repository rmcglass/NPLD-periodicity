import numpy as np

def interpPH(x1, y1, x2):
    ### based on Matlab code by Mike Sori
    ### By Riley McGlasson, February 2022
    ### Interpolating in a rational way.
    ### inputs must be row vectors
    ### returns interpolated vector y2, with length = len(x2)
    
    if len(x1) != len(y1):
        raise Exception("input vectors are not the same length")
    y2 = np.zeros(len(x2))
    
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

def xcPH(y1, y2, XCtype=0):
    # %This function computes the cross correlation (r^2) at zero lag for
    # %two input records.  Records should be sampled at the same 
    # %unifrom intervals.
    # %
    # %records y1 and y2, default is r^2, but if XCtype==1 then returns r.
    # %
    # %function [XC]=xcPH(y1,y2,type,demean);
    # %
    # %y1:     1st record 
    # %y2:     2nd record
    # %type:   0=squared cross-correlation, 1=cross-correlation       (default=0)
    
    pl1 = np.where(np.isnan(y1)==0)
    pl2 = np.where(np.isnan(y2)==0)
    y1 = y1[pl1]
    y2 = y2[pl2]
    
    #demean
    y1=y1-np.mean(y1)
    y2=y2-np.mean(y2)
    
    #XC = np.sum(np.multiply(y1,y2))/(np.sqrt(np.sum(np.multiply(y1,y1))*np.sum(np.multiply(y2,y2))))
    
    if XCtype!=1:
        XC=XC**2
    XC=1
    return XC
    
    
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
    
    tx = np.linspace(min(tx1),max(tx1),len(y))
    x = interpPH(tx1,x,tx)
    
    x = normPH(x)
    y = normPH(y)
    
    N = len(y)
    M = len(x)
    x = np.array(x)
    y = np.array(y)
    
    # g sets punishment multiplier for going off diagonal in the cost matrix
    g = 2
    

    
    #compute d, a matrix of the squared differences between every value of x and y
    d = np.zeros((N,M))
    for n in range(N): #loop through y's
        for m in range(M): #loop through x's
            d[n,m]=(y[n]-x[m])**2
    
    #If we assume that the surface return of both depth profiles corresponds to the same age -- roughly the present,
    # but we don't know if the bottoms are the same, then we will set the last row and column to be zeros. 
    # That way, it allows for the best path to end before (N,M) if necessary.  
    
#     zero_col = np.zeros((d.shape[0], 1))  # zeros column as 2D array
#     d = np.hstack((d, zero_col))
#     zero_row = np.zeros((1,d.shape[1]))
#     d = np.vstack((d, zero_row))
    
    N = d.shape[0]
    M = d.shape[1]
    
    d[-1,:]=0
    d[:,-1]=0
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
            D[n,m] = d[n,m]+ min(D[n-1,m-1], g*D[n-1,m], g*D[n,m-1])
    
    
    #TRAVERSE COST MATRIX TO FIND PATH OF LEAST COST
    # Construct W, a matrix of 2 columns which contains the optimal path from (0,0) to (N,M). 
    # Each row in W is a set of coordinates that the path follows.
    
    n=N-1
    m=M-1
    
    W = [[n,m]]
    
    while n+m > 0:
        steps = [D[n-1,m-1], D[n-1,m], D[n,m-1]]
        if n == 0:
            m = m-1
        elif m == 0:
            n = n-1
        elif steps.index(min(steps)) == 0:
            n = n-1
            m = m-1
        elif steps.index(min(steps)) == 1:
            n = n-1
        elif steps.index(min(steps)) == 2:
            m = m-1
        W = np.vstack((W, [n,m])) 
    
    #calculate statistics
    #ty = np.arange(N)
    xtune = interpPH(ty[W[:,0]], x[W[:,1]], ty) #interpolate the values of the tuned x record at the times for y  
    XC = xcPH(xtune,y,1)                        # cross-correlation between the tuned x record and the y record
    tstd = np.std(ty[W[:,0]] - tx[W[:,1]])      # standard dev of the difference between times along the min cost path
    dt = interpPH(ty[W[:,0]],ty[W[:,0]] - tx[W[:,1]],ty); # differences between times along the min cost path, interpolated at the times for y

    
    return xtune, XC, tstd, dt, W, D
    
# y=[6,3,2]
#x=[5,1,2,4]
#x2=[5,1,2,4]        

# tx1 = [0,1,2,3]
# x = [5,1,2,4]
# tx = np.linspace(min(tx1),max(tx1),8)
#dtw_mars(x,x2)

    