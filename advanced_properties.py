# -*- coding: utf-8 -*-
"""
Created on Wed May 13 14:41:24 2026

@author: franc
"""
import numpy as np
import matplotlib.pyplot as plt


# =====================================================
# VISCOSITE DYNAMIQUE DE L'EAU
# =====================================================

def compute_viscosity_water(T_celsius):
    """
    Calcule la viscosité dynamique de l'eau (Pa.s)

    Paramètre
    ----------
    T_celsius : float ou array
        Température en degrés Celsius

    Retour
    -------
    mu : float ou array
        Viscosité dynamique en Pa.s

    Corrélation utilisée :
    mu(T) = 2.414e-5 * 10^(247.8 / (T - 140))

    avec T en Kelvin
    """

    T_kelvin = T_celsius + 273.15

    mu = 2.414e-5 * 10**(247.8 / (T_kelvin - 140))

    return mu

# Test sur la valeur de la viscosité

if __name__ == "__main__":

    T_test = np.array([20, 40, 60, 80])

    mu = compute_viscosity_water(T_test)

    for T, m in zip(T_test, mu):
        print(f"T = {T} °C -> mu = {m:.6e} Pa.s")