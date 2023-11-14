#The goal of this part is to determine an optimized dTmin such that costs are minimized. 
#In all scenarios we will do the following:
#1. Determine the area of the HX in term of the dTmin
#2. Determine the cost of the HX in term of the the Area
#3. Determine the cost of the HX in term of the dTmin

# ##Scenario 1: dTmin for the past5 

# ### Determine the area of the HX in term of the dTmin

import numpy as np
import matplotlib.pyplot as plt

T1=333
T2=348

m1=0.48
m2=0.55
cp1=3400
cp2=2976.18181818181


slope1 = 1/(m1*cp1)
slope2 = 1/(m2*cp2)

#Plot the two lines with T on the y-axis and h on the x-axis
#h is the enthalpy of the stream between 1 and 1000 kJ/kg
N=1000000
h = np.linspace(1,N,N)

T1v = slope1*h + T1
T_2 = T2 - slope2*N
T2v = slope2*h + T_2

plt.plot(h, T1v)
plt.plot(h, T2v)
plt.xlabel('Enthalpy (kJ/kg)')
plt.ylabel('Temperature (K)')
plt.title('Temperature vs Enthalpy')
plt.show()
print(slope1)
print(slope2)



#
Q=0
alpha=0
U = alpha/2
dTmin = 0


