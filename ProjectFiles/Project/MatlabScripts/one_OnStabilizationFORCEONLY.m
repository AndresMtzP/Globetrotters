%Christopher Pakosta
%813244465
%EE490 Maglev attempt

% About the maglev system:  The maglev system formulas below are for
% levitating from the bottom with 2 permanant magnets(one in the levitated 
% device and one in lower base) and four inductor coils to help maintain 
% stability. 

uo = (4*pi*10^(-7));
% t = [] %time
% Sx =  %Surface area between magnets
% ur =   %permeability of magnets
% Hca =  %coercive force of magnet a
% Hcb =  %coercive force of magnet b
% lA =  %length of magnet a (height)
% lB =  %length of magnet b (height)
% x =  %air gap distance
% rb =  %bottom ring diameter
% N =  %number of turns in each inductor
% I =  %Current in each inductor 

syms  t Sx ur Hca Hcb lA lB x rb N I

%_______________________________________________________________________%
%At complete balance (when inductors do not contribute H fields)
% the force equation is below No contributing current

% NOTE: must obey ( NI < Hc*l ) or permanant magnets will demagnetize
% NOTE: must obey ( NI < 2Hc*l ) or permanant magnets will demagnetize
% NOTE: equation below ignores fringing
% NOTE: equation below assumes infinite permeability in the ferrous
% inductor core (or infinite conductance)

F_balance = Sx*uo*(ur^2)*((Hca*lA + Hcb*lB)/((ur*x)+(ur*sqrt((x^2)+(rb^2)) +lB+lA)))

%______________________________________________________________________%

%Equation below is the force applied in ONE inductor for stabilization 
%with the distance and current as factors controlling the force

%NOTE positioning of inductors with a ring will help produce accurate
%calculations.  COME BACK AND CORRECT THIS LATER ONCE WE FIND OUT WHAT WE
%ARE DOING.

F_correction = Sx*uo*(ur^2)*((N*I + Hca*lA + Hcb*lB)/((ur*x)+(ur*sqrt((x^2)+(rb^2)) +lB+lA)))





