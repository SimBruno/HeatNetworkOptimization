#The goal of this part is to determine an optimized dTmin such that costs are minimized. 
#In all scenarios we will do the following:
#1. Determine the area of the HX in term of the dTmin
#2. Determine the cost of the HX in term of the the Area
#3. Determine the cost of the HX in term of the dTmin

# ##Scenario 1: dTmin for the past5 

# ### Determine the area of the HX in term of the dTmin

import numpy as np
import matplotlib.pyplot as plt
#from codes_01_energy_bill.coolprop_functions import mixture



T1 = 333
T2 = 348

p1 = 100000

h1 = -91021.1032324004
h2 = -38880.66837888083

m1 = 0.48
m2 = 0.55
cp1 = 3400
cp2 = 2976.18181818181

slope1 = 1/(m1*cp1)
slope2 = 1/(m2*cp2)

#Plot the two lines with T on the y-axis and h on the x-axis
#h is the enthalpy of the stream between h1 and h2
N = 3
h = np.linspace(h1, h2, N)

T_1 = T1 - slope1*h1
T1v = slope1*h + T_1

T_2 = T2 - slope2*h2
T2v = slope2*h + T_2

plt.plot(h, T1v)
plt.plot(h, T2v)
plt.xlabel('Enthalpy (kJ/kg)')
plt.ylabel('Temperature (K)')
plt.title('Temperature vs Enthalpy')
plt.grid(True)
plt.show()
print(slope1)
print(slope2)

#
Q=0
alpha=0
U = alpha/2
dTmin = 0




'''
#

T1= 60+273
T2 = 75+273
m1 = 0.48
m2 = 0.55
cp1 = 3470.44
cp2 = 3482.19



slope_cold = 1/(m1*cp1)
slope_hot = 1/(m2*cp2) 


#State_Past5=mixture(T=T2, P=100000, frac_water=0.5, frac_fat=0.5)
#print(State_e6)
h1=-91021
h2=-38880.66                    

T2_prime = T2 - slope_hot*h2
print(T2_prime)                 


#plot the two lines with T on the y-axis and h on the x-axis
#h is the enthalpy of the stream between h1 and h2
N = 100
h = np.linspace(h1, h2, N)
T = np.linspace(T1, T2, N)


Tcold = T1 + h*slope_cold
Thot = T2_prime + h*slope_hot  
plt.plot(h, Tcold, label='Cold Stream')
plt.plot(h, Thot, label='Hot Stream')
plt.xlabel('Enthalpy (J/kg)')
plt.ylabel('Temperature (K)')

#Plot as a vertical line the dTmin (i.e. the minimum temperature difference between the two streams)
dt = Thot-Tcold
dTmin = dt.min()
min_index = dt.argmin()
plt.axvline(x=h[min_index], color='r', linestyle='--')

plt.title('Temperature vs Enthalpy')
plt.legend()
plt.grid(True)
plt.show()

print('dTmin = ', dTmin, 'K at h = ', h[min_index], 'kJ/kg')

# Find T1_prime 

T1_prime = T2 - dTmin
print(f'T1_prime = {T1_prime} K')

#Find the minimum Area of the HX 

Q = 1
LMTD = ((T2-T1_prime)-(T1-T2_prime))/(log((T2-T1_prime)/(T1-T2_prime)))
alpha = 0
U = alpha/2

Area_min = Q/(U*LMTD)

print(f'Area_min = {Area_min} m^2')

#Find the CAPEX of the HX

'''