import numpy as np

TS_sludge = 0.037
VS_sludge = 0.742
BMP_sludge = 0.407 # m3_CH4/kg_VS
d1_dry = 0.01561
d1_liquid = 0.1018
d1 = d1_dry + d1_liquid
conversion_factor = 0.90
CH4_density = 0.657 # kg/m3
CH4_in_biogas = 0.55 # kg_CH4/kg_biogas (55% CH4 in biogas)
biogas_density = 1.15 # kg/m3
biogas_expansion = 0.15
U_digester = 2.5 # W/m2/°C
T_digester = 55 # °C
T_in = 20 # °C
cp_flow = 4180 # J/kg/°C

d3 = d1 * BMP_sludge * TS_sludge * VS_sludge * conversion_factor * CH4_density / CH4_in_biogas # kg/s
d2 = d1 - d3
print(' d1=', d1, '\n', 'd2=', d2, '\n', 'd3=', d3)

# Compute the Volume
time = 20 * 24 * 3600 # 20 days in seconds
V_biogas= d3 * time / biogas_density # m3
print('V=', V_biogas)

# Compute the surface area
V_digester = V_biogas * (1 + biogas_expansion) # m3
print('V_digester=', V_digester)

D = (4 * V_digester / (0.6 * np.pi))**(1/3) 
H = 0.6 * D
print(' H =', H, '\n', 'D =', D)
A = np.pi * D * H + 2 * np.pi * (D/2)**2 # cylindrical digester area
print ('A =', A)

# Compute the heat loss
Q_digester = U_digester * A * (T_digester - T_in) # W
print('Q_digester=', Q_digester)
Q_flow = cp_flow * d1 * (T_digester - T_in) # W
print('Q_flow=', Q_flow)
Q_tot = Q_digester + Q_flow
print('Q_tot=', Q_tot)
