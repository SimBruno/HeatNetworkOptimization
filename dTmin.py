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
def Dtmin(dT, T1, T1v, T2, T2_prime, m2, cp2, position, pastnb):
    
    if position == 'left':
        T1_prime = T2 - dT
    elif position == 'right':
        T1_prime = T1v.max()
    
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

    if pastnb == 5:
        Qpast6 = m2*cp2*(T2-T1_prime)
        OP6_fr = gas_fr * Qpast6/1000 * top
        OP6_ger = gas_ger * Qpast6/1000 * top

        Qpast7 = m2*cp2*(T2_prime-277)  #T7 = 4°C = 277K
        Wpast7 = Qpast7/COP

        OP7_fr = elec_fr * Wpast7/1000 * top  
        OP7_ger = elec_ger * Wpast7/1000 * top 

        OPEX_fr = OP6_fr + OP7_fr
        OPEX_ger = OP6_ger + OP7_ger

    elif pastnb == 1:
        Qpast2 = m2*cp2*(348-T2)
        OP2_fr = gas_fr * Qpast2/1000 * top
        OP2_ger = gas_ger * Qpast2/1000 * top

        #Qpast 3 is neglect since the difference temepreature is not that high anymore

        Qpast4 = m2*cp2*(T2_prime-277)  #T7 = 4°C = 277K
        Wpast4 = Qpast4/COP

        OP4_fr = elec_fr * Wpast4/1000 * top  
        OP4_ger = elec_ger * Wpast4/1000 * top 

        OPEX_fr = OP2_fr + OP4_fr
        OPEX_ger = OP2_ger + OP4_ger

    #Find the TOTEX
    TOTEX_fr = CAPEX + OPEX_fr
    TOTEX_ger = CAPEX + OPEX_ger

    return CAPEX, OPEX_fr, OPEX_ger, TOTEX_fr, TOTEX_ger, Area

# Scenario 1: dTmin for the past5

#In our code 1 stands for cold stream and 2 for hot stream. 
#When we have a T#number it is related to the entrance of te stream and _prime relate to the exiting
#The _Number stands for the past number
#T2_prime_2 stands for the T_hout of the past2 HX

T1_5 = 333
T2_5 = 348

p1_5 = 100000

m1_5 = 0.48
m2_5 = 0.55

h1_5 = -91021.1032324004*m1_5  #from mixture with dry = 35% and wet = 65%
h2_5 = -38880.66837888083*m2_5

cp1_5 = 3470.44348
cp2_5 = 3482.1944

slope1_5 = 1/(m1_5*cp1_5)
slope2_5 = 1/(m2_5*cp2_5)

#Plot the two lines with T on the y-axis and h on the x-axis
#h is the enthalpy of the stream between h1 and h2
N = 100
h_5 = np.linspace(h1_5, h2_5, N)

C1_5 = T1_5 - slope1_5*h1_5
T1v_5 = slope1_5*h_5 + C1_5

C2_5 = T2_5 - slope2_5*h2_5
T2v_5 = slope2_5*h_5 + C2_5

T2_prime_5 = T2v_5.min()

plt.plot(h_5, T1v_5, label='Cold Stream')
plt.plot(h_5, T2v_5, label='Hot Stream')
plt.xlabel('Enthalpy (J)')
plt.ylabel('Temperature (K)')
plt.title('Temperature vs Enthalpy')
plt.legend()
#Plot as a vertical line the dTmin (i.e. the minimum temperature difference between the two streams)
dt_5 = T2v_5-T1v_5
dTmin_5 = dt_5.min() #This dTmin is not the optimized with respect to TOTEX but just to know the LMTD of HX relation based on if dTmin is left or rigth of the curves 
min_index_5 = dt_5.argmin()
plt.axvline(x=h_5[min_index_5], color='r', linestyle='--')
plt.grid(True)
plt.show()

print('dTmin = ', dTmin_5, 'K at h = ', h_5[min_index_5], 'kJ/kg')


#Redo the CAPEX/OPEX/TOTEX for different dT and plot the results

CAPEXv_5 = []
OPEX_frv_5 = []
OPEX_gerv_5 = []
TOTEX_frv_5 = []
TOTEX_gerv_5 = []
Areav_5 = []

dt_5 = np.linspace(0, 30, 300)

for t in dt_5:
    CAPEX_5, OPEX_fr_5, OPEX_ger_5, TOTEX_fr_5, TOTEX_ger_5, Area_5 = Dtmin(t, T1_5, T1v_5, T2_5, T2_prime_5, m2_5, cp2_5, 'left', 5)
    CAPEXv_5.append(CAPEX_5)
    OPEX_frv_5.append(OPEX_fr_5)
    OPEX_gerv_5.append(OPEX_ger_5)
    TOTEX_frv_5.append(TOTEX_fr_5)
    TOTEX_gerv_5.append(TOTEX_ger_5)
    Areav_5.append(Area_5)

#plot the results with respect to the dt values

plt.plot(dt_5, CAPEXv_5, label='CAPEX', linestyle='-', color = 'black')
plt.plot(dt_5, OPEX_frv_5, label='OPEX (France)', linestyle='-', color = 'blue')
plt.plot(dt_5, OPEX_gerv_5, label='OPEX (Germany)', linestyle='-', color = 'red')
plt.plot(dt_5, TOTEX_frv_5, label='TOTEX (France)',linestyle='--', color = 'blue')
plt.plot(dt_5, TOTEX_gerv_5, label='TOTEX (Germany)', linestyle='--', color = 'red')
plt.xlabel('dTmin (K)')
plt.ylabel('Costs (€)')
plt.title('Costs vs dTmin')
plt.legend()
plt.grid(True)

min_index_fr_5 = np.argmin(TOTEX_frv_5)
plt.plot(dt_5[min_index_fr_5], TOTEX_frv_5[min_index_fr_5], 'bo')
min_index_ger_5 = np.argmin(TOTEX_gerv_5)
plt.plot(dt_5[min_index_ger_5], TOTEX_gerv_5[min_index_ger_5], 'ro')
plt.show()
#print the area, dt, CAPEX, OPEX, TOTEX for the minimum TOTEX

dtmin_opt_5 = dt_5[min_index_fr_5]
area_opt_5 = Areav_5[min_index_fr_5]
CAPEX_opt_5 = CAPEXv_5[min_index_fr_5]
OPEX_fr_opt_5 = OPEX_frv_5[min_index_fr_5]
OPEX_ger_opt_5 = OPEX_gerv_5[min_index_fr_5]
TOTEX_fr_opt_5 = TOTEX_frv_5[min_index_fr_5]
TOTEX_ger_opt_5 = TOTEX_gerv_5[min_index_fr_5]
Past5_opt = pd.DataFrame({'dTmin [K]': dtmin_opt_5, 'Area [m^2]': area_opt_5, 'CAPEX[€/yr]': CAPEX_opt_5, 'OPEX_fr[€/yr]': OPEX_fr_opt_5, 'OPEX_ger[€/yr]': OPEX_ger_opt_5, 'TOTEX_fr[€/yr]': TOTEX_fr_opt_5, 'TOTEX_ger[€/yr]': TOTEX_ger_opt_5}, index=[0])



# Scenario 2: dTmin for the past1+past6

#This time we know only T_cin and T_cout but nothing about the hot streams
#We can't reuse the exact same method as for past6 where we knew T_hin and T_cin
#We will first determine T_cin from the Past2 HX on which we can reuse the same method as for past6

# PAST2 Intermediate HX to determine T_cin

T1_2 = 333
T2_2 = 348

p1_2 = 100000

m1_2 = 7.52
m2_2 = 7.52

h1_2 = 136414.15*m1_2  #from mixture with dry = 11.7% and wet = 88.3%
h2_2 = 195671.23*m2_2

cp1_2 = 3946.06
cp2_2 = 3955.46

#mcp_cold < mcp_hot verified

slope1_2 = 1/(m1_2*cp1_2)
slope2_2 = 1/(m2_2*cp2_2)

#Plot the two lines with T on the y-axis and h on the x-axis
#h is the enthalpy of the stream between h1 and h2
N = 100
h_2 = np.linspace(h1_5, h2_5, N)

C1_2 = T1_2 - slope1_2*h1_2
T1v_2 = slope1_2*h_2 + C1_2

C2_2 = T2_2 - slope2_2*h2_2
T2v_2 = slope2_2*h_2 + C2_2

T2_prime_2 = T2v_2.min()  #This value is T_hout and will be our T_hin for the past1
print('T2_prime_2 = ', T2_prime_2)
#Check the T_cout to be sure it is coherent 
dt_2 = T2v_2-T1v_2
dTmin_2 = dt_2.min()
T1_prime_2 = T2_2 - dTmin_2 
print(T1_prime_2) #WEIRD Results (T1_prime_2 almost = 75°C which would make the PAST3 irrelevant)

# PAST1 

T1_1 = 277
T2_1 = T2_prime_2

p1_1 = 100000

m1_1 = 8
m2_1 = 7.52

h1_1 = -84420.13*m1_1   #from mixture function with dry = 11.7% and wet = 88.3%
h2_1 = -18059.7680*m2_1


cp1_1 = 3963.18
cp2_1 = 3941.70

#This time mcp_cold > mcp_hot --> HOW TO DO ??? Assume I didn't see it and do the same as for past6

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

#This time the the dTmin is on the left of the curves and thus dTmin = T_hout-T_cin (instead of T_hin-Tcout as in past6)

#Redo the CAPEX/OPEX/TOTEX for different dT and plot the results

CAPEXv_1 = []
OPEX_frv_1 = []
OPEX_gerv_1 = []
TOTEX_frv_1 = []
TOTEX_gerv_1 = []
Areav_1 = []

dt_1 = np.linspace(0, 30, 300)

for t in dt_1:
    CAPEX_1, OPEX_fr_1, OPEX_ger_1, TOTEX_fr_1, TOTEX_ger_1, Area_1 = Dtmin(t, T1_1, T1v_1, T2_1, T2_prime_1, m2_1, cp2_1, 'right', 1)
    CAPEXv_1.append(CAPEX_1)
    OPEX_frv_1.append(OPEX_fr_1)
    OPEX_gerv_1.append(OPEX_ger_1)
    TOTEX_frv_1.append(TOTEX_fr_1)
    TOTEX_gerv_1.append(TOTEX_ger_1)
    Areav_1.append(Area_1)

'''
#plot the results with respect to the dt values

plt.plot(dt_1, CAPEXv_1, label='CAPEX', linestyle='-', color = 'black')
plt.plot(dt_1, OPEX_frv_1, label='OPEX (France)', linestyle='-', color = 'blue')
plt.plot(dt_1, OPEX_gerv_1, label='OPEX (Germany)', linestyle='-', color = 'red')
plt.plot(dt_1, TOTEX_frv_1, label='TOTEX (France)',linestyle='--', color = 'blue')
plt.plot(dt_1, TOTEX_gerv_1, label='TOTEX (Germany)', linestyle='--', color = 'red')
plt.xlabel('dTmin (K)')
plt.ylabel('Costs (€)')
plt.title('Costs vs dTmin')
plt.legend()
plt.grid(True)
'''

min_index_fr_1 = np.argmin(TOTEX_frv_1)
#plt.plot(dt_1[min_index_fr_1], TOTEX_frv_1[min_index_fr_1], 'bo')
min_index_ger_1 = np.argmin(TOTEX_gerv_1)
#plt.plot(dt_1[min_index_ger_1], TOTEX_gerv_1[min_index_ger_1], 'ro')
#plt.show()


dtmin_opt_1 = dt_1[min_index_fr_1]
area_opt_1 = Areav_1[min_index_fr_1]
CAPEX_opt_1 = CAPEXv_1[min_index_fr_1]
OPEX_fr_opt_1 = OPEX_frv_1[min_index_fr_1]
OPEX_ger_opt_1 = OPEX_gerv_1[min_index_fr_1]
TOTEX_fr_opt_1 = TOTEX_frv_1[min_index_fr_1]
TOTEX_ger_opt_1 = TOTEX_gerv_1[min_index_fr_1]
Past6_opt = pd.DataFrame({'dTmin [K]': dtmin_opt_1, 'Area [m^2]': area_opt_1, 'CAPEX[€/yr]': CAPEX_opt_1, 'OPEX_fr[€/yr]': OPEX_fr_opt_1, 'OPEX_ger[€/yr]': OPEX_ger_opt_1, 'TOTEX_fr[€/yr]': TOTEX_fr_opt_1, 'TOTEX_ger[€/yr]': TOTEX_ger_opt_1}, index=[0])


#plot the results with respect to the dt values

dt_15 = np.linspace(0, 30, 300)
CAPEXv_15 = []
OPEX_frv_15 = []
OPEX_gerv_15 = []
TOTEX_frv_15 = []
TOTEX_gerv_15 = []

for i in range(0, len(dt_15)):
    CAPEXv_15.append(CAPEXv_1[i] + CAPEXv_5[i])
    OPEX_frv_15.append(OPEX_frv_1[i] + OPEX_frv_5[i])
    OPEX_gerv_15.append(OPEX_gerv_1[i] + OPEX_gerv_5[i])
    TOTEX_frv_15.append(TOTEX_frv_1[i] + TOTEX_frv_5[i])
    TOTEX_gerv_15.append(TOTEX_gerv_1[i] + TOTEX_gerv_5[i])



plt.plot(dt_15, CAPEXv_15, label='CAPEX', linestyle='-', color = 'black')
plt.plot(dt_15, OPEX_frv_15, label='OPEX (France)', linestyle='-', color = 'blue')
plt.plot(dt_15, OPEX_gerv_15, label='OPEX (Germany)', linestyle='-', color = 'red')
plt.plot(dt_15, TOTEX_frv_15, label='TOTEX (France)',linestyle='--', color = 'blue')
plt.plot(dt_15, TOTEX_gerv_15, label='TOTEX (Germany)', linestyle='--', color = 'red')
plt.xlabel('dTmin (K)')
plt.ylabel('Costs (€)')
plt.title('Costs vs dTmin')
plt.legend()
plt.grid(True)
min_index_fr_15 = np.argmin(TOTEX_frv_15)
plt.plot(dt_15[min_index_fr_15], TOTEX_frv_1[min_index_fr_15], 'bo')
min_index_ger_15 = np.argmin(TOTEX_gerv_15)
plt.plot(dt_15[min_index_ger_15], TOTEX_gerv_15[min_index_ger_15], 'ro')

## Combining PAST1 and PAST5
dtmin_opt_15 = dtmin_opt_1 + dtmin_opt_5
area_opt_15 = area_opt_1 + area_opt_5
CAPEX_opt_15 = CAPEX_opt_1 + CAPEX_opt_5
OPEX_fr_opt_15 = OPEX_fr_opt_1 + OPEX_fr_opt_5
OPEX_ger_opt_15 = OPEX_ger_opt_1 + OPEX_ger_opt_5
TOTEX_fr_opt_15 = TOTEX_fr_opt_1 + TOTEX_fr_opt_5
TOTEX_ger_opt_15 = TOTEX_ger_opt_1 + TOTEX_ger_opt_5
Past15_opt = pd.DataFrame({'dTmin [K]': dtmin_opt_15, 'Area [m^2]': area_opt_15, 'CAPEX[€/yr]': CAPEX_opt_15, 'OPEX_fr[€/yr]': OPEX_fr_opt_15, 'OPEX_ger[€/yr]': OPEX_ger_opt_15, 'TOTEX_fr[€/yr]': TOTEX_fr_opt_15, 'TOTEX_ger[€/yr]': TOTEX_ger_opt_15}, index=[0])
print(Past15_opt)
plt.show()