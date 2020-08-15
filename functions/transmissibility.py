"""
@author: Yohanes Nuwara
@email: ign.nuwara97@gmail.com
"""

def transmissibility1d_boundary(bound_type, dx, dy, dz, kx, mu, B):
  """
  Calculate the transmissibility at boundary (specifically for constant pressure B.C.)
  1D reservoir
  """
  if bound_type=='constant_pressure':
    Ax = dy * dz
    T = .001127 * (kx * Ax) / (mu * B * 0.5 * dx)
  else:
    T = 0    
  return T

def transmissibility2d_boundary(bound_loc, bound_type, dx, dy, dz, kx, ky, mu, B):
  """
  Calculate the transmissibility at boundary (specifically for constant pressure B.C.)
  2D reservoir
  """
  if bound_type=='constant_pressure':
    if bound_loc==1 or bound_loc==2:
      Ax = dy * dz
      T = .001127 * (kx * Ax) / (mu * B * 0.5 * dx)
    if bound_loc==3 or bound_loc==4:
      Ay = dx * dz
      T = .001127 * (ky * Ay) / (mu * B * 0.5 * dy)      
  if bound_type=='constant_pressuregrad' or bound_type=='constant_rate' or bound_type=='no_flow':
    T = 0    
  return T 

def transmissibility1d(dx, dy, dz, kx, mu, B):
  A = dy * dz
  T_min = .001127 * (kx * A) / (mu * B * dx)
  T_max = T_min
  return T_min, T_max

def transmissibility2d(dx, dy, dz, kx, ky, mu, B):
  Ax = dy * dz
  Ay = dx * dz

  # flow to x direction
  Tx_min = .001127 * (kx * Ax) / (mu * B * dx)
  Tx_plus = Tx_min

  # flow to y direction
  Ty_min = .001127 * (ky * Ay) / (mu * B * dy)
  Ty_plus = Ty_min   
  return Tx_min, Tx_plus, Ty_min, Ty_plus
