#   Created by Georgiy Maruzhenko on 2019-03-16.
#   Copyright © 2019 Georgiy Maruzhenko. All rights reserved.

from __future__ import print_function
import matplotlib.pyplot as plt
import numpy as np
import pyromat as pyro
import math as math
from scipy.integrate import simps
from numpy import trapz

# Global Constants
GAMMA = 1.4
R = 0.08205746   # L atm / K mol
MAX_PRESSURE_RATIO = 20
T_MAX = 273.15 + 1000  # KELVIN
# CP = 1.006 * 1000     # L*atm/kgK
CP = 1.006              # KJ/kgK
# Initial Conditions
T0 = 273.15 + 10        # KELVIN
P0 = 1.  # atm
V0 = 773.4550236  # L fir 1kg air at stp
N = P0 * V0 / (R * T0)


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

    def initilize_temperature_array(pressure_array, volume_array, temperature_array):
        index = 0
        end = len(pressure_array)
        while index < end:
            temperature_array[index] = pressure_array[index] * volume_array[index] / (N * R)
            index += 1
    def calculate_delta_s(t1, t2, p1, p2):
        d_s1 = CP * math.log(t2 / t1) - N * 8.314 / 1000 * math.log(p2 / p1)
        print("delta_s = ", d_s1, "KJ")
        return d_s1


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
    v3 = N * R * T_MAX / p3
    t3 = t2 * v3 / v2

    # stage 4
    p4 = p1
    v4 = v3 * (p3/p4)**(1/GAMMA)
    t4 = t3 * (v3/v4)**(GAMMA-1)

    # stage 1 - 2
    pressure_1_2 = np.linspace(p1, p2)
    volume_1_2 = np.ones(len(pressure_1_2))
    initilize_adiabat_volume(volume_1_2, pressure_1_2, v1)
    d_s1 = calculate_delta_s(t1, t2, p1, p2)

    # stage 2 - 3
    volume_2_3 = np.linspace(v2, v3)
    pressure_2_3 = np.ones(len(volume_2_3)) * p2
    d_s2 = calculate_delta_s(t2, t3, p2, p3)

    # stage 3 - 4
    pressure_3_4 = pressure_1_2
    volume_3_4 = np.ones(len(pressure_1_2))
    initilize_adiabat_volume(volume_3_4, pressure_3_4, v4)
    calculate_delta_s(t3, t4, p3, p4)

    # stage 4 - 1
    volume_4_1 = np.linspace(v4, v1)
    pressure_4_1 = np.ones(len(volume_4_1)) * p1
    calculate_delta_s(t4, t1, p4, p1)
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


def plot_t_s():
    # initialize library
    air = pyro.get('ig.air')
    pyro.config['unit_pressure'] = 'bar'
    pyro.config['unit_temperature'] = 'K'
    pyro.config['unit_matter'] = 'kg'
    pyro.config['unit_energy'] = 'kJ'

    # isobaric
    p1 = P0
    T1 = T0
    s1 = air.s(T1, p1)
    p2 = p1 * MAX_PRESSURE_RATIO
    T2 = air.T_s(s=s1, p=p2)
    # wc = air.h(T2,p2) - air.h(T1,p1)
    T3 = T_MAX
    p4 = p1
    p3 = p2
    qh = air.h(T3, p3) - air.h(T2, p2)
    s3 = air.s(T3, p3)
    s4 = s3
    T4 = air.T_s(s=s4, p=p4)
    wt = air.h(T3, p3) - air.h(T4, p4)

    T = np.linspace(T2, T3)
    plt.plot(air.s(T=T, p=p2), T, 'r', linewidth=1.5)
    T = np.linspace(T1, T4)
    plt.plot(air.s(T=T, p=p1), T, 'r--', linewidth=1.5)

    plt.plot([s1, s1], [T1, T2], 'r', linewidth=1.5)
    plt.plot([s3, s3], [T3, T4], 'r', linewidth=1.5)

    plt.xlabel('Entropy, s (kJ/kg/K)')
    plt.ylabel('Temperature, T (K)')
    plt.grid('on')
    plt.title('Brayton Cycle T-s Graphic')
    plt.show()

# plot efficiency vs pressure ratio
#main function
# plot_thermal_efficiency_vs_pressure_ratio()
plot_t_s()
get_thermal_efficiency(MAX_PRESSURE_RATIO, 'apple')





