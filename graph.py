import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import CubicSpline
# from value import separate_by_month

def constant_curve(x, c):
    return np.full_like(x, c)





def lagrange_interpolation(x_values, y_values, x_interpolate):
    result = 0
    for i in range(len(y_values)):
        term = y_values[i]
        for j in range(len(x_values)):
            if i != j:
                term = term * (x_interpolate - x_values[j]) / (x_values[i] - x_values[j])
        result += term
    return result

def plot_lagrange_interpolation(x_values, y_values,constant1,constant2,disp, x_label, y_label, line_color='blue'):
    x_value1 = np.linspace(min(x_values), max(x_values), 300)
    y_values_constant1 = constant_curve(x_value1,constant1)

    x_value2 = np.linspace(min(x_values), max(x_values), 300)
    y_values_constant2 = constant_curve(x_value2,constant2)

    x_interpolate = np.linspace(min(x_values), max(x_values), 300)
    cubic_spline = CubicSpline(x_values, y_values)
    y_interpolate = cubic_spline(x_interpolate)

    # y_interpolate = [lagrange_interpolation(x_values, y_values, x) for x in x_interpolate]

    plt.plot(x_interpolate, y_interpolate, color=line_color)
    if(constant1!=0):
        plt.plot(x_value1,y_values_constant1, color='green', linestyle='--')
    plt.plot(x_value2,y_values_constant2, color='orange', linestyle='--')
    if(constant1!=0):
        plt.text(min(x_values)+2, constant1-0.25, 'Lower range', horizontalalignment='center',fontsize=12)
    plt.text(min(x_values)+8, constant2+0.25, 'Upperrange', horizontalalignment='center',fontsize=12)
    plt.scatter(x_values, y_values, color='red')  # Add points for reference
    plt.title(disp)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.grid(True)
    plt.show()


