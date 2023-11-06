import numpy as np
import pandas as pd

# This function gives the heat recieved by the heat exchanger (Q>0)

def Heat_capacity_mix(Cp_1,Cp_2,m_1,m_2,m_mix):

    Cp_mix = Cp_1*(m_1/m_mix)+Cp_2(m_2/m_mix)

    return Cp_mix
    

def heat_exchanger_Q(T_in,T_out,m,Cp):

    Q = m * Cp * abs( T_in - T_out )

    return Q
