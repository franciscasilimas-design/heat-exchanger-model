# -*- coding: utf-8 -*-
"""
Created on Sat May  9 15:38:26 2026

@author: franc
"""

import numpy as np
import matplotlib.pyplot as plt

# Fonctions hydraulique 

# Section 

def compute_area(D):

    return np.pi * D**2 / 4
# Vitesse

def compute_velocity(m_dot, rho, A):

    return m_dot / (rho * A)

# Reynolds 

def compute_reynolds(rho, u, D, mu):

    return rho * u * D / mu

# Facteur de friction 

def compute_friction_factor(Re):

    if Re < 2300:

        f = 64 / Re

    else:

        f = 0.3164 * Re**(-0.25)

    return f


# Perte de charge 

def compute_pressure_drop(f, L, D, rho, u):

    return f * (L / D) * (rho * u**2 / 2)


# MODULE CONVECTION

# Prandtl 

def compute_prandtl(cp, mu, k):

    return cp * mu / k

# Nusselt 

def compute_nusselt(Re, Pr, mode):

    if mode == 'heating':

        n = 0.4

    elif mode == 'cooling':

        n = 0.3

    else:

        raise ValueError("mode invalide")

    Nu = 0.023 * Re**0.8 * Pr**n

    return Nu

# Coefficient convectif 

def compute_convective_coefficient(Nu, k, D):

    return Nu * k / D

# Analyse convective 

def convection_analysis(
    m_dot,
    rho,
    mu,
    cp,
    k,
    D,
    mode
):

    A = compute_area(D)

    u = compute_velocity(m_dot, rho, A)

    Re = compute_reynolds(rho, u, D, mu)

    Pr = compute_prandtl(cp, mu, k)

    Nu = compute_nusselt(Re, Pr, mode)

    h = compute_convective_coefficient(Nu, k, D)

    return {

        "velocity": u,
        "Re": Re,
        "Pr": Pr,
        "Nu": Nu,
        "h": h
    }

# Coefficient global 

def compute_global_U(h_hot, h_cold):

    return (h_hot * h_cold) / (h_hot + h_cold)


# Solveur matriciel

def solve_heat_exchanger_matrix(
    T_c_in,
    T_f_in,
    m_dot_c,
    m_dot_f,
    cp_c,
    cp_f,
    U,
    D,
    L,
    N=100
):
    
# Maillage 

    x = np.linspace(0, L, N)

    dx = L / (N - 1)

    P = np.pi * D
    
    
# Coefficient chaud et froid 

    K_c = U * P / (m_dot_c * cp_c)

    K_f = U * P / (m_dot_f * cp_f)
    
    
# Matrice et 2nd membre

    size = 2 * N

    A = np.zeros((size, size))

    B = np.zeros(size)
    
# Equations fluides chaud

# Conditions limite fluide chaud 
    A[0, 0] = 1.0

    B[0] = T_c_in
    
    
# Noeuds interne chaud 

    for i in range(1, N):

        row = i
        
        A[row, i] = 1 + dx * K_c

        A[row, i-1] = -1
        
# Couplage fluide froid (Commence à l'indice N)

        cold_index = N + i

        A[row, cold_index] = -dx * K_c
        
        
# Equations fluide froid 

# Condition fluide froid 

    last_row = 2 * N - 1

    A[last_row, last_row] = 1.0

    B[last_row] = T_f_in
    
# Noeuds froid interne

    for i in range(N-1):
        row = N + i
        
# Equations 

        hot_index = i

        cold_index = N + i

        next_cold = N + i + 1
        
        A[row, hot_index] = -dx * K_f

        A[row, cold_index] = 1 + dx * K_f

        A[row, next_cold] = -1
        
        
# Résolution linéaire 

    X = np.linalg.solve(A, B)
    
    
# Extraction des solutions 

    T_c = X[0:N]

    T_f = X[N:2*N]
    
# Retour


    return x, T_c, T_f

# Script principal

if __name__ == "__main__":
    
    
# Analyse convective

    # =====================================================
    # PARAMETRES
    # =====================================================

    T_c_in = 80.0
    T_f_in = 20.0

    m_dot_c = 1.0
    m_dot_f = 1.0

    rho = 1000.0
    mu = 1e-3

    cp = 4180.0

    k = 0.6

    D = 0.02
    L = 5.
    
# Analyse convective 
# Chaud refroidi

    hot = convection_analysis(
        m_dot_c,
        rho,
        mu,
        cp,
        k,
        D,
        mode='cooling'
    )
    
# Froid réchauffé

    cold = convection_analysis(
        m_dot_f,
        rho,
        mu,
        cp,
        k,
        D,
        mode='heating'
    )

# Coefficient global 

    U = compute_global_U(
        hot["h"],
        cold["h"]
    )
    
    
# Affichage convection 

    print("\n===== ANALYSE CONVECTIVE =====\n")

    print(f"h chaud  = {hot['h']:.2f} W/m²/K")

    print(f"h froid  = {cold['h']:.2f} W/m²/K")

    print(f"U global = {U:.2f} W/m²/K")
    
    
# Solveur matriciel

    x, T_c, T_f = solve_heat_exchanger_matrix(
        T_c_in,
        T_f_in,
        m_dot_c,
        m_dot_f,
        cp,
        cp,
        U,
        D,
        L,
        N=200
    )
    
# Bilan Thermique 

    Q_hot = m_dot_c * cp * (T_c_in - T_c[-1])

    Q_cold = m_dot_f * cp * (T_f[0] - T_f_in)
    
    print("\n===== BILAN THERMIQUE =====\n")

    print(f"Q chaud = {Q_hot:.2f} W")

    print(f"Q froid = {Q_cold:.2f} W")

# Visualisation 

    plt.figure(figsize=(10,6))

    plt.plot(x, T_c, label='Fluide chaud', color ='red')

    plt.plot(x, T_f, label='Fluide froid', color ='blue')

    plt.xlabel('Position (m)')

    plt.ylabel('Temperature (°C)')

    plt.title('Solveur thermo-hydraulique matriciel')

    plt.grid(True)

    plt.legend()

    plt.show()