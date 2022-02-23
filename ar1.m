function y = ar1(x)

% produces an AR1 (markov) time series with the same length and lag-1
% autocorrelation as x

% randn('state',sum(100*clock));

lag1=xcorr(x,'coeff'); 
lag1=lag1((length(lag1)-1)/2); % lag-1 autocorrelation

mu = mean(x);

sigma = std(x);

errors = randn(size(x));

y=zeros(size(x));

for i=2:length(y)
   
    y(i)= lag1*y(i-1) + errors(i);
    
end

% normalize so variance(y) = variance(x)
y = y/std(y)*sigma;

% add the mean of x
y = y+mu;