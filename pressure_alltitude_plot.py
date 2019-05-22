#   Created by Georgiy Maruzhenko on 2019-03-16.
#   Copyright © 2019 Georgiy Maruzhenko. All rights reserved.

import numpy as np
import matplotlib.pyplot as plt


# Global Variables
START_TEMP = 15 + 273.15    # k
START_PRESSURE = 101          # kpa
GAMMA = 1.4
GRAVITY = 9.8   # m/s
MOLAR_MASS = 28.9 / 1000    # kg/mol
R = 8.314  # L atm / K mol

MAX_HEIGHT = 1000

dZ = 1   #m

def inittilize_IC():
    pressure_array[0] = START_PRESSURE
    temperature_array[0] = START_TEMP


# Start code
pressure_array = np.ones(int(MAX_HEIGHT/dZ))
temperature_array = np.ones(int(MAX_HEIGHT/dZ))
x_axis_for_plot = [i * dZ for i in range(0, int(MAX_HEIGHT/dZ))]


inittilize_IC()

index = 0
while index * dZ < MAX_HEIGHT - 1:
    dP = -1 * MOLAR_MASS * GRAVITY * pressure_array[index] / (R * temperature_array[index])
    dT = (1 - 1/GAMMA) * temperature_array[index] * dP / pressure_array[index]
    #print(dP, "and ", dT)
    print (pressure_array[index])
    pressure_array[index + 1] = pressure_array[index] + dP
    temperature_array[index + 1] = temperature_array[index] + dT
    index += 1

plt.plot(x_axis_for_plot, pressure_array)
plt.plot(x_axis_for_plot, temperature_array, 'ro')
plt.title('Pressure vs Height')
plt.xlabel('Height (m)')
plt.ylabel('Pressure (kPa)')
#plt.legend(['theoretical', 'numerical'])

plt.show()