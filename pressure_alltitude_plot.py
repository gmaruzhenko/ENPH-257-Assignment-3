#   Created by Georgiy Maruzhenko on 2019-03-16.
#   Copyright © 2019 Georgiy Maruzhenko. All rights reserved.

import numpy as np

# Global Variables
START_TEMP = 15 + 273.15    # k
START_PRESSURE = 1          # atm
GAMMA = 1.4
GRAVITY = 9.8   # m/s
MOLAR_MASS = 28.9 / 1000    # kg/mol
R = 0.08205746   # L atm / K mol

MAX_HEIGHT = 1000

dZ = 1   #m

pressure_array = np.ones(int(MAX_HEIGHT/dZ))
temperature_array = np.ones(int(MAX_HEIGHT/dZ))

