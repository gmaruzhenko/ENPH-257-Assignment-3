#   Created by Georgiy Maruzhenko on 2019-03-16.
#   Copyright © 2019 Georgiy Maruzhenko. All rights reserved.

import pyromat as pyro
import numpy as np
import matplotlib.pyplot as plt


air = pyro.get('ig.air')

Wnet = 310.

p1 = 1.013

pyro.config['unit_pressure'] = 'bar'
pyro.config['unit_temperature'] = 'K'

T1 = 300.
pr = 10.
s1 = air.s(T1,p1)
pyro.config['unit_energy'] = 'kJ'
p2 = p1*pr
T2 = air.T_s(s=s1,p=p2)
wc = air.h(T2,p2) - air.h(T1,p1)
T3 = 1400.
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