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

C1 = T1 - slope1*h1
T1v = slope1*h + C1

C2 = T2 - slope2*h2
T2v = slope2*h + C2

T2_prime = T2v.min()


plt.plot(h, T1v, label='Cold Stream')
plt.plot(h, T2v, label='Hot Stream')
plt.xlabel('Enthalpy (J)')
plt.ylabel('Temperature (K)')
plt.title('Temperature vs Enthalpy')
plt.legend()
#Plot as a vertical line the dTmin (i.e. the minimum temperature difference between the two streams)
dt = T2v-T1v
dTmin = dt.min()
min_index = dt.argmin()
plt.axvline(x=h[min_index], color='r', linestyle='--')
plt.grid(True)
plt.show()

print('dTmin = ', dTmin, 'K at h = ', h[min_index], 'kJ/kg')


#Find T1_prime

T1_prime = T2 - dTmin
print(f'T1_prime = {T1_prime} K')

#Find the minimum Area of the HX
Q = m2*cp2*(T2-T2_prime)
print(f'Q = {Q} W')
alpha= 1000 #W/m^2°C, assumption based on alpha_H20 since 65wt% of the stream is water 
U = alpha/2
dtA = abs(T2-T1_prime)  ####CHECK IF ABS IS NEEEDDDEEDEDED
dtB = abs(T1-T2_prime)
LMTD = (dtA-dtB)/np.log(dtA/dtB)
print(f'LMTD = {LMTD} K')
Area = Q/(U*LMTD)
print(f'Area = {Area} m^2')

#Find the CAPEX

CEPCI2019=603.1 
CEPCI1998=389.5 #https://personalpages.manchester.ac.uk/staff/tom.rodgers/Interactive_graphs/CEPCI.html?reactors/CEPCI/index.html
K1=3.8528  #sl 12 T4.1 assumption flat plate HX
K2=0.4242
FBM=4.74 #assumption fluid sl 10 T4.1
i=0.09 #sl 8 T4.2
e=0.92 #€/$ exchange rate 2023 Nov 
n=10

Cp = CEPCI2019/CEPCI1998 * 10**(K1+K2*np.log(Area))

CBM = Cp*FBM*e

ANNUALIZATIONFACTOR = (i*(1+i)**n)/((1+i)**n-1)

CAPEX = ANNUALIZATIONFACTOR*CBM
print(f'CAPEX = {CAPEX} €')


#Find the OPEX
top = 24*0.95*365 #h/year
gas_fr = 0.08 # €/kWh
gas_ger = 0.08 # €/kWh 
elec_fr = 0.12 # €/kWh
elec_ger = 0.21 # €/kWh
COP = 3.5
#c_water = 

Qpast6 = m2*cp2*(T2-T1_prime)
OP6_fr = gas_fr * Qpast6/1000 * top
OP6_ger = gas_ger * Qpast6/1000 * top

Qpast7 = m2*cp2*(T2_prime-277)  #T7 = 4°C = 277K
Wpast7 = Qpast7/COP
#Qwater = Qpast7 + Wpast7  #WTFWTFWTFWTFWTWTFWTFWTFWTWTWFTW
#mwater = Qwater/(4180)

OP7_fr = elec_fr * Wpast7/1000 * top  
OP7_ger = elec_ger * Wpast7/1000 * top 

OPEX_fr = OP6_fr + OP7_fr
OPEX_ger = OP6_ger + OP7_ger

print(f'OPEX_fr = {OPEX_fr} €')
print(f'OPEX_ger = {OPEX_ger} €')


#Find the TOTEX
TOTEX_fr = CAPEX + OPEX_fr
TOTEX_ger = CAPEX + OPEX_ger


#Redo the CAPEX/OPEX/TOTEX for different dT and plot the results




