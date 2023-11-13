#Exergy Pasteurization

import math

Q_refrigeration=60.416
Q_past1=1691.648
Q_past2=142.88
Q_past3=285.76
Q_past4=3863.4239999999995
Q_past5=16.344426439950947
Q_past6=16.643399999999918
Q_past7=124.40440000000011
T_fmilk=6.0
T_mixure_out=4.0
T_past_cent=60.0
T_milk_0=60.0
T_cream_0=60.0
T_past_a=65.0
T_past_b=75.0
T_past_c=80.0
T_past_d=139.19820828667412
T_milk=4.0
T_crpast_a=65.01501225490199
T_thick=4.0
T_crpast_x=64.83236605779223
T_crpast_b=75.0
T_crpast_c=80.0
T_cream=4.0
m_fmilk=8.0
m_milk=7.52
m_cream=0.55
m_int=0.4800000000000004
m_thick=0.07
m_gly_ref=3.0982564102564103
m_steam_past3=28.63326653306613
m_gly_past4=198.12430769230767
m_steam_past6=1.6676753507013946
m_gly_past7=6.379712820512826
Cp_alboline=70.0
Cp_raw_milk=3800.0
Cp_cream=3400.0
Cp_glywater=3900.0
Cp_steam=1996.0
Cp_fmilk=3776.0
Cp_cream_mixed=2976.1818181818207
Ta=25+273
#Refrigeration
L_milk_ref=m_fmilk*Cp_fmilk*(T_fmilk-T_mixure_out)-Ta*math.log(T_fmilk/T_mixure_out)

L_gy_ref=m_gly_ref*Cp_glywater*(T_fmilk-T_mixure_out)-Ta*math.log(T_fmilk/T_mixure_out)

L_ref=L_milk_ref+L_gy_ref
print(L_ref)
#Past 1

L_past1_1=m_fmilk*Cp_fmilk*(T_mixure_out-T_past_cent)-Ta*math.log(T_mixure_out/T_past_cent)
L_past1_2=m_milk*Cp_raw_milk*(T_past_c-T_past_d)-Ta*math.log(T_past_c/T_past_d) 

L_past1=L_past1_1+L_past1_2
print(L_past1)
#Past 2

L_past2_1=m_milk*Cp_raw_milk*(T_milk_0-T_past_a)-Ta*math.log(T_milk_0/T_past_a) #Question which m and cp
L_past2_2=m_milk*Cp_raw_milk*(T_past_b-T_past_c)-Ta*math.log(T_past_b/T_past_c) #Question which m and cp

L_past2=L_past2_1+L_past2_2
print(L_past2)


#Exergy Evaporation
#Load csv files (dfevap, dfhx, dfrecap)
import pandas as pd
import numpy as np
#Load csv files
dfevap = pd.read_csv('dfevap.csv', sep = ',')
dfhx = pd.read_csv('dfhx.csv', sep = ',')
dfrecap = pd.read_csv('dfrecap.csv', sep = ',')


print(dfrecap["Mass flow (kg/s)"])
m1=dfrecap["Mass flow"].iloc(0)
m2=dfrecap["Mass flow"].loc[1]
print(dfrecap.loc[1, "Mass flow"])
m3=dfrecap["Mass flow"].iloc(2)
m4=dfrecap["Mass flow"].iloc(3)
m5=dfrecap["Mass flow"].iloc(4)
m6=dfrecap["Mass flow"].iloc(5)
m7=dfrecap["Mass flow"].iloc(6)
m8=dfrecap["Mass flow"].iloc(7)
m9=dfrecap["Mass flow"].iloc(8)
m10=dfrecap["Mass flow"].iloc(9)
m11=dfrecap["Mass flow"].iloc(10)
m12=dfrecap["Mass flow"].iloc(11)
m13=dfrecap["Mass flow"].iloc(12)
m14=dfrecap["Mass flow"].iloc(13)
m15=dfrecap["Mass flow"].iloc(14)
m16=dfrecap["Mass flow"].iloc(15)
m17=dfrecap["Mass flow"].iloc(16)
m18=dfrecap["Mass flow"].iloc(17)
m19=dfrecap["Mass flow"].iloc(18)
m20=dfrecap["Mass flow"].iloc(19)
m21=dfrecap["Mass flow"].iloc(20)
m22=dfrecap["Mass flow"].iloc(21)
m23=dfrecap["Mass flow"].iloc(22)

h1=dfrecap["Enthalpy"].iloc(0)
h2=dfrecap["Enthalpy"].iloc(1)
h3=dfrecap["Enthalpy"].iloc(2)
h4=dfrecap["Enthalpy"].iloc(3)
h5=dfrecap["Enthalpy"].iloc(4)
h6=dfrecap["Enthalpy"].iloc(5)
h7=dfrecap["Enthalpy"].iloc(6)
h8=dfrecap["Enthalpy"].iloc(7)
h9=dfrecap["Enthalpy"].iloc(8)
h10=dfrecap["Enthalpy"].iloc(9)
h11=dfrecap["Enthalpy"].iloc(10)
h12=dfrecap["Enthalpy"].iloc(11)
h13=dfrecap["Enthalpy"].iloc(12)
h14=dfrecap["Enthalpy"].iloc(13)
h15=dfrecap["Enthalpy"].iloc(14)
h16=dfrecap["Enthalpy"].iloc(15)
h17=dfrecap["Enthalpy"].iloc(16)
h18=dfrecap["Enthalpy"].iloc(17)
h19=dfrecap["Enthalpy"].iloc(18)
h20=dfrecap["Enthalpy"].iloc(19)
h21=dfrecap["Enthalpy"].iloc(20)
h22=dfrecap["Enthalpy"].iloc(21)
h23=dfrecap["Enthalpy"].iloc(22)

s1=dfrecap["Entropy"].iloc(0)
s2=dfrecap["Entropy"].iloc(1)
s3=dfrecap["Entropy"].iloc(2)
s4=dfrecap["Entropy"].iloc(3)
s5=dfrecap["Entropy"].iloc(4)
s6=dfrecap["Entropy"].iloc(5)
s7=dfrecap["Entropy"].iloc(6)
s8=dfrecap["Entropy"].iloc(7)
s9=dfrecap["Entropy"].iloc(8)
s10=dfrecap["Entropy"].iloc(9)
s11=dfrecap["Entropy"].iloc(10)
s12=dfrecap["Entropy"].iloc(11)
s13=dfrecap["Entropy"].iloc(12)
s14=dfrecap["Entropy"].iloc(13)
s15=dfrecap["Entropy"].iloc(14)
s16=dfrecap["Entropy"].iloc(15)
s17=dfrecap["Entropy"].iloc(16)
s18=dfrecap["Entropy"].iloc(17)
s19=dfrecap["Entropy"].iloc(18)
s20=dfrecap["Entropy"].iloc(19)
s21=dfrecap["Entropy"].iloc(20)
s22=dfrecap["Entropy"].iloc(21)
s23=dfrecap["Entropy"].iloc(22)


#Exergy for heat exchangers

L_heat1 = m11*(h11-Ta*s11)-m12*(h12-Ta*s12)+m1*(h1-Ta*s1)-m2*(h2-Ta*s2)
print(L_heat1)

L_heat2= m2*(h2-Ta*s2)-m3*(h3-Ta*s3)+m16*(h16-Ta*s16)
print(L_heat2)

L_heat3=m3*(h3-Ta*s3)-m4*(h4-Ta*s4)+m20*(h20-Ta*s20)
print(L_heat3)

L_heat4=m4*(h4-Ta*s4)-m5*(h5-Ta*s5)-m15*(h15-Ta*s15)
print(L_heat4)

#Exergy for evaporators

L_eva1=m6*(h6-Ta*s6)-m7*(h7-Ta*s7)-m14*(h14-Ta*s14)+m_21(h21-Ta*s21)
print(L_eva1)

L_eva2=m8*(h8-Ta*s8)+m17*(h17-Ta*s17)-m15*(h15-Ta*s15)-m9*(h9-Ta*s9)
print(L_eva2)

L_eva3=m10*(h10-Ta*s10)-m18*(h18-Ta*s18)-m19*(h19-Ta*s19)-m11*(h11-Ta*s11)


#Total exergy evaporation section

L_tot_eva= L_heat1+L_heat2+L_heat3+L_heat4+L_eva1+L_eva2+L_eva3
print(L_tot_eva)