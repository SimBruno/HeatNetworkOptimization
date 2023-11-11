elec_fr = 0.12 # €/kWh
elec_ger = 0.21 # €/kWh

gas_fr = 0.08 # €/kWh
gas_gr = 0.08 # €/kWh 

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
Qdry_cool = 0 #W
Qdry_hx1 = 0 #W
Qdry_hx2 = 0 #W

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

Qcool_tot = Qpast_cool + Qevap_cool + Qdry_cool + Qclean_cool + Q_storage
OPEXcool_fr = Qcool_tot*0.001 * elec_fr * top
OPEXcool_ger = Qcool_tot*0.001 * elec_ger *top

#Heat cost

Qheat_tot = Qpast_heat + Qevap_heat + Qdry_heat + Qclean_heat + Qhot_water + Qrivella_heat + Qdigester_heat
OPEXheat_fr = Qheat_tot*0.001 * gas_fr * top
OPEXheat_ger = Qheat_tot*0.001 * gas_gr * top

print('OPEXcool_fr =', OPEXcool_fr, '\n', 'OPEXcool_ger =', OPEXcool_ger, '\n', 'OPEXheat_fr =', OPEXheat_fr, '\n', 'OPEXheat_ger =', OPEXheat_ger)

#WHAT TO DO FOR WATER AND 