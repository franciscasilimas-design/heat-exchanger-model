# -*- coding: utf-8 -*-
"""
Created on Wed May 13 15:04:20 2026

@author: franc
"""

import numpy as np
import matplotlib.pyplot as plt

from Thermo_hydraulique_solveur_matricielle import (
    compute_area,
    compute_velocity,
    compute_reynolds,
    compute_prandtl,
    compute_nusselt,
    compute_convective_coefficient,
    compute_global_U,
    solve_heat_exchanger_matrix
)

from advanced_properties import compute_viscosity_water


def solve_heat_exchanger_nonlinear(
    T_c_in,
    T_f_in,
    m_dot,
    cp,
    k,
    D,
    L,
    rho,
    N=100,
    max_iter=50,
    tol=1e-4
):

    # Initialisation
    T_c = np.full(N, T_c_in)
    T_f = np.full(N, T_f_in)

    for iteration in range(max_iter):

        T_c_old = T_c.copy()
        T_f_old = T_f.copy()

        # =========================================
        # PROPRIETES MOYENNES
        # =========================================

        T_mean_c = np.mean(T_c)
        T_mean_f = np.mean(T_f)

        mu_c = compute_viscosity_water(T_mean_c)
        mu_f = compute_viscosity_water(T_mean_f)

        # =========================================
        # HYDRAULIQUE
        # =========================================

        A = compute_area(D)

        u = compute_velocity(m_dot, rho, A)

        Re_c = compute_reynolds(rho, u, D, mu_c)
        Re_f = compute_reynolds(rho, u, D, mu_f)

        Pr_c = compute_prandtl(cp, mu_c, k)
        Pr_f = compute_prandtl(cp, mu_f, k)

        # =========================================
        # CONVECTION
        # =========================================

        Nu_c = compute_nusselt(Re_c, Pr_c, mode='cooling')
        Nu_f = compute_nusselt(Re_f, Pr_f, mode='heating')

        h_c = compute_convective_coefficient(Nu_c, k, D)
        h_f = compute_convective_coefficient(Nu_f, k, D)

        U = compute_global_U(h_c, h_f)

        # =========================================
        # RESOLUTION THERMIQUE
        # =========================================

        x, T_c, T_f = solve_heat_exchanger_matrix(
            T_c_in,
            T_f_in,
            m_dot,
            m_dot,
            cp,
            cp,
            U,
            D,
            L,
            N
        )

        # =========================================
        # TEST CONVERGENCE
        # =========================================

        err = max(
            np.max(np.abs(T_c - T_c_old)),
            np.max(np.abs(T_f - T_f_old))
        )

        if err < tol:
            print(f"Convergence atteinte en {iteration+1} iterations")
            break

    return x, T_c, T_f, U

if __name__ == "__main__":

    

    # =========================================
    # PARAMETRES
    # =========================================

    T_c_in = 80.0
    T_f_in = 20.0

    m_dot = 1.0

    rho = 1000.0
    cp = 4180.0
    k = 0.6

    D = 0.02
    L = 5.0

    # =========================================
    # RESOLUTION NON LINEAIRE
    # =========================================

    x, T_c, T_f, U = solve_heat_exchanger_nonlinear(
        T_c_in,
        T_f_in,
        m_dot,
        cp,
        k,
        D,
        L,
        rho,
        N=200
    )

    print("\n===== RESULTATS NON LINEAIRES =====\n")
    print(f"U global = {U:.2f} W/m²/K")

    # =========================================
    # PLOT
    # =========================================

    plt.figure(figsize=(10,6))

    plt.plot(x, T_c, label="Fluide chaud (non-linéaire)")
    plt.plot(x, T_f, label="Fluide froid (non-linéaire)")

    plt.xlabel("Position (m)")
    plt.ylabel("Température (°C)")
    plt.title("Solveur non-linéaire avec propriétés variables")

    plt.grid(True)
    plt.legend()

    plt.show()
    
    from performance_analysis import (
    compute_ntu,
    compute_effectiveness
)

NTU = compute_ntu(U, D, L, m_dot, cp)

epsilon, Q_real = compute_effectiveness(
    m_dot,
    cp,
    T_c_in,
    T_f_in,
    T_c[-1]
)

print("\n===== ANALYSE NTU =====\n")
print(f"NTU = {NTU:.3f}")
print(f"Effectiveness = {epsilon:.3f}")
print(f"Puissance thermique = {Q_real:.2f} W")