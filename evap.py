
import pandas as pd
import numpy as np

m1=5.0
m6=m1
m14=1.6
m15=1.28
m16=0.8



def fat_increase(m_int1, m_int2, m_int3, m_in = 5.0, p_fat_out3 = 0.50):
    m_out = m_in - m_int1 - m_int2 - m_int3
    if m_out < 0:
        print("ERROR: The mass of the output is negative.")
    # OUT 3
    p_water_out3 = 1 - p_fat_out3
    m_water_out3 = m_out * p_water_out3
    m_fat = m_out * p_fat_out3
    # OUT 2
    m_water_out2 = m_water_out3 + m_int3
    m_tot_2 = m_water_out2 + m_fat
    p_fat_out2 = m_fat / m_tot_2
    p_water_out2 = 1 - p_fat_out2
    # OUT 1
    m_water_out1 = m_water_out2 + m_int2
    m_tot_1 = m_water_out1 + m_fat
    p_fat_out1 = m_fat / m_tot_1
    p_water_out1 = 1 - p_fat_out1
    # OUT 0
    m_water_out0 = m_water_out1 + m_int1
    m_tot_0 = m_water_out0 + m_fat
    p_fat_out0 = m_fat / m_tot_0
    p_water_out0 = 1 - p_fat_out0
    if p_water_out0 > 0.883:
        print("WARNING: The water content in the final product is too high.")
    return m_out, p_fat_out0, p_fat_out1, p_fat_out2, p_fat_out3, p_water_out0, p_water_out1, p_water_out2, p_water_out3

m11, p_fat_out0, p_fat_out1, p_fat_out2, p_fat_out3, p_water_out0, p_water_out1, p_water_out2, p_water_out3 = fat_increase(m_int1=m14, m_int2=m15, m_int3=m16, m_in = m6, p_fat_out3 = 0.5)


data = {'Point': ['6', '7&8', '9&10', '11'],
        'Fat content (%)': [p_fat_out0*100, p_fat_out1*100, p_fat_out2*100, p_fat_out3*100],
        'Water content (%)': [p_water_out0*100, p_water_out1*100, p_water_out2*100, p_water_out3*100]}
df = pd.DataFrame(data)
df = df.set_index('Point')
df = df.round(2)
print(df)

#Evaporator 1
from codes_01_energy_bill.coolprop_functions import mixture
from pyxosmose.state import State
def evaporator_fct(m_in,m_out1,m_out2,h_in,h_out1,h_out2,cp_in,deltaT,hfg):
    Q_evap = m_in*cp_in*deltaT - m_in*h_in + m_out1*h_out1 + m_out2*h_out2
    m_w = (Q_evap)/(hfg)
    print('Qevap:',Q_evap)
    print('mw:',m_w)
    return Q_evap, m_w
#Fixed Parameters 
p6=31000
p7=p6
p14=p6
p24=100000

T6=343
T7=T6
T14=343
T24=373 #can be changed if needed to reduce cost instead of having a high pressure

#Dependent Parameters
State_e6=mixture(T=T6, P=p6, frac_water=p_water_out0, frac_fat=p_fat_out0) # this is a dictionary!!
print(State_e6)
h6=State_e6["enthalpy"]
cp6=State_e6["cpmass"]


State_e7=mixture(T=T7, P=p7, frac_water=p_water_out1, frac_fat=p_fat_out1) # this is a dictionary!!
print(State_e7)
h7=State_e7["enthalpy"]

Point_e14 = State(pair='TP', fluid='water', temperature=T14, pressure=p14)
# Then calculate the state using the State class method StateCalc
Point_e14.StateCalc()
# And print the dictionary for revision
State_e14 = Point_e14.__dict__ # Whole dictionary with properties
h14=State_e14["enthalpy"]
print(h14)


Point_e24 = State(pair='TP', fluid='water', temperature=T24, pressure=p24)
# Then calculate the state using the State class method StateCalc
Point_e24.StateCalc()
# And print the dictionary for revision
State_e24 = Point_e24.__dict__ # Whole dictionary with properties
hfg1=State_e24["enthalpy"]
print(hfg1)


#Evap 1 calculation of heat 
m7=m6-m14
deltaT=5

Q_evap1, m_w1 = evaporator_fct(m6,m14,m7,h6,h14,h7,cp6,deltaT,hfg1)

print(Q_evap1)
print(m_w1)

#Evaporator 2

from codes_01_energy_bill.coolprop_functions import mixture

p8=25000
p9=p8
p15=25000
p17=p14

T8=338
T9=T8
T15=338
T17=T14

State_e8=mixture(T=T8, P=p8, frac_water=p_water_out2, frac_fat=p_fat_out2) # this is a dictionary!!
print(State_e8)
h8=State_e8["enthalpy"]
cp8=State_e8["cpmass"]

State_e9=mixture(T=T9, P=p9, frac_water=p_water_out2, frac_fat=p_fat_out2) # this is a dictionary!!
print(State_e9)
h9=State_e9["enthalpy"]

Point_e15 = State(pair='TP', fluid='water', temperature=T15, pressure=p15)
# Then calculate the state using the State class method StateCalc
Point_e15.StateCalc()
# And print the dictionary for revision
State_e15 = Point_e15.__dict__ # Whole dictionary with properties
h15=State_e15["enthalpy"]
print(h15)

Point_e17 = State(pair='TP', fluid='water', temperature=T17, pressure=p17)
# Then calculate the state using the State class method StateCalc
Point_e17.StateCalc()
# And print the dictionary for revision
State_e17 = Point_e17.__dict__ # Whole dictionary with properties
hfg2=State_e17["enthalpy"]
print(hfg2)

m8=m7
m9=m8-m15
deltaT=5

Q_evap2, m_w2 = evaporator_fct(m8,m15,m9,h8,h15,h9,cp8,deltaT,hfg2)

print(Q_evap2)
print(m_w2)

#Evaporator 3

from codes_01_energy_bill.coolprop_functions import mixture


p10=20000
p11=p10
p15=25000
p18=p15
p16=20000


T10=333
T11=T10
T15=338
T18=T15
T16=333

State_e10=mixture(T=T10, P=p10, frac_water=p_water_out2, frac_fat=p_fat_out2) # this is a dictionary!!
print(State_e10)
h10=State_e10["enthalpy"]
cp10=State_e10["cpmass"]

State_e11=mixture(T=T11, P=p11, frac_water=p_water_out3, frac_fat=p_fat_out3) # this is a dictionary!!
print(State_e11)
h11=State_e11["enthalpy"]

Point_e16 = State(pair='TP', fluid='water', temperature=T16, pressure=p16)
# Then calculate the state using the State class method StateCalc
Point_e16.StateCalc()
# And print the dictionary for revision
State_e16 = Point_e16.__dict__ # Whole dictionary with properties
h16=State_e16["enthalpy"]
print(h16)

Point_e18 = State(pair='TP', fluid='water', temperature=T18, pressure=p18)
# Then calculate the state using the State class method StateCalc
Point_e18.StateCalc()
# And print the dictionary for revision
State_e18 = Point_e18.__dict__ # Whole dictionary with properties
hfg3=State_e18["enthalpy"]
print(hfg3)

m10=m9
m11=m10-m16
deltaT=5

Q_evap3, m_w3 = evaporator_fct(m10,m16,m11,h10,h16,h11,cp10,deltaT,hfg3)

print(Q_evap3)
print(m_w3)

m19=m14-m_w2
m20=m15-m_w3


#Heat Exchanger 4
def HeatExchanger(mcold, cpcold, Tcoldin, Tcoldout, Thotin, cphot, mhot, hhot):
    Q = mcold*cpcold*(Tcoldout-Tcoldin)
    Qcond = mhot*abs(hhot)
    if Qcond<Q:
        print("Cold stream is completely condensed")
        Thotout = (-Q+mhot*abs(hhot))/(mhot*cphot) + Thotin
    else:
        print("Cold stream is not completely condensed")
        Thotout = Thotin
    
    print('Qcond:',Qcond)
    print('Q:',Q)
    print('Tcold_in:',Tcoldin)
    print('Tcold_out:',Tcoldout)
    print('Thot_in:',Thotin)
    print('Thot_out:',Thotout)

    return Q, Thotout

T4=337
T5=338
T19=T14
p4=p6
State_e4=mixture(T=T4, P=p4, frac_water=p_water_out0, frac_fat=p_fat_out0) # this is a dictionary!!
cp4=State_e4["cpmass"]
m5=m1
m19=m14-m_w2
p19=p6
Point_e19 = State(pair='TP', fluid='water', temperature=T19, pressure=p19)
# Then calculate the state using the State class method StateCalc
Point_e19.StateCalc()
# And print the dictionary for revision
State_e19 = Point_e19.__dict__ # Whole dictionary with properties
h19=State_e19["enthalpy"]
cp19=State_e19["cpmass"]


Q4, Thot4 = HeatExchanger(m5, cp4, T4, T5, T19, cp19, m19, h19)


#Heat Exchanger 3
T3=321
T20=T15
m4=m1
m20=m15-m_w3
p20=p8
p3=p6
State_e3=mixture(T=T3, P=p3, frac_water=p_water_out0, frac_fat=p_fat_out0) # this is a dictionary!!
cp3=State_e3["cpmass"]

Point_e20 = State(pair='TP', fluid='water', temperature=T20, pressure=p20)
# Then calculate the state using the State class method StateCalc
Point_e20.StateCalc()
# And print the dictionary for revision
State_e20 = Point_e20.__dict__ # Whole dictionary with properties
h20=State_e20["enthalpy"]
cp20=State_e20["cpmass"]

Q3, Thot3 = HeatExchanger(m4, cp3, T3, T4, T20, cp20, m20, h20)

#Heat Exchanger 2
T2=309
m3=m1
p2=p6
State_e2=mixture(T=T2, P=p2, frac_water=p_water_out0, frac_fat=p_fat_out0) # this is a dictionary!!
cp2=State_e2["cpmass"]
cp16=State_e16["cpmass"]

Q2, Thot2 = HeatExchanger(m3, cp2, T2, T3, T16, cp16, m16, h16)

#Heat Exchanger 1
T1=282.5
p1=p6
State_e1=mixture(T=T1, P=p1, frac_water=p_water_out0, frac_fat=p_fat_out0) # this is a dictionary!!
cp1=State_e1["cpmass"]
cp11=State_e11["cpmass"]
h11=State_e11["enthalpy"]

# mcold, cpcold, Tcoldin, Tcoldout, Thotin, cphot, mhot, hhot
Q1, Thot1 = HeatExchanger(m1, cp1, T1, T2, T11, cp11, m11, h11)


print('m19',m19)
print('m20',m20)
print('m16',m16)
print('m11',m11)


#Heat Exchanger Glycolic water

p12=p11
T12=Thot1
T13=277
m12=m11
State_e12=mixture(T=T12, P=p11, frac_water=p_water_out0, frac_fat=p_fat_out0)
cp12=State_e12["cpmass"]
print('cp12', cp12)

Tinglycol=270
Toutglycol=277
cpglycol=2294

Qglycol = m12*cp12*(T12-T13)
mglycol = m12*(cp12/cpglycol)*(T12-T13)/(Toutglycol-Tinglycol)
print('Qglycol:',Qglycol)
print('mglycol:',mglycol)

...

