import pyromat as pyro
import numpy as np
import matplotlib.pyplot as plt


# Global Constants
GAMMA = 1.4
R = 0.08205746   # L atm / K mol
CP = 1.006 * 1000     # L*atm/kgK
MAX_PRESSURE_RATIO = 20.

# Initial Conditions
T0 = 273.15 + 10        # KELVIN
P0 = 1.013  # atm
V0 = 773.4550236  # L fir 1kg air at stp
N = P0 * V0 / (R * T0)  # mols
T_max = 273.15 + 1000   # KELVIN

air = pyro.get('ig.air')

pyro.config['unit_pressure'] = 'bar'
pyro.config['unit_temperature'] = 'K'
pyro.config['unit_matter'] = 'kg'
pyro.config['unit_energy'] = 'kJ'

p1 = P0
T1 = T0
pr = MAX_PRESSURE_RATIO
s1 = air.s(T1,p1)
p2 = p1*pr
T2 = air.T_s(s=s1,p=p2)
# wc = air.h(T2,p2) - air.h(T1,p1)
T3 = T_max
p4 = p1
p3 = p2
qh = air.h(T3,p3) - air.h(T2,p2)
s3 = air.s(T3,p3)
s4 = s3
T4 = air.T_s(s=s4,p=p4)
wt = air.h(T3,p3) - air.h(T4,p4)


T = np.linspace(T2,T3)
plt.plot(air.s(T=T,p=p2),T,'r',linewidth=1.5)
T = np.linspace(T1,T4)
plt.plot(air.s(T=T,p=p1),T,'r--',linewidth=1.5)

plt.plot([s1,s1],[T1,T2],'r',linewidth=1.5)
plt.plot([s3,s3],[T3,T4],'r',linewidth=1.5)

plt.xlabel('Entropy, s (kJ/kg/K)')
plt.ylabel('Temperature, T (K)')
plt.grid('on')
plt.title('Brayton Cycle T-s Graphic')
plt.show()