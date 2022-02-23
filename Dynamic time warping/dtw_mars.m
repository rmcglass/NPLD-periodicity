function [xtune, XC, tstd, dt, closeness, w] = dtw_mars(y,x,qplot)

%This takes a piece of Mars stratigraphy with units brightness, slope, etc
%as a function of depth, and tunes it to a forcing function y

%Dynamic Time Warping Algorithm
%D is the accumulated distance matrix
%w is the optimal path
%y is the vector you are testing against
%x is the vector you are testing


ty = 1:length(y);
tx1 = 1:length(x);

tx = linspace(min(tx1),max(tx1),length(y));
x = interpPH(tx1,x,tx);

x = normPH(x(:));
y = normPH(y(:));


% The above lines normalizes the vectors t and r to unit standard deviation
% and demeans them, i.e. normPH(t) has mean=0 and std=1.  

N = length(y);
M = length(x);

% g=2;
gd = 1;
gy = 1;
gx = 1;
% g is the "punishment" multiplier for going off diagonal in the cost
% matrix.  

%d = zeros(5000,5000);
%for n=1:N
%    for m=1:M
%        d(n,m)=(y(n)-x(m))^2;
%    end
%end


d = (repmat(y,1,M)-repmat(x',N,1)).^2; %this replaces the nested for loops from above Thanks Georg Schmitz 

d(:,end)=zeros;
d(end,:)=zeros;

%figure; imagesc(d)

% A matrix d of N rows and M columns is created.  The elements are the
% squared differences between every possible combination of an element in t
% and an element in r.  Variation of t happen on the "vertical axis" and
% variations of r happen on the "horizontal axis."  

% d(1,:)=d(1,:); %*0.01;
% d(:,end)=d(:,end); %*0.01;

% These lines of statements do nothing at the moment.

% D=zeros(size(d));
% D(1,1)=d(1,1);
% 
% % This begins to construct the accumlated distance (ie cost) matrix D.  We
% % want to know the path from element (1,1) to element (N,M) that involves
% % the least total cost.  This begins by setting the first element at (1,1)
% % equal to the first element from d, because this is simply the starting
% % point.  
% 
% 
% 
% if 1,
%   for n=2:N
%     D(n,1)=d(n,1)+D(n-1,1);
%   end
%   for m=2:M
%     D(1,m)=d(1,m)+D(1,m-1);
%   end
% end;
% 
% % In making a path from (1,1) to (N,M), we are only allowed to take steps
% % to the right, down, or diagonally down-right.  Thus, the first row/column
% % of D is simply equal to the accumulated sum of the elements of d to the left/up
% % of it (because there is only one possible path to get to, say, element
% % (N,1) - straight down the first column).  
% 
% for n=2:N
%   for m=2:M
%     D(n,m)=d(n,m)+min([g*D(n-1,m),D(n-1,m-1),g*D(n,m-1)]);
%   end
% end
% 
% % This fills in the remaining elements of D.  Each element can be reached
% % from either the element to the left, top, or upper-left of it.  Each
% % element is thus set to the minimum of these three adjacent elements, plus
% % the cost associated with that element from d (after the g-factor has been
% % multiplied in).  

D = mexGetCostMatrix(d,gd,gy,gx); % This calls a C mex function to calculate the cost matrix

% Dist=D(N,M);
n=N;
m=M;
% k=1;
w=[];
w(1,:)=[N,M];
while n+m > 2
    if n == 1
        m = m-1;
    elseif m == 1
        n = n-1;
    else
        [values,number] = min([D(n-1,m),D(n,m-1),D(n-1,m-1)]);
        switch number
            case 1
                n = n-1;
            case 2
                m = m-1;
            case 3
                n = n-1;
                m = m-1;
        end
    end
%     k=k+1;
    w = cat(1,w,[n m]);
end


% These lines construct W, which is a matrix of two columns which contains
% the optimal path from (1,1) to (N,M).  Each row in W is a set of
% coordinates that the path follows.  k is a counter variable; it is equal
% to the number of steps in the path.

% if qplot

w2 = w(w(:,1)==N);
w3 = w(w(:,2)==M);
closeness = max(length(w2),length(w3))/N;



pl=find( (w(:,1)>1) & (w(:,2)>1)); % Finds the portion of the path that is not on the uppermost row or the leftmost column
pl=[pl; pl(end)+1]; % Adds the first point on the path that is on the uppermost row or the leftmost column

xtune = interpPH(ty(w(:,1)),x(w(:,2)),ty);   % interpolate the values of the tuned x record at the times for y  
XC = xcPH(xtune,y,1);                        % cross-correlation between the tuned x record and the y record
tstd = std( ty(w(:,1)) - tx(w(:,2)));     % standard dev of the difference between times along the min cost path
dt = interpPH(ty(w(:,1)),ty(w(:,1)) - tx(w(:,2)),ty); % differences between times along the min cost path, interpolated at the times for y
  
% xc is the cross-correlation (covariance) between x2 and y.  It is the
% value displayed on the resulting plots that we have been looking at.  

  
% $$$   figure(1); clf; hold on;
% $$$   subplot(311); hold on;
% $$$   plot(tr,r,'k');
% $$$   plot(tt,t,'r');
% $$$   
% $$$   subplot(312); hold on;
% $$$   plot(tr(w(pl,2)),r(w(pl,2)),'k');
% $$$   plot(tt(w(pl,1)),t(w(pl,1)),'r');
% $$$   
% $$$   subplot(313); hold on;
% $$$   plot(tr,r2,'k');
% $$$   plot(tr,t,'r');

% end


if qplot == 1

    figure
    
    num=5;
    for ct=1:num-1;
        sp(ct,:)=(2:num)+(ct-1)*num;
        sp2(ct)=(ct-1)*num+1;
    end;
    subplot(num,num,sp(:));
    cla;
    hold on;
%     imagesc(d);
    imagesc(D./10000);
    axis equal tight;
%    col = jet(64); tmp = linspace(0,1,64)';
%for n = 1:3, col(:,n) = interp1( 10.^tmp, col(:,n), 1+9*tmp, 'linear'); end
%colormap(col)
    colormap('jet')
%     h=plot(1:length(y),1:length(y),'--r'); set(h,'linewidth',2);
    h=plot([1 M],[1 N],'--w'); set(h,'linewidth',2);
    
%     h=plot(w(pl,2),w(pl,1),'y'); set(h,'linewidth',2);
%    h=plot(w2(:,1),w2(:,2),'-b','Color',[.5 .5 .5]); set(h,'linewidth',6)
    h=plot(w(:,2),w(:,1),'k'); set(h,'linewidth',3);
    set(gca,'ydir','normal');
    set(gca,'yaxisloc','right');
    set(gca,'xaxisloc','top');
    xlabel('Depth (arbitrary units)','fontsize',18)
    ylabel('Time (kyr)','fontsize',18)
   
    axes('LineWidth',3)
    
    subplot(num,num,sp2'); cla; hold on;
    plot(y,ty,'k');
%     plot(x(w(pl,2)),tx(w(pl,1)),'r');
%    plot(xtune,ty,'r');
    axis tight;
    title(num2str(XC,3),'fontsize', 14);
    
    subplot(num,num,num*(num-1)+2:num*num)
    plot(tx,x,'k');
    axis tight;
    
    drawnow;
    
%figure
%plot(ty,y,'k','linewidth',1.5)
%hold on
%plot(ty,xtune,'--r','linewidth',1.5)
end

