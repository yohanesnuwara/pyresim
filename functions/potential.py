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
