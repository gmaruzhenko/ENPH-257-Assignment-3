#   Created by Georgiy Maruzhenko on 2019-03-16.
#   Copyright © 2019 Georgiy Maruzhenko. All rights reserved.

from __future__ import print_function
import matplotlib.pyplot as plt
import numpy as np
import math as math
from scipy.integrate import simps
from numpy import trapz

# Global Constants
GAMMA = 1.4
R = 0.08205746   # L atm / K mol
CP = 1.006 * 1000     # L*atm/kgK
MAX_PRESSURE_RATIO = 20

# Initial Conditions
T0 = 273.15 + 10        # KELVIN
P0 = 1.  # atm
V0 = 773.4550236  # L fir 1kg air at stp
N = P0 * V0 / (R * T0)  # mols


def get_thermal_efficiency(p_maximum_ratio, type):
    # helpers
    def initilize_adiabat_volume(volume_array, pressure_array, v_minimum):
        volume_array[0] = v_minimum
        count = 1
        while count < len(pressure_array):
            volume_array[count] = volume_array[count - 1] * (pressure_array[count - 1] / pressure_array[count]) ** (
                        1 / GAMMA)
            count += 1
        return

    def efficiency_comparison():
        print("actual efficiency =", get_numerical_efficiency())
        print("theoretical efficiency =", get_theoretical_efficiency())
        return

    def get_theoretical_efficiency():
        return 1 - t1 / t2

    def get_numerical_efficiency():
        area = - abs(trapz(pressure_1_2, volume_1_2)) + abs(trapz(pressure_2_3, volume_2_3)) \
               + abs(trapz(pressure_3_4, volume_3_4)) - abs(trapz(pressure_4_1, volume_4_1))
        heat_in = N * 7 / 2 * R * (t3 - t2)
        return area / heat_in

    def plot_chart():
        plt.plot(volume_1_2, pressure_1_2, 'blue')
        plt.plot(volume_2_3, pressure_2_3, 'red')
        plt.plot(volume_3_4, pressure_3_4, 'green')
        plt.plot(volume_4_1, pressure_4_1, 'black')

        plt.title('Brayton Cycle P-V ')
        plt.xlabel('Volume, V (L)')
        plt.ylabel('Pressure, P (atm)')
        plt.legend(['Adiabatic Compression', 'Isobaric Combustion', 'Adiabatic Compression', 'Isobaric Cooling'])

        plt.show()
        return

    def initilize_temperature_array(pressure_array, volume_array, temperature_array):
        index = 0
        end = len(pressure_array)
        while index < end:
            temperature_array[index] = pressure_array[index] * volume_array[index] / (N * R)
            index += 1

    def initilize_delta_s(temperature_array, pressure_array, delta_entropy_array):
        delta_entropy_array[0] = 0
        index = 1
        end = len(temperature_array)
        while index < end :
            delta_entropy_array[index] = CP * math.log(temperature_array[index]/temperature_array[index-1]) \
                                         - (N * R) * math.log(pressure_array[index] / pressure_array[index-1])
            index += 1
    # Constraints for System
    T_max = 273.15 + 1000   # KELVIN

    # Stage 1 (given)
    p1 = P0
    t1 = T0
    v1 = N * R * t1 / p1

    # stage 2
    p2 = p1 * p_maximum_ratio
    v2 = v1 * (p1/p2)**(1/GAMMA)
    t2 = t1 * (v1/v2)**(GAMMA - 1)

    # stage 3
    p3 = p2
    v3 = N * R * T_max / p3
    t3 = t2 * v3 / v2

    # stage 4
    p4 = p1
    v4 = v3 * (p3/p4)**(1/GAMMA)
    t4 = t3 * (v3/v4)**(GAMMA-1)

    # stage 1 - 2
    pressure_1_2 = np.linspace(p1, p2)
    volume_1_2 = np.ones(len(pressure_1_2))
    temperature_1_2 = np.ones(len(pressure_1_2))
    delta_s_1_2 = np.ones(len(temperature_1_2))

    initilize_adiabat_volume(volume_1_2, pressure_1_2, v1)
    initilize_temperature_array(pressure_1_2, volume_1_2, temperature_1_2)
    initilize_delta_s(temperature_1_2, pressure_1_2, delta_s_1_2)

    plt.plot(temperature_1_2, delta_s_1_2)


    # stage 2 - 3
    volume_2_3 = np.linspace(v2, v3)
    pressure_2_3 = np.ones(len(volume_2_3)) * p2
    temperature_2_3 = np.ones(len(pressure_2_3))
    delta_s_2_3 = np.ones(len(temperature_1_2))
    initilize_temperature_array(pressure_2_3, volume_2_3, temperature_2_3)
    initilize_delta_s(temperature_2_3, pressure_2_3, delta_s_2_3)

    plt.plot(temperature_2_3, delta_s_2_3)
    plt.show()

    # stage 3 - 4
    pressure_3_4 = pressure_1_2
    volume_3_4 = np.ones(len(pressure_1_2))
    temperature_3_4 = np.ones(len(pressure_1_2))
    initilize_adiabat_volume(volume_3_4, pressure_3_4, v4)
    initilize_temperature_array(pressure_3_4, volume_3_4, temperature_3_4)

    # stage 4 - 1
    volume_4_1 = np.linspace(v4, v1)
    pressure_4_1 = np.ones(len(volume_4_1)) * p1
    temperature_4_1 = np.ones(len(volume_4_1))
    initilize_temperature_array(pressure_4_1, volume_4_1, temperature_4_1)

    # uncomment to plot and show Brayton Cycle P-V
    #plot_chart()

    # uncomment to show Thermal efficiency vs Pressure ratio comparison
    #efficiency_comparison()

    # return requested type of efficiency
    if type == 'theoretical':
        return get_theoretical_efficiency()
    else:
        return get_numerical_efficiency()


def plot_thermal_efficiency_vs_pressure_ratio():
    # set max value we want to plot up to

    pressure_ratio_array = [i for i in range(1, MAX_PRESSURE_RATIO + 1)]
    thermal_eff_array = [get_thermal_efficiency(i, 'theoretical') * 100 for i in pressure_ratio_array]
    numeric_eff_array = [get_thermal_efficiency(i, 'numerical') * 100 for i in pressure_ratio_array]

    plt.plot(thermal_eff_array, pressure_ratio_array)
    plt.plot(numeric_eff_array, pressure_ratio_array, 'ro')
    plt.title('Pressure Ratio VS Thermal Efficiency')
    plt.xlabel('Thermal Efficiency (%)')
    plt.ylabel('Pressure Ratio')
    plt.legend(['theoretical', 'numerical'])

    plt.show()


# plot efficiency vs pressure ratio
get_thermal_efficiency(20, 'apple')







