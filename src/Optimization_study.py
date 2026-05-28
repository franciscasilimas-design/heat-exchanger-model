# -*- coding: utf-8 -*-
"""
Created on Mon May 11 17:02:16 2026

@author: franc
"""

import numpy as np
import matplotlib.pyplot as plt

# Import du solveur matricielle thermohydraulique

from Thermo_hydraulique_solveur_matricielle import (
    convection_analysis,
    compute_global_U,
    compute_area,
    compute_velocity,
    compute_reynolds,
    compute_friction_factor,
    compute_pressure_drop,
    solve_heat_exchanger_matrix
)


# Paramètres physiques 

# =====================================================
# CONDITIONS THERMIQUES
# =====================================================

T_c_in = 80.0
T_f_in = 20.0

# =====================================================
# PROPRIETES FLUIDE (EAU)
# =====================================================

rho = 1000.0       # kg/m3

mu = 1e-3          # Pa.s

cp = 4180.0        # J/kg/K

k = 0.6            # W/m/K


# =====================================================
# GEOMETRIE
# =====================================================

D = 0.02           # m

L = 5.0            # m

# Domaine d'étude : étude paramétrique sur le débit

m_dot_values = np.linspace(0.1, 5.0, 40)


# Tableau de stockage 

Re_values = []

U_values = []

Q_thermal_values = []

DeltaP_values = []

PumpPower_values = []

T_hot_out_values = []

T_cold_out_values = []

# Boucle Paraméttrique 

for m_dot in m_dot_values:
    
# Analyse convective côté chaud 

    hot = convection_analysis(
        m_dot,
        rho,
        mu,
        cp,
        k,
        D,
        mode='cooling'
    )
    
# Analyse convective côté froid

    cold = convection_analysis(
    m_dot,
    rho,
    mu,
    cp,
    k,
    D,
    mode='heating'
)
    
# Coefficient Global

    U = compute_global_U(
        hot["h"],
        cold["h"]
    )
    
# Hydraulique 

#Section 
    A = compute_area(D)

# Vitesse 

    u = compute_velocity(
        m_dot,
        rho,
        A
    )


# Reynolds

    Re = compute_reynolds(
        rho,
        u,
        D,
        mu
    )
    
# Facteur de friction

    f = compute_friction_factor(Re)
    
# Perte de charge 

    DeltaP = compute_pressure_drop(
        f,
        L,
        D,
        rho,
        u
    )
    


# Résolution thermique 

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
        N=200
    )
    

# Puissance thermique 

    Q_thermal = (
        m_dot
        * cp
        * (T_c_in - T_c[-1])
    )
    
# Puissance de pompage 
# Débit volumique 

    Qv = m_dot / rho
    
# Puissance pompe

    PumpPower = DeltaP * Qv
    
# Stockage résultats

    Re_values.append(Re)

    U_values.append(U)

    Q_thermal_values.append(Q_thermal)

    DeltaP_values.append(DeltaP)

    PumpPower_values.append(PumpPower)

    T_hot_out_values.append(T_c[-1])

    T_cold_out_values.append(T_f[0])
    
    
    
# VISUALISATION

# Performance thermique

plt.figure(figsize=(10,6))

plt.plot(
    m_dot_values,
    Q_thermal_values
)

plt.xlabel("Debit massique (kg/s)")

plt.ylabel("Puissance thermique (W)")

plt.title("Performance thermique vs debit")

plt.grid(True)

plt.show()


# Perte de charge

plt.figure(figsize=(10,6))

plt.plot(
    m_dot_values,
    DeltaP_values
)

plt.xlabel("Debit massique (kg/s)")

plt.ylabel("Perte de charge (Pa)")

plt.title("Perte de charge vs debit")

plt.grid(True)

plt.show()

# Puissance de pompe

plt.figure(figsize=(10,6))

plt.plot(
    m_dot_values,
    PumpPower_values
)

plt.xlabel("Debit massique (kg/s)")

plt.ylabel("Puissance de pompage (W)")

plt.title("Puissance de pompage vs debit")

plt.grid(True)

plt.show()

# Coefficient global 

plt.figure(figsize=(10,6))

plt.plot(
    Re_values,
    U_values
)

plt.xlabel("Nombre de Reynolds")

plt.ylabel("Coefficient global U (W/m²/K)")

plt.title("Evolution de U avec Reynolds")

plt.grid(True)

plt.show()

fig, ax1 = plt.subplots()

# Axe gauche : U
ax1.plot(Re_values, U_values, label="U (thermique)")
ax1.set_xlabel("Nombre de Reynolds")
ax1.set_ylabel("U (W/m²/K)")
ax1.grid(True)

# Axe droit : Delta P
ax2 = ax1.twinx()
ax2.plot(Re_values, DeltaP_values, linestyle='--', label="ΔP (hydraulique)")
ax2.set_ylabel("Perte de charge (Pa)")

plt.title("Compromis thermo-hydraulique")

plt.show()

# U en fonction de PumpPower
plt.figure()

plt.plot(PumpPower_values, U_values)

plt.xlabel("Puissance de pompage (W)")
plt.ylabel("Coefficient global U (W/m²/K)")
plt.title("Compromis énergétique : U = f(P_pompe)")

plt.grid(True)

plt.show()
# Analyse de résultats 

print("\n===== ETUDE D'OPTIMISATION =====\n")

print(f"Debit minimal : {m_dot_values[0]:.2f} kg/s")

print(f"Debit maximal : {m_dot_values[-1]:.2f} kg/s")

print(f"Puissance thermique max : {max(Q_thermal_values):.2f} W")

print(f"Perte de charge max : {max(DeltaP_values):.2f} Pa")

print(f"Puissance pompe max : {max(PumpPower_values):.2f} W")

# =========================================
# OPTIMISATION SIMPLE
# =========================================

eta_values = []

for i in range(len(U_values)):
    if PumpPower_values[i] > 0:
        eta = U_values[i] / PumpPower_values[i]
    else:
        eta = 0
    eta_values.append(eta)

# Point optimal
idx_opt = np.argmax(eta_values)

U_opt = U_values[idx_opt]
Ppump_opt = PumpPower_values[idx_opt]
Re_opt = Re_values[idx_opt]

print("\n=== POINT DE FONCTIONNEMENT OPTIMAL ===")
print(f"Re optimal : {Re_opt:.0f}")
print(f"U optimal : {U_opt:.2f} W/m²/K")
print(f"Ppompe optimal : {Ppump_opt:.2f} W")

plt.figure()

plt.plot(PumpPower_values, U_values, label="U")

plt.scatter(Ppump_opt, U_opt, label="Optimum")

plt.xlabel("Puissance de pompage (W)")
plt.ylabel("Coefficient U (W/m²/K)")
plt.title("Compromis énergétique et point optimal")

plt.legend()
plt.grid()

plt.show()

