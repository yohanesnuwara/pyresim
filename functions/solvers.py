"""
Codes for solving the reservoir simulation

@author: Yohanes Nuwara
@email: ign.nuwara97@gmail.com
"""

def lhs_coeffs1d(bound_loc, T_plus, T_min):
  """
  Calculate the Left-hand side (LHS) coefficients of p+, p-, and p
  1D reservoir
  """
  if bound_loc=='west':
    p_plus, p_min, p = T_plus, 0, -(T_min + T_plus)
  if bound_loc=='east':
    p_plus, p_min, p = 0, T_min, -(T_min + T_plus) 
  else: 
    # None
    p_plus, p_min, p = T_plus, T_min, -(T_min + T_plus) 
  return p_plus, p_min, p

def rhs_constant(solver, bound_type, qsc, T_pb=None, p_b=None):
  """
  Calculate the Right-hand side (RHS) constants
  All (1D, 2D, 3D) reservoir

  T_pb = transmissibility at boundary with constant pressure condition
  """  
  if solver=='incompressible':  
    if bound_type=='constant_pressure':
      rhs = -qsc - (T_pb * p_b) 
    else:
      rhs = -qsc
    return rhs
