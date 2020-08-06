"""
Codes to calculate wellblock geometric factor, prorate (production rate), and estimate FBHP

@author: Yohanes Nuwara
@email: ign.nuwara97@gmail.com
"""
def wellblock_geometric_factor_1dlinear(dx, dy, kx, ky, s, rw, h):
  """
  Calculate the "theoretical" geometric factor
  """
  if kx != ky:
    # anisotropic wellblock
    r_eq = 0.28 * (((ky / kx)**0.5 * dx**2) + ((kx / ky)**0.5 * dy**2))**0.5 / ((ky / kx)**0.25 + (kx / ky)**0.25)
    kh = (kx * ky)**0.5

  if kx == ky:
    # isotropic wellblock
    kh = kx
    if dx == dy:
      r_eq = 0.198 * dx
    if dx != dy:
      r_eq = 0.14 * (dx**2 + dy**2)**0.5

  Gw = (2 * np.pi * .001127 * kh * h) / (np.log(r_eq / rw) + s)
  return kh, r_eq, Gw

def fraction_wellblock_geometric_factor(dx, dy, kx, ky, s, rw, h, well_config):
  """
  Calculate the geometric factor as the FRACTION of the "theoretical" geom. factor
  """
  # modify the Δx and Δy for the boundary (well configurations)
  if well_config==0:
    dx, dy = dx, dy
    fr = 1
  if well_config==1:
    dx, dy = dx, 2 * dy
    fr = 0.5
  if well_config==2:
    dx, dy = 2 * dx, dy
    fr = 0.5
  if well_config==3:
    dx, dy = 2 * dx, 2 * dy
    fr = 0.25

  # calculate horizontal permeability and equilibrium radius
  if kx != ky:
    # anisotropic wellblock
    r_eq = 0.28 * (((ky / kx)**0.5 * dx**2) + ((kx / ky)**0.5 * dy**2))**0.5 / ((ky / kx)**0.25 + (kx / ky)**0.25)
    kh = (kx * ky)**0.5

  if kx == ky:
    # isotropic wellblock
    kh = kx
    if dx == dy:
      r_eq = 0.198 * dx
    if dx != dy:
      r_eq = 0.14 * (dx**2 + dy**2)**0.5

  Gw = fr * (2 * np.pi * .001127 * kh * h) / (np.log(r_eq / rw) + s)  
  return kh, r_eq, Gw

def wellblock_geometric_factor_1dradial(kh, Z, r1, rw, s):
  """
  Z = elevation 
  """
  Gw = (2 * np.pi * .001127 * kh * Z) / (np.log(r1 / rw) + s)
  return Gw
