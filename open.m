[X,Y] = meshgrid(0:1.0:20);

Sol = readtable('newman1/newman1_cpit_gmunoz120723.sol','FileType','text');
B = readtable('newman1/newman1.blocks','FileType','text');
%B=table2array(B(:,[1 2 3 4]));
idx = Sol.Var3 == 0;
S1 = Sol(idx,:);
%T=join(Sol, B, 'LeftKeys',1, 'RightKeys',1)

table_size = height(B) ; 
rows = table_size(1); 
Z=zeros(20,20);

for row = 1:rows 
    x_ind=float(B(row,2))
    y_ind=float(B(row,3))
    Z(x_ind, y_ind ) = B(row,4);
end

surf(X,Y,Z);