% Christopher Pakosta 
% 4-14-2017
% Magnetization of Base Ring Magnet 
%
%
%
%
% B field reading from Measurement of SS49E Hall-Effect Sensor
% measurement @ x=0, y=0, z=0 using a cartesian cordinate system reading 
% from the center of the ring


%***********************************************************************
%       Initial Parameters

Bmeas = 0.029; % Measured Tesla unit @ z=0  ONLY!!!! (our value: 0.029)

r = 0.0475; %inner diameter (our value: 0.0475)   0.055
R = 0.09; %outer diameter (our value: 0.09 )  0.065
d = 0.02; %depth of ring magnet (our value: 0.02) 0.03
z = 0.032; %Resting Height of magnet (our value: 0.015) 0.032
Wo = 0.01; %distance to electromagnets edge from center, radius (our value: 0.01) 0.02
PA = 0.073435; % (our value 0.073435) % POle area of base ring magnet 

%************************************************************************


%make sure radius, and depth are in meters
s1 = sqrt(r^2 + d^2); %sqrt of inner diameter and depth
s2 = sqrt(R^2 + d^2); %sqrt of outer diamter and depth

M_ringmagnet = 2*Bmeas*(s1*s2)/((-d*s2)+(d*s1)) % (Our Value 0.3389)  1.23  
%Magnetization of the Base Ring Magnet



%*********************************************************************
% Calculating B-Field at a point x=0.1mm displaced from ring magnet
%
%


% OUR Base Ring Magnet Parameters
%r =  0.0475; %Inner radius
%R =  0.09; %Outer radius
%d =  0.02; %depth of ringmagnet

%For resting Height of 0.015 meters (1.5cm)

L = sqrt(z^2 + 0.0001^2); %changing distance

FirstTerm = ((-d-L)/(sqrt(r^2 + (-d-L)^2)));
SecTerm = ((-d-L)/(sqrt(R^2 + (-d-L)^2)));
ThirdTerm = (L/(sqrt(r^2 + L^2)));
FourthTerm = (L/(sqrt(R^2 + L^2)));

B_ringmagnet =  (M_ringmagnet/2)*(FirstTerm-SecTerm+ThirdTerm-FourthTerm)

 

F_ringmagnet_rest =  ((B_ringmagnet^2)*PA / (2.5133*(10^(-6))))

inv_sin_xdirec = asind(z/(sqrt(0.0001^2 + z^2))); %0.0001 x-displacement
F_ringmagnet_onemm_xdirect_SecondTerm = cosd(inv_sin_xdirec);
F_ringmagnet_onemm_rest_xdirect = F_ringmagnet_rest*F_ringmagnet_onemm_xdirect_SecondTerm

%*************************************************************************
%    Calculating I_0


%************************************************************************
%      Change values here for different systems

u_o = (4*3.14)*10^(-7);
r_ele = 0.0085; %PUT IN METERS (Our value 0.0085) USE CORE DIAMETER OR INNERDIAMETER  0.0197
A_ele = 3.14*((r_ele)^2);
N = 288; %(Our value 288)  759
%************************************************************************

frst_denom = ((z^2)+((Wo-.0001)^2)); % Replace 0.022 with z for HIS value!!
sec_denom = ((z^2)+((Wo+0.0001)^2)); % Replace 0.022 with z for HIS value!!

SecStep_num = (4.53)*frst_denom*sec_denom; %F_ringmagnet_onemm_rest_xdirect
SecStep_den = (sec_denom*u_o*A_ele*(N^2))+(frst_denom*u_o*A_ele*(N^2));

 I_o = sqrt(SecStep_num/SecStep_den)
 I_o_dividebytwo = I_o /2 





