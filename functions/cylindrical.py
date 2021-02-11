def transmissibility1d_boundary_cylindrical(bound_type, bound_loc, dr, dz, Vb, kh, mu, B):
  """
  Calculate the transmissibility at boundary (specifically for constant pressure B.C.)
  1D reservoir
  """
  import numpy as np
  
  if bound_type=='constant_pressure':
    if bound_loc=='east':
      # calculate area of grid in Z-direction
      Az = Vb / dz
      # calculate circumference of the grid
      circ = 2 * np.pi * np.sqrt(Az / np.pi)
      # calculate area of grid in r-direction
      Ar = circ * dz
      # transmissibility
      T = .001127 * (kh * Ar) / (mu * B * 0.5 * dr)
    if bound_loc=='west':
      T = 0
  else:
    # boundary type is 'constant_rate', 'constant_pressuregrad', 'no_flow'    
    T = 0 
  return T
  
def transmissibility2d_boundary_cylindrical(bound_type, bound_loc, dr, dz, Vb, kh, kz, mu, B):
  """
  Calculate the transmissibility at boundary (specifically for constant pressure B.C.)
  2D reservoir

  In cylindrical there are only 4 boundaries: 'upper', 'bottom', 'west', and 'east'
  'west' is the inner-ring boundary (in contact with WELL)
  'east' is the outer-ring boundary (in contact with BOUNDARY ZONE e.g. AQUIFER)
  """
  import numpy as np
  
  if bound_type=='constant_pressure':
    if bound_loc=='bottom' or bound_loc=='upper':
      # calculate area of grid in r-direction      
      Az = dv / dz
      # transmissibility      
      T = .001127 * (kz * Az) / (mu * B * 0.5 * dz)
    if bound_loc=='east':
      # calculate area of grid in Z-direction
      Az = Vb / dz
      # calculate circumference of the grid
      circ = 2 * np.pi * np.sqrt(Az / np.pi)
      # calculate area of grid in r-direction
      Ar = circ * dz
      # transmissibility
      T = .001127 * (kh * Ar) / (mu * B * 0.5 * dr)
    if bound_loc=='west':
      T = 0
  else:
    # boundary type is 'constant_rate', 'constant_pressuregrad', 'no_flow'
    T = 0    
  return T

def boundary_floweq1d_cylindrical(bound_type, dr, dz, Vb, kh, mu, B, value, no_block=1):
    """
    Boundary Conditions for 1D Rectangular Reservoir (floweq simulation)
    Input:
    bound_type = type of boundary condition at West (bW) and East (bE) boundaries ('constant_pressure',
    'constant_pressuregrad', 'constant_rate', 'no_flow'
    dr, dz = size of grid (r-direction and z-direction)
    Vb = bulk volume of grid
    kh = permeability in x-direction
    mu = fluid viscosity in boundary block
    B = fluid FVF in boundary block
    value = specify the boundary value, depends on the boundary conditions
    * if B.C. is 'constant_pressure', specify the pressure gradient: p_b
    * if B.C. is 'constant_pressuregrad', specify the pressure gradient: p_grad
    * if B.C. is 'constant_rate', specify the pressure gradient: q_b
    * if B.C. is 'no_flow', don't specify any value
    no_block = boundary block location
    Input example: Boundary at grid block 4 has constant pressure gradient of 0.5 psi/ft.
    Grid properties dx, dy, dz, kx, mu, B are known.
    > boundary_floweq1d('constant_pressuregrad', dx=dx, dy=dx, dz=dz, kx=kx, mu=mu, B=B, p_grad=0.1, no_block=4)
    Output:
    qsc = flow equation (string format)
    * if B.C. is 'constant_pressure',
    e.g.: '0.757 (3000 - p(2,1))')
    where: 0.757 is the calculated transmissibility, 3000 is the p_b, and (2,1)
    is the no_block (boundary location)
    * if B.C. is 'constant_pressuregrad',
    e.g.: '100.5'
    where: 100.5 is the calculated flow rate
    * if B.C. is 'constant_rate',
    e.g.: '100.5'
    where: 10.5 is exactly the flow rate
    * if B.C. is 'no_flow',
    e.g.: '0.'
    where: 0 is exactly the flow rate (no flow)
    """
    import numpy as np
    if bound_type == 'constant_pressure':
        # calculate area of grid in Z-direction
        Az = Vb / dz
        # calculate circumference of the grid
        circ = 2 * np.pi * np.sqrt(Az / np.pi)
        # calculate area of grid in r-direction
        Ar = circ * dz
        # transmissibility
        T = .001127 * (kh * Ar) / (mu * B * 0.5 * dr)
        qsc = '{} ({} - p{})'.format(T, value, no_block)

    if bound_type == 'constant_pressuregrad':
        # calculate area of grid in Z-direction
        Az = Vb / dz
        # calculate circumference of the grid
        circ = 2 * np.pi * np.sqrt(Az / np.pi)
        # calculate area of grid in r-direction
        Ar = circ * dz
        # transmissibility
        T = .001127 * (kh * Ar) / (mu * B * 0.5 * dr)        
        qsc = '{}'.format(np.round((.001127 * (kh * Ar) / (mu * B)) * (value - 0), 5))  # Eq 4.45, zero (p_grad - 0) because Z1=Z2

    if bound_type == 'constant_rate':
        qsc = '{}'.format(value)

    if bound_type == 'no_flow':
        qsc = 0

    return qsc
  
def calculate_bulk_cylindrical(spacing, dw, h, nr):
  """
  Calculate bulk volume of cylindrical grids

  Input:

  spacing = well spacing (ft)
  dw = wellbore diameter (ft)
  h = reservoir thickness (ft)
  nr = number of grid blocks in x-direction

  Output:

  α_tg = logarithmic spacing constant
  gridblock = number of gridblocks (notation: 1, 2, 3, ..., nr)
  rn = size of grid block
  Vbulk = bulk volume of grid block (ft3)
  """
  import numpy as np

  # gridblock
  gridblock = np.arange(1, nr+1, 1)

  # calculate reservoir outer boundary
  re = np.sqrt(spacing / np.pi)

  # calculate reservoir inner boundary (=wellbore radius)
  rw = 0.5 * dw

  # calculate α_tg
  α_tg = (re / rw)**(1 / nr)

  # calculate gridblock spacing in r direction
  r1 = ((α_tg * np.log(α_tg)) / (α_tg - 1)) * rw # 1st gridblock

  ## next gridblock
  rn = []

  for i in range(2, nr+1):
    rn_ = α_tg**(i-1) * r1
    rn.append(rn_)

  rn = np.append(r1, rn)

  # calculate gridblock boundaries in r direction for transmissibility calculation

  ## min direction
  rtrans_min = ((α_tg - 1) / (α_tg * np.log(α_tg))) * rn

  ## plus direction
  rtrans_plus = ((α_tg - 1) / (np.log(α_tg))) * rn

  # calculate argument for ln term
  ratio_ri_rtrans_min = (α_tg * np.log(α_tg)) / (α_tg - 1)
  ratio_riplus_rtrans_plus = (α_tg * np.log(α_tg)) / (α_tg - 1)
  ratio_rtrans_min_rimin = (α_tg - 1) / (np.log(α_tg)) 
  ratio_rtrans_plus_ri = (α_tg - 1) / (np.log(α_tg)) 
  ratio_rtrans_plus_rtrans_min = α_tg 

  # calculate gridblock boundaries in r direction for bulk volume calculation

  ## min direction
  rbulk_min = np.sqrt(((α_tg**2 - 1) / (α_tg**2 * np.log(α_tg**2))) * rn**2)

  ## plus direction
  rbulk_plus = np.sqrt(((α_tg**2 - 1) / (np.log(α_tg**2))) * rn**2)
  rbulk_plus[-1] = re # change the last value of rbulk_plus with re

  # bulk volume calculation
  θ = 2 * np.pi # angle

  ## calculation for r1 until rn-1
  Vbulk_ri = []
  for i in range(nr-1):
    Vbulk_ = (((α_tg**2 - 1)**2 / (α_tg**2 * np.log(α_tg**2))) * rn[i]**2) * (0.5 * θ) * h
    Vbulk_ri.append(Vbulk_)

  ## calculation for rn (last grid block)
  Vbulk_rn = (1 - (np.log (α_tg) / (α_tg - 1))**2 * (α_tg**2 - 1) / (α_tg**2 * np.log(α_tg**2))) * re**2 * (0.5 * θ) * h

  ## append both Vbulk_ri and Vbulk_rn
  Vbulk = np.append(Vbulk_ri, Vbulk_rn)

  return α_tg, gridblock, rn, Vbulk

def trans_r_min(dz_now, dz_prev, dtheta, alpha_tg, kh_now, kh_prev, mu, B):
  """
  Calculate transmissibility of cylindrical grid in r- direction
  """
  import numpy as np
  # transmissibility geometric factor
  G_trans_r_min = (.001127 * dtheta) / (np.log(alpha_tg * np.log(alpha_tg) / (alpha_tg - 1)) / (dz_now * kh_now) + np.log((alpha_tg - 1) / np.log(alpha_tg)) / (dz_prev * kh_prev))
  # calculate transmissibility
  T_r_min = G_trans_r_min / (mu * B)
  return T_r_min

def trans_r_plus(dz_now, dz_next, dtheta, alpha_tg, kh_now, kh_next, mu, B):
  """
  Calculate transmissibility of cylindrical grid in r+ direction
  """
  import numpy as np
  # transmissibility geometric factor
  G_trans_r_plus = (.001127 * dtheta) / (np.log((alpha_tg - 1) / np.log(alpha_tg)) / (dz_now * kh_now) + np.log(alpha_tg * np.log(alpha_tg) / (alpha_tg - 1)) / (dz_next * kh_next))
  # calculate transmissibility
  T_r_plus = G_trans_r_plus / (mu * B)
  return T_r_plus
  
def horizontal_permeability(kx, ky):
  """
  Calculate horizontal permeability using geometric mean
  """
  import numpy as np

  kh = np.sqrt(kx * ky)
  return kh

def lhs_coeffs1d_cylindrical(bound_loc, block_location, T_plus, T_min, Vb, 
                            solver='slicomp', reservoir_input=None, timestep=1):
  """
  Calculate the Left-hand side (LHS) coefficients of p+, p-, and p
  1D cylindrical reservoir
  """
  import numpy as np
  
  if bound_loc=='west':
    p_plus, p_min, p = T_plus, 0, -(T_min + T_plus)
  if bound_loc=='east':
    p_plus, p_min, p = 0, T_min, -(T_min + T_plus) 
  else: 
    # None
    p_plus, p_min, p = T_plus, T_min, -(T_min + T_plus) 

  " SOLVER "

  if solver=='incompressible':
    return p_plus, p_min, p         
  
  if solver=='slicomp':
    # Vb = reservoir_input['dx'] * reservoir_input['dy'] * reservoir_input['dz']
    ct = reservoir_input['cpore'] + reservoir_input['cfluid']
    rhs_term = (Vb * reservoir_input['poro'] * ct) / (5.614583 * reservoir_input['B'] * timestep)

    # modify coefficient of p
    p = p - rhs_term
    return p_plus, p_min, p


def rhs_constant1d_cylindrical(bound_type, block_location, potential_term, 
                               qsc_b=None, T_pb=None, p_b=None, solver='slicomp', 
                               p_initial=None, reservoir_input=None, Vb=None, timestep=1):
  """
  Calculate the Right-hand side (RHS) constants (1D reservoir)

  T_pb = transmissibility at boundary with constant pressure condition
  potential_term = potential calculated using 'potential1d', 'potential2d', and 'potential3d'
  (for grid with ELEVATION only. If there's no ELEVATION, potential_term = 0)
  """  
  import numpy as np

  # boundary conditions  
  if bound_type=='constant_pressure':
    rhs = 0 - (T_pb * p_b) + potential_term
  if bound_type=='no_flow':
    rhs = 0 + potential_term
  if bound_type=='constant_pressuregrad' or bound_type=='constant_rate':
    rhs = 0 - np.float64(qsc_b) + potential_term

  " SOLVERS "
  if solver=='incompressible':
    return rhs

  if solver=='slicomp':
    # add term 
    ct = reservoir_input['cpore'] + reservoir_input['cfluid']
    rhs_term = (Vb * reservoir_input['poro'] * ct) / (5.614583 * reservoir_input['B'] * timestep)  
    rhs = rhs - (rhs_term * p_initial)
    return rhs  

def transmissibility_inner_boundary1d(well_df):
  """
  Calculate inner boundary transmissibility of a cylindrical grid
  due to flow from WELL
  """
  well_condition = well_df['well_condition']

  if well_condition == 'constant_fbhp':
    Gw = well_df['well_Gw']
    mu = well_df['well_mu']
    B = well_df['well_B']
    T_min = Gw / (mu * B)
  else:
    T_min = 0
    
  return T_min 
