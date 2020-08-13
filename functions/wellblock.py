"""
Codes to calculate wellblock geometric factor, prorate (production rate), and estimate FBHP

@author: Yohanes Nuwara
@email: ign.nuwara97@gmail.com
"""

def prodrate1d(well_condition, well_value, Gw=10, mu=1, B=1, rw=2, kh=10, h=10):
  if well_condition == 'shutin':
    qsc = 0
  if well_condition == 'constant_pressuregrad':
    qsc = (- (2 * np.pi * .001127 * kh * rw * h) / (B * mu)) * well_value
  if well_condition == 'constant_fbhp':
    qsc = '{} (p - {})'.format((-Gw / (mu * B)), pwf)
  if well_condition == 'constant_rate':
    qsc = q
  return qsc

def fraction_wellblock_geometric_factor(dx, dy, kx, ky, s, rw, h, well_config):
  """
  Calculate the geometric factor as the FRACTION of the "theoretical" geom. factor
  """
  import numpy as np
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
