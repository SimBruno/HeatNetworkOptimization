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

#####
def Dtmin(dT, T1, T2, T2_prime, m1, m2, cp1, cp2, h1, h2):
    
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

# Scenario 1: dTmin for the past5


T1_6 = 333
T2_6 = 348

p1_6 = 100000

m1_6 = 0.48
m2_6 = 0.55

h1_6 = -91021.1032324004*m1_6  #from mixture with dry = 35% and wet = 65%
h2_6 = -38880.66837888083*m2_6

cp1_6 = 3470.44348
cp2_6 = 3482.1944

slope1_6 = 1/(m1_6*cp1_6)
slope2_6 = 1/(m2_6*cp2_6)

#Plot the two lines with T on the y-axis and h on the x-axis
#h is the enthalpy of the stream between h1 and h2
N = 100
h_6 = np.linspace(h1_6, h2_6, N)

C1_6 = T1_6 - slope1_6*h1_6
T1v_6 = slope1_6*h_6 + C1_6

C2_6 = T2_6 - slope2_6*h2_6
T2v_6 = slope2_6*h_6 + C2_6

T2_prime_6 = T2v_6.min()


plt.plot(h_6, T1v_6, label='Cold Stream')
plt.plot(h_6, T2v_6, label='Hot Stream')
plt.xlabel('Enthalpy (J)')
plt.ylabel('Temperature (K)')
plt.title('Temperature vs Enthalpy')
plt.legend()
#Plot as a vertical line the dTmin (i.e. the minimum temperature difference between the two streams)
dt_6 = T2v_6-T1v_6
dTmin_6 = dt_6.min() #This dTmin is not the optimized with respect to TOTEX but just to know the LMTD of HX relation based on if dTmin is left or rigth of the curves 
min_index_6 = dt_6.argmin()
plt.axvline(x=h_6[min_index_6], color='r', linestyle='--')
plt.grid(True)
plt.show()

print('dTmin = ', dTmin_6, 'K at h = ', h_6[min_index_6], 'kJ/kg')


#Redo the CAPEX/OPEX/TOTEX for different dT and plot the results

CAPEXv_6 = []
OPEX_frv_6 = []
OPEX_gerv_6 = []
TOTEX_frv_6 = []
TOTEX_gerv_6 = []
Areav_6 = []

dt_6 = np.linspace(0, 30, 300)

for t in dt_6:
    CAPEX_6, OPEX_fr_6, OPEX_ger_6, TOTEX_fr_6, TOTEX_ger_6, Area_6 = Dtmin(t, T1_6, T2_6, T2_prime_6, m1_6, m2_6, cp1_6, cp2_6, h1_6, h2_6)
    CAPEXv_6.append(CAPEX_6)
    OPEX_frv_6.append(OPEX_fr_6)
    OPEX_gerv_6.append(OPEX_ger_6)
    TOTEX_frv_6.append(TOTEX_fr_6)
    TOTEX_gerv_6.append(TOTEX_ger_6)
    Areav_6.append(Area_6)

#plot the results with respect to the dt values

plt.plot(dt_6, CAPEXv_6, label='CAPEX', linestyle='-', color = 'black')
plt.plot(dt_6, OPEX_frv_6, label='OPEX (France)', linestyle='-', color = 'blue')
plt.plot(dt_6, OPEX_gerv_6, label='OPEX (Germany)', linestyle='-', color = 'red')
plt.plot(dt_6, TOTEX_frv_6, label='TOTEX (France)',linestyle='--', color = 'blue')
plt.plot(dt_6, TOTEX_gerv_6, label='TOTEX (Germany)', linestyle='--', color = 'red')
plt.xlabel('dTmin (K)')
plt.ylabel('Costs (€)')
plt.title('Costs vs dTmin')
plt.legend()
plt.grid(True)

min_index_fr_6 = np.argmin(TOTEX_frv_6)
plt.plot(dt_6[min_index_fr_6], TOTEX_frv_6[min_index_fr_6], 'bo')
min_index_ger_6 = np.argmin(TOTEX_gerv_6)
plt.plot(dt_6[min_index_ger_6], TOTEX_gerv_6[min_index_ger_6], 'ro')

#print the area, dt, CAPEX, OPEX, TOTEX for the minimum TOTEX

dtmin_opt_6 = dt_6[min_index_fr_6]
area_opt_6 = Areav_6[min_index_fr_6]
CAPEX_opt_6 = CAPEXv_6[min_index_fr_6]
OPEX_fr_opt_6 = OPEX_frv_6[min_index_fr_6]
OPEX_ger_opt_6 = OPEX_gerv_6[min_index_fr_6]
TOTEX_fr_opt_6 = TOTEX_frv_6[min_index_fr_6]
TOTEX_ger_opt_6 = TOTEX_gerv_6[min_index_fr_6]
Past6_opt = pd.DataFrame({'dTmin [K]': dtmin_opt_6, 'Area [m^2]': area_opt_6, 'CAPEX[€/yr]': CAPEX_opt_6, 'OPEX_fr[€/yr]': OPEX_fr_opt_6, 'OPEX_ger[€/yr]': OPEX_ger_opt_6, 'TOTEX_fr[€/yr]': TOTEX_fr_opt_6, 'TOTEX_ger[€/yr]': TOTEX_ger_opt_6}, index=[0])
plt.show()


# Scenario 2: dTmin for the past1+past6

#PAST1 


T1_1 = 277
T1_prime_1 = 333

#This time we know only T_cin and T_cout but nothing about the hot streams
#We can't reuse the exact same method as for past6 where we knew T_hin and T_cin

#We assume dTmin is on the left of the curves.
#We will thus have dTmin = T_cout - T_hin which gives two unkowns dTmin and T_cout
#We will solve 



p1_1 = 100000

m1_1 = 8
m2_1 = 7.52

h1_1 = -84420.13*m1_1   #from mixture function with dry = 11.7% and wet = 88.3%
h2_1 = -18059.7680*m2_1

cp1_1 = 3963.18
cp2_1 = 3941.70

slope1_1 = 1/(m1_1*cp1_1)
slope2_1 = 1/(m2_1*cp2_1)

#Plot the two lines with T on the y-axis and h on the x-axis
#h is the enthalpy of the stream between h1 and h2
N = 100
h_1 = np.linspace(h1_1, h2_1, N)

C1_1 = T1_1 - slope1_1*h1_1
T1v_1 = slope1_1*h_1 + C1_1

C2_1 = T2_1 - slope2_1*h2_1
T2v_1 = slope2_1*h_1 + C2_1

T2_prime_1 = T2v_1.min()

plt.plot(h_1, T1v_1, label='Cold Stream')
plt.plot(h_1, T2v_1, label='Hot Stream')
plt.xlabel('Enthalpy (J)')
plt.ylabel('Temperature (K)')
plt.title('Temperature vs Enthalpy')
plt.legend()
#Plot as a vertical line the dTmin (i.e. the minimum temperature difference between the two streams)
dt_1 = T2v_1-T1v_1
dTmin_1 = dt_1.min()   
min_index_1 = dt_1.argmin()
plt.axvline(x=h_1[min_index_1], color='r', linestyle='--')
plt.grid(True)
plt.show()

print('dTmin = ', dTmin_1, 'K at h = ', h_1[min_index_1], 'kJ/kg')
