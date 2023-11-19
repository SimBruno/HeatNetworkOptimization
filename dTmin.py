#The goal of this part is to determine an optimized dTmin such that costs are minimized. 
#In all scenarios we will do the following:
#1. Determine the area of the HX in term of the dTmin
#2. Determine the cost of the HX in term of the the Area
#3. Determine the cost of the HX in term of the dTmin

# ##Scenario 1: dTmin for the past5 

# ### Determine the area of the HX in term of the dTmin

import numpy as np
import matplotlib.pyplot as plt

T1 = 333
T2 = 348

p1 = 100000

m1 = 0.48
m2 = 0.55

h1 = -91021.1032324004*m1
h2 = -38880.66837888083*m2

cp1 = 3470.44348
cp2 = 3482.1944

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

plt.plot(h, T1v, label='Cold Stream')
plt.plot(h, T2v, label='Hot Stream')
plt.xlabel('Enthalpy (J)')
plt.ylabel('Temperature (K)')
plt.title('Temperature vs Enthalpy')
plt.legend()
plt.grid(True)
plt.show()

#
Q=0
alpha=0
U = alpha/2
dTmin = 0


