function [f, P1 ] = fastfourier( X,depth )
%UNTITLED3 Summary of this function goes here
%   Detailed explanation goes here

Fs = length(X)/depth;
T = 1/Fs;
L= length(X);
t = (0:L-1)*T;

Y = fft(X);
P2 = abs(Y/L);
P1 = P2(1:floor(L/2+1));
P1(2:end-1) = 2*P1(2:end-1);

f = Fs*(0:(L/2))/L;
% figure
% semilogx(f,P1)
% 
% RN = (3*10^-6)*f.^-2;
% hold on
% semilogx(f,RN)
% 
% figure
% semilogx(f,P1)
figure

semilogx(1./f,P1)

end

