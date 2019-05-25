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
R = 8.314  # J / K mol

# Vary these
MAX_HEIGHT = 14000
dZ = 1   #m


def inittilize_ic():
    pressure_array[0] = START_PRESSURE
    temperature_array[0] = START_TEMP


def update_arrays(position):
    dP = -1 * MOLAR_MASS * GRAVITY * pressure_array[position] * dZ / (R * temperature_array[position])
    dT = (1 - 1/GAMMA) * temperature_array[position] * dP / pressure_array[position]
    pressure_array[position + 1] = pressure_array[position] + dP
    temperature_array[position + 1] = temperature_array[position] + dT


def plot_charts():
    plt.plot(hight_array, pressure_array)
    # plt.plot(hight_array, temperature_array, 'red')
    plt.title('Elevation vs Atmospheric Pressure')
    plt.xlabel('Elevation above Sea Level (m)')
    plt.ylabel('Pressure (kPa)')
    plt.show()


# Start code
pressure_array = np.ones(int(MAX_HEIGHT/dZ))
temperature_array = np.ones(int(MAX_HEIGHT/dZ))
hight_array = [i * dZ for i in range(0, int(MAX_HEIGHT/dZ))]

inittilize_ic()

index = 0
while index * dZ < MAX_HEIGHT - 1:
    update_arrays(index)
    index += 1

plot_charts()
