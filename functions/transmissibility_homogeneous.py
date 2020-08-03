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

def transmissibility3d(dx, dy, dz, kx, ky, kz, mu, B):
  Ax = dy * dz
  Ay = dx * dz
  Az = dx * dy

  # flow to x direction
  Tx_min = .001127 * (kx * Ax) / (mu * B * dx)
  Tx_plus = Tx_min

  # flow to y direction
  Ty_min = .001127 * (ky * Ay) / (mu * B * dy)
  Ty_plus = Ty_min   

  # flow to y direction
  Tz_min = .001127 * (kz * Az) / (mu * B * dz)
  Tz_plus = Tz_min

  return Tx_min, Tx_plus, Ty_min, Ty_plus, Tz_min, Tz_plus

def potential3d(dz, rho):
  """
  Calculate the potential term (γ*ΔZ) for flow term in 3D reservoir

  in 3D case (unlike 1D, 2D), the potential term is not neglected, 
  because there is elevation difference in z-direction. In 1D and 2D, 
  in x and y-direction, there is no elevation difference, so γ*ΔZ = 0
  """
  # Z for flow from below (positive sign, vector)
  Z_min = dz

  # Z for flow from above (negative sign, vector)
  Z_plus = - dz

  # gamma
  gamma_min = .21584E-3 * rho * 32.174
  gamma_plus = gamma_min

  Z_gamma_min = Z_min * gamma_min
  Z_gamma_plus = Z_plus * gamma_plus  

  return Z_gamma_min, Z_gamma_plus
