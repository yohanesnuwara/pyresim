"""
Potential term for elevated blocks

@author: Yohanes Nuwara
@email: ign.nuwara97@gmail.com
"""

def potential_term1d(rho, T_min, T_plus, Z_previous, Z, Z_next):
  """
  Calculate potential term for the RHS constant
  """
  Z_min = Z_previous - Z
  Z_plus = Z_next - Z
  gamma = .21584E-3 * rho * 32.174
  potential_term = gamma * ((T_plus * Z_plus) + (T_min * Z_min))
  return potential_term

def potential_term2d(rho, T, Zx_min, Zx_plus, Zy_min, Zy_plus, Z):
  """
  Calculate potential term in 2D reservoir

  Potential term = γ * ((T1 * ΔZ1) + (T2 * ΔZ2) + (T3 * ΔZ3) + (T4 * ΔZ4))

  Input:

  T = transmissibility array (T1, T2, T3, T4)
  """
  import numpy as np
  
  gamma = .21584E-3 * rho * 32.174
  potential_term = T * np.array([Zx_min - Z, Zx_plus - Z, Zy_min - Z, Zy_plus - Z])
  potential_term = gamma * np.sum(potential_term)
  return potential_term
