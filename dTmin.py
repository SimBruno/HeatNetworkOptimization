#The goal of this part is to determine an optimized dTmin such that costs are minimized. 
#In all scenarios we will do the following:
#1. Determine the area of the HX in term of the dTmin
#2. Determine the cost of the HX in term of the the Area
#3. Determine the cost of the HX in term of the dTmin

# ##Scenario 1: dTmin for the past5 

# ### Determine the area of the HX in term of the dTmin

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
#from codes_01_energy_bill.coolprop_functions import mixture



T1 = 333
T2 = 348

p1 = 100000

m1 = 0.48
m2 = 0.55

h1 = -91021.1032324004*m1  #from mixture with dry = 35% and wet = 65%
h2 = -38880.66837888083*m2

cp1 = 3470.44348
cp2 = 3482.1944

slope1 = 1/(m1*cp1)
slope2 = 1/(m2*cp2)

#Plot the two lines with T on the y-axis and h on the x-axis
#h is the enthalpy of the stream between h1 and h2
N = 100
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

def DTMIN(dT, T1, T2, m1, m2, cp1, cp2, h1, h2):

    T1_prime = T2 - dT

    #Find the minimum Area of the HX
    Q = m2*cp2*(T2-T2_prime)
    alpha= 1000 #W/m^2°C, assumption based on alpha_H20 since 65wt% of the stream is water 
    U = alpha/2
    dtA = abs(T2-T1_prime)  # to be sure we have a positive value in the ln() of the LMTD
    dtB = abs(T1-T2_prime)
    LMTD = (dtA-dtB)/np.log(dtA/dtB)
    Area = Q/(U*LMTD)
    #Find the CAPEX

    CEPCI2019=603.1 
    CEPCI1998=389.5 #https://personalpages.manchester.ac.uk/staff/tom.rodgers/Interactive_graphs/CEPCI.html?reactors/CEPCI/index.html
    K1=3.6788 #sl 12 T4.1 assumption flat plate HX
    K2=0.4412
    FBM=4.74 #assumption fluid sl 10 T4.1
    i=0.05 #sl 8 T4.2
    e=0.92 #€/$ exchange rate 2023 Nov 
    n=20

    Cp = CEPCI2019/CEPCI1998 * 10**(K1+K2*np.log(Area))

    CBM = Cp*FBM*e

    ANNUALIZATIONFACTOR = (i*(1+i)**n)/((1+i)**n-1)

    CAPEX = ANNUALIZATIONFACTOR*CBM

    #Find the OPEX
    top = 24*0.95*365 #h/year
    gas_fr = 0.08 # €/kWh
    gas_ger = 0.08 # €/kWh 
    elec_fr = 0.12 # €/kWh
    elec_ger = 0.21 # €/kWh
    COP = 3.5 #same assumption in Energy Bill

    Qpast6 = m2*cp2*(T2-T1_prime)
    OP6_fr = gas_fr * Qpast6/1000 * top
    OP6_ger = gas_ger * Qpast6/1000 * top

    Qpast7 = m2*cp2*(T2_prime-277)  #T7 = 4°C = 277K
    Wpast7 = Qpast7/COP

    OP7_fr = elec_fr * Wpast7/1000 * top  
    OP7_ger = elec_ger * Wpast7/1000 * top 

    OPEX_fr = OP6_fr + OP7_fr
    OPEX_ger = OP6_ger + OP7_ger

    #Find the TOTEX
    TOTEX_fr = CAPEX + OPEX_fr
    TOTEX_ger = CAPEX + OPEX_ger

    return CAPEX, OPEX_fr, OPEX_ger, TOTEX_fr, TOTEX_ger, Area

#Redo the CAPEX/OPEX/TOTEX for different dT and plot the results

CAPEXv = []
OPEX_frv = []
OPEX_gerv = []
TOTEX_frv = []
TOTEX_gerv = []
Areav = []

dt = np.linspace(0, 30, 300)

for t in dt:
    CAPEX, OPEX_fr, OPEX_ger, TOTEX_fr, TOTEX_ger, Area = DTMIN(t, T1, T2, m1, m2, cp1, cp2, h1, h2)
    CAPEXv.append(CAPEX)
    OPEX_frv.append(OPEX_fr)
    OPEX_gerv.append(OPEX_ger)
    TOTEX_frv.append(TOTEX_fr)
    TOTEX_gerv.append(TOTEX_ger)
    Areav.append(Area)

#plot the results with respect to the dt values

plt.plot(dt, CAPEXv, label='CAPEX', linestyle='-', color = 'black')
plt.plot(dt, OPEX_frv, label='OPEX (France)', linestyle='-', color = 'blue')
plt.plot(dt, OPEX_gerv, label='OPEX (Germany)', linestyle='-', color = 'red')
plt.plot(dt, TOTEX_frv, label='TOTEX (France)',linestyle='--', color = 'blue')
plt.plot(dt, TOTEX_gerv, label='TOTEX (Germany)', linestyle='--', color = 'red')
plt.xlabel('dTmin (K)')
plt.ylabel('Costs (€)')
plt.title('Costs vs dTmin')
plt.legend()
plt.grid(True)

min_index_fr = np.argmin(TOTEX_frv)
plt.plot(dt[min_index_fr], TOTEX_frv[min_index_fr], 'bo')
min_index_ger = np.argmin(TOTEX_gerv)
plt.plot(dt[min_index_ger], TOTEX_gerv[min_index_ger], 'ro')

#print the area, dt, CAPEX, OPEX, TOTEX for the minimum TOTEX

dtmin_opt = dt[min_index_fr]
area_opt = Areav[min_index_fr]
CAPEX_opt = CAPEXv[min_index_fr]
OPEX_fr_opt = OPEX_frv[min_index_fr]
OPEX_ger_opt = OPEX_gerv[min_index_fr]
TOTEX_fr_opt = TOTEX_frv[min_index_fr]
TOTEX_ger_opt = TOTEX_gerv[min_index_fr]

recap = pd.DataFrame({'dTmin [K]': dtmin_opt, 'Area [m^2]': area_opt, 'CAPEX[€/yr]': CAPEX_opt, 'OPEX_fr[€/yr]': OPEX_fr_opt, 'OPEX_ger[€/yr]': OPEX_ger_opt, 'TOTEX_fr[€/yr]': TOTEX_fr_opt, 'TOTEX_ger[€/yr]': TOTEX_ger_opt}, index=[0])
print(recap)



plt.show()

#PAST1 


T1_1 = 277
T2_1 = 293.8

p1_1 = 100000

m1_1 = 8
m2_1 = 7.52

h1 = -91021.1032324004*m1   #from mixture function with dry = 11.7% and wet = 88.3%
h2 = -38880.66837888083*m2

cp1 = 3470.44348
cp2 = 3482.1944

slope1 = 1/(m1*cp1)
slope2 = 1/(m2*cp2)

#Plot the two lines with T on the y-axis and h on the x-axis
#h is the enthalpy of the stream between h1 and h2
N = 100
h = np.linspace(h1, h2, N)

C1 = T1 - slope1*h1
T1v = slope1*h + C1

C2 = T2 - slope2*h2
T2v = slope2*h + C2

T2_prime = T2v.min()


