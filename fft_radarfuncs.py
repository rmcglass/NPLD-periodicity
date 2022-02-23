import numpy as np
from scipy.fftpack import fft
import statsmodels.api as sm


def fft_radar(depth,values):
    ### takes two nx1 matrices, depth and values
    ### returns (w, P1), a tuple of nx1 matrices where w is the wavelength 
    ### and P1 is the corresponding single sided spectrum of the fft
    ### use: w, P1 = fft_radar(depth,values)
    
    #adapted from Mike Sori's matlab code
    X = depth #in m
    Y = values
    #depth and values must be the same length, and length must be an even number
    if len(X) != len(Y):
        raise Exception("depth and values must be the same length")     
    if len(X) % 2 != 0:
        X.pop()
        Y.pop()

    #Fs = len(Y)/deptht #sampling rate (s).  
    Fs = len(Y)/(X[-1]-X[0]) #sampling rate (m).
    T = 1/Fs
    L = len(X)
    t = np.arange(L)*T 

    #take fft, compute the two-sided spectrum P2. 
    #Then compute the single-sided spectrum P1 based on P2 and the even-valued signal length L
    ffty = fft(Y)
    P2 = np.abs(ffty/L)
    P1 = P2[0:np.int(np.floor(L/2))]
    P1[1:len(P1)-1]=2*P1[1:len(P1)-1]

    #frequency
    f = Fs*np.arange(0,(L/2))/L
    #convert to wavelength
    np.seterr(divide='ignore')
    w = 1/f
    
    return w,P1


def ar1(x,y,fit):
    ### produces an AR1 (markov) series with the same length and lag-1
    ### autocorrelation as y, and fit to a similar trend line
    ### returns m, the AR1 time series
    
    lag1 = sm.tsa.acf(y, nlags=1,fft=True)[1]
    
    mu = np.mean(y)

    sigma = np.std(y)

    errors = np.random.randn(len(y))
    errors = np.square(errors) # negative values don't make sense
    errors = errors * fit # fit errors to best fit skewed gaussian of data
    
    m = [0]*len(y)

    for i in range(1,len(m)):
        m[i]=lag1*m[i-1]+errors[i]

    #make variance(m)=variance(y) and mean(m)=mean(y)
    m = mu + (m - np.mean(m))*(sigma/np.std(m))


   
    
    return m
