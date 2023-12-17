# type: ignore
# flake8: noqa
#
#
#
```
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#

import math
import pandas as pd
import numpy as np
from IPython.display import display, HTML

df = pd.read_csv('pasteurization_process.csv',sep = ';')

for i in range(0,len(df.index)):
    globals()[df.iloc[i][1]] = df.iloc[i][2]

Delta_T_Gly=5
Ta=298

#Refrigeration
L_milk_ref=m_fmilk*Cp_fmilk*((T_fmilk-T_mixure_out)-T_a*math.log(T_fmilk/T_mixure_out))

L_gy_ref=m_gly_ref*Cp_glywater*((Delta_T_Gly)-T_a*np.log(T_fmilk/T_mixure_out))#glywater temperature

L_ref=L_milk_ref+L_gy_ref


#Past 1

L_past1_1=m_fmilk*Cp_fmilk*((T_mixure_out-T_past_cent)-T_a*np.log(T_mixure_out/T_past_cent))
L_past1_2=m_milk*Cp_raw_milk*((T_past_c-T_past_d)-T_a*np.log(T_past_c/T_past_d) )

L_past1=L_past1_1+L_past1_2

#Past 2

L_past2_1=m_milk*Cp_raw_milk*((T_past_a-T_milk_0)-T_a*np.log(T_past_a/T_milk_0))  
L_past2_2=m_milk*Cp_raw_milk*((T_past_c-T_past_b)-T_a*np.log(T_past_c/T_past_b)) 

L_past2_1=m_milk*Cp_raw_milk*((T_milk_0-T_past_a)-T_a*np.log(T_milk_0/T_past_a))  
L_past2_2=m_milk*Cp_raw_milk*((T_past_b-T_past_c)-T_a*np.log(T_past_b/T_past_c)) 

L_past2=L_past2_1+L_past2_2


#Past 3

L_past3_1=m_milk*Cp_raw_milk*((T_past_b-T_past_a)-T_a*np.log(T_past_b/T_past_a))

L_past3_2=m_steam_past3*(delta_h_steam-T_a*delta_s_steam)

L_past3=L_past3_1L_past3_2-


#Past 4

L_past4_1=m_milk*Cp_raw_milk*((T_milk-T_past_d)-T_a*np.log(T_milk/T_past_d))

L_gy_past4=m_gly_past4*Cp_glywater*((T_milk-T_past_d)-T_a*np.log(T_milk/T_past_d))#glywater temperature

L_past4=L_past4_1+L_gy_past4


#Past 5
L_past5_1=m_int*Cp_cream*((T_crpast_a-T_cream)-T_a*np.log(T_crpast_a/T_cream))
L_past5_2=m_cream*Cp_cream*((T_crpast_c-T_crpast_b)-T_a*np.log(T_crpast_c/T_crpast_b))

L_past5=L_past5_1+L_past5_2


#Past 6
L_past6_1=m_cream*Cp_cream_mixed*((T_crpast_x-T_crpast_b)-T_a*np.log(T_crpast_x/T_crpast_b))
L_past6_2=m_steam_past6*(delta_h_steam-Ta*delta_s_steam)

L_past6=L_past6_1+L_past6_2


#Past 7

L_past7_1=m_cream*Cp_cream*((T_crpast_c-T_cream)-T_a*np.log(T_crpast_c/T_cream))

L_gy_past7=m_gly_past7*Cp_glywater*((T_crpast_c-T_cream)-T_a*np.log(T_crpast_c/T_cream))#glywater temperature

L_past7=L_past7_1+L_gy_past7


#Mixer

L_mixer_1=m_cream*Cp_cream*((T_crpast_a-T_crpast_x)-T_a*np.log(T_crpast_a/T_crpast_x))
L_mixer_2=m_thick*Cp_alboline*((T_crpast_x-T_thick)-T_a*np.log(T_crpast_x/T_thick))

L_mixer=L_mixer_1+L_mixer_2


#Total exergy pasteurisation section

L_tot_past= L_ref+L_past1+L_past2+L_past3+L_past4+L_past5+L_past6+L_past7+L_mixer


# Dataframe for Exergy Loss Pasteurization

Exergy_losses  = 'kW'

Variables_Names = ['L_Refrigeration','L_Past1','L_Past2','L_Past3','L_Past4','L_Past5','L_Past6','L_Past7','L_mixer','L_tot_past']
Variables_Values = np.divide([L_ref,L_past1,L_past2,L_past3,L_past4,L_past5,L_past6,L_past7,L_mixer,L_tot_past],1000)
Variables_Units =  Exergy_losses
df = pd.DataFrame(data = {'Exergy loss': Variables_Names, 'Value':Variables_Values, 'Unit': Variables_Units})
display(df)
HTML(df.to_html(index=False))

#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#

#Exergy Evaporation

#import math
import pandas as pd
import numpy as np
from IPython.display import display, HTML

dfrecap = pd.read_csv('dfrecap.csv', sep = ',')

for i in range(0,len(dfrecap.index)):
    globals()['m'+str(i+1)] = dfrecap['Mass flow (kg/s)'].iloc[i]
    globals()['h'+str(i+1)] = dfrecap['Enthalpy (J/mol)'].iloc[i]
    globals()['s'+str(i+1)] = dfrecap['Entropy (J/K)'].iloc[i]


#Exergy for heat exchangers

Ta=298

L_heat1 = m11*(h11-Ta*s11)-m12*(h12-Ta*s12)+m1*(h1-Ta*s1)-m2*(h2-Ta*s2)

L_heat2= -m2*(h2-Ta*s2)+m3*(h3-Ta*s3)-m16*(h16-Ta*s16)


L_heat3=-m3*(h3-Ta*s3)+m4*(h4-Ta*s4)-m20*(h20-Ta*s20)


L_heat4=-m4*(h4-Ta*s4)+m5*(h5-Ta*s5)+m15*(h15-Ta*s15)


#Exergy for evaporators

L_eva1=-m6*(h6-Ta*s6)+m7*(h7-Ta*s7)+m14*(h14-Ta*s14)-m21*(h21-Ta*s21)


L_eva2=-m8*(h8-Ta*s8)-m17*(h17-Ta*s17)+m15*(h15-Ta*s15)+m9*(h9-Ta*s9)


L_eva3=-m10*(h10-Ta*s10)+m18*(h18-Ta*s18)+m16*(h16-Ta*s16)+m11*(h11-Ta*s11)


#Total exergy evaporation section

L_tot_eva= L_heat1+L_heat2+L_heat3+L_heat4+L_eva1+L_eva2+L_eva3


# Dataframe for Exergy Loss Evaporation

Exergy_losses  = 'kW'

Variables_Names = ['L_heat1','L_heat2','L_heat3','L_heat4','L_eva1','L_eva2','L_eva3','L_tot_eva']
Variables_Values = np.divide([L_heat1,L_heat2,L_heat3,L_heat4,L_eva1,L_eva2,L_eva3,L_tot_eva],1000)
Variables_Units =  Exergy_losses
df_2 = pd.DataFrame(data = {'Exergy loss': Variables_Names, 'Value':Variables_Values, 'Unit': Variables_Units})

display(df_2)
display(HTML(df_2.to_html(index=False)))
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#print dataframe with the price of electricity and natural gas in France and Germany
import pandas as pd
import numpy as np
from IPython.display import display, HTML

elec_fr = 0.12 # €/kWh
elec_ger = 0.21 # €/kWh
gas_fr = 0.08 # €/kWh
gas_gr = 0.08 # €/kWh

price = pd.DataFrame({'France (€/kWh)':[elec_fr, gas_fr], 'Germany (€/kWh)':[elec_ger, gas_gr]}, index = ['Electricity', 'Natural gas'])
price = price.round(3)
HTML(price.to_html())
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
top = 24*0.95*365 #h/year

#Pasterization
Qpast_ref = 60416 #W    
Qpast_4 = 3863424 #W  #A changer 
Qpast_5 = 16344 #W    #A changer
Qpast_3 = 285.76 #W   #A changer
Qpast_6 = 16643 #W    #A changer

Qpast_cool = Qpast_ref + Qpast_4 + Qpast_5
Qpast_heat = Qpast_3 + Qpast_6 

#Evap
Qevap_5 = 55703.14  #W
Qevap_st1 = 98038.87 #W
Qevap_cool = Qevap_5
Qevap_heat = Qevap_st1

#Dryer
Qdry_cool = 15299.94 #W
Qdry_hx1 =  112.16 #W
Qdry_hx2 =  1967.71#W
Qdry_cool = Qdry_cool
Qdry_heat = Qdry_hx1 + Qdry_hx2 

#Cleaning
Qclean_cool = 225940 #W
Qclean_heat = 334710 #W

#Storage & hot water
Q_storage = 500000  #W
Qhot_water = 167253.2 #W

#Rivella
Qrivella_heat =  579418.2 #W

#Digester
Qdigester_dq1 = 28754.1 #W
Qdigester_steam = 107608.5 #W
Qdigester_heat = Qdigester_dq1 + Qdigester_steam

#Cool cost
COP = 3.5 # assumption
Qcool_tot = (Qpast_cool + Qevap_cool + Qdry_cool + Qclean_cool + Q_storage)/COP
OPEXcool_fr = Qcool_tot*0.001 * elec_fr * top
OPEXcool_ger = Qcool_tot*0.001 * elec_ger *top

#Heat cost
Qheat_tot = Qpast_heat + Qevap_heat + Qdry_heat + Qclean_heat + Qhot_water + Qrivella_heat + Qdigester_heat
OPEXheat_fr = Qheat_tot*0.001 * gas_fr * top
OPEXheat_ger = Qheat_tot*0.001 * gas_gr * top

#print in a dataframe the OPEX line: cooling, heating and total and column: France, Germany
OPEX = pd.DataFrame({'France (M€/y)':[OPEXcool_fr/1e6, OPEXheat_fr/1e6, OPEXcool_fr/1e6 + OPEXheat_fr/1e6], 'Germany (M€/y)':[OPEXcool_ger/1e6, OPEXheat_ger/1e6, OPEXcool_ger/1e6 + OPEXheat_ger/1e6]}, index = ['Cooling', 'Heating', 'Total'])
OPEX = OPEX.round(3)
HTML(OPEX.to_html())
#
#
#
#
