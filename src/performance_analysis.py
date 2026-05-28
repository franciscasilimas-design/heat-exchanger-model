# -*- coding: utf-8 -*-
"""
Created on Wed May 13 15:29:29 2026

@author: franc
"""

import numpy as np


def compute_ntu(U, D, L, m_dot, cp):

    A = np.pi * D * L

    C = m_dot * cp

    C_min = C  # débits égaux

    NTU = U * A / C_min

    return NTU


def compute_effectiveness(m_dot, cp, T_c_in, T_f_in, T_c_out):

    C = m_dot * cp

    Q_real = m_dot * cp * (T_c_in - T_c_out)

    Q_max = C * (T_c_in - T_f_in)

    epsilon = Q_real / Q_max

    return epsilon, Q_real