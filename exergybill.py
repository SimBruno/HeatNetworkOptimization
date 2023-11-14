#Exergy Pasteurization

import math
import pandas as pd
import numpy as np

df = pd.read_csv('pasteurization_process.csv',sep = ';')

for i in range(0,len(df.index)):
    globals()[df.iloc[i][1]] = df.iloc[i][2]

Ta=25+273.15

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
#import pandas as pd
#import numpy as np
#Load csv files

#dfevap = pd.read_csv('dfevap.csv', sep = ',')
#dfhx = pd.read_csv('dfhx.csv', sep = ',')

dfrecap = pd.read_csv('dfrecap.csv', sep = ',')

for i in range(0,len(dfrecap.index)):
    globals()['m'+str(i+1)] = dfrecap['Mass flow (kg/s)'].iloc[i]
    globals()['h'+str(i+1)] = dfrecap['Enthalpy (J/mol)'].iloc[i]
    globals()['s'+str(i+1)] = dfrecap['Entropy (J/K)'].iloc[i]


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

L_eva1=m6*(h6-Ta*s6)-m7*(h7-Ta*s7)-m14*(h14-Ta*s14)+m21*(h21-Ta*s21)
print(L_eva1)

L_eva2=m8*(h8-Ta*s8)+m17*(h17-Ta*s17)-m15*(h15-Ta*s15)-m9*(h9-Ta*s9)
print(L_eva2)

L_eva3=m10*(h10-Ta*s10)-m18*(h18-Ta*s18)-m19*(h19-Ta*s19)-m11*(h11-Ta*s11)


#Total exergy evaporation section

L_tot_eva= L_heat1+L_heat2+L_heat3+L_heat4+L_eva1+L_eva2+L_eva3
print(L_tot_eva)
