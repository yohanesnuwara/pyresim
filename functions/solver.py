"""
@author: Yohanes Nuwara
@email: ign.nuwara97@gmail.com
"""

def lhs_coeffs1d_welltype(bound_loc, block_location, well_df, qsc, T_plus, T_min):
  """
  Calculate the Left-hand side (LHS) coefficients of p+, p-, and p
  1D reservoir
  """
  df = well_df.loc[well_df['well_loc'] == block_location]
  if df['well_condition'].values=='constant_fbhp':
    # well in constant FBHP condition
    Gw, mu, B = df['well_Gw'], df['well_mu'], df['well_B']
    if bound_loc=='west':
      p_plus, p_min, p = T_plus, 0, -((Gw / (mu * B)) + T_min + T_plus)
    if bound_loc=='east':
      p_plus, p_min, p = 0, T_min, -((Gw / (mu * B)) + T_min + T_plus) 
    else: 
      # None
      p_plus, p_min, p = T_plus, T_min, -((Gw / (mu * B)) + T_min + T_plus)  

  else:
    # well is either in constant pressure gradient, constant rate, OR no flow
    if bound_loc=='west':
      p_plus, p_min, p = T_plus, 0, -(T_min + T_plus)
    if bound_loc=='east':
      p_plus, p_min, p = 0, T_min, -(T_min + T_plus) 
    else: 
      # None
      p_plus, p_min, p = T_plus, T_min, -(T_min + T_plus) 

  return p_plus, p_min, p

def lhs_coeffs2d_welltype(bound_loc, well_dict, T, mu, B, 
                          solver='slicomp', reservoir_input=None, timestep=1):
  """
  Calculate the Left-hand side (LHS) coefficients of p+, p-, and p
  2D reservoir
  """
  
  import numpy as np
  
  Tx_min, Tx_plus, Ty_min, Ty_plus = T[0], T[1], T[2], T[3]
  well_condition = well_dict['condition']
  Gw = well_dict['Gw']

  " Well term "
  if Gw!=Gw:
    # NaN, no well
    A = 0

  if Gw==Gw:
    # there is well
    if well_condition=='constant_fbhp':
      # well in constant FBHP condition     
      A = np.array(Gw) / (mu * B)
    else:
      A = 0

  " Transmissibility term "
  # summing the transmissibilities
  T_sum = Tx_plus + Tx_min + Ty_plus + Ty_min
   
  " Calculate coefficients "

  # boundary blocks
  if bound_loc==1:
    px_plus, px_min, py_plus, py_min, p = Tx_plus, 0, Ty_plus, Ty_min, -(A + T_sum)

  if bound_loc==14:
    px_plus, px_min, py_plus, py_min, p = Tx_plus, 0, 0, Ty_min, -(A + T_sum)  

  if bound_loc==13:
    px_plus, px_min, py_plus, py_min, p = Tx_plus, 0, Ty_plus, 0, -(A + T_sum)  

  if bound_loc==2:
    px_plus, px_min, py_plus, py_min, p = 0, Tx_min, Ty_plus, Ty_min, -(A + T_sum) 

  if bound_loc==24:
    px_plus, px_min, py_plus, py_min, p = 0, Tx_min, 0, Ty_min, -(A + T_sum)  

  if bound_loc==23:
    px_plus, px_min, py_plus, py_min, p = 0, Tx_min, Ty_plus, 0, -(A + T_sum) 

  if bound_loc==3:
    px_plus, px_min, py_plus, py_min, p = Tx_plus, Tx_min, Ty_plus, 0, -(A + T_sum)   
      
  if bound_loc==4:
    px_plus, px_min, py_plus, py_min, p = Tx_plus, Tx_min, 0, Ty_min, -(A + T_sum)             

  # interior blocks              
  else: 
    px_plus, px_min, py_plus, py_min, p = Tx_plus, Tx_min, Ty_plus, Ty_min, -(A + T_sum)  
  
  " SOLVER "
  if solver=='incompressible':
    return px_min, px_plus, py_min, py_plus, p
  
  if solver=='slicomp':
    Vb = reservoir_input['dx'] * reservoir_input['dy'] * reservoir_input['dz']
    ct = reservoir_input['cpore'] + reservoir_input['cfluid']
    rhs_term = (Vb * reservoir_input['poro'] * ct) / (5.614583 * reservoir_input['B'] * timestep)

    # modify coefficient of p
    p = p - rhs_term
    return px_min, px_plus, py_min, py_plus, p  

# def lhs_coeffs2d_welltype(bound_loc, well_dict, T, mu, B):
#   """
#   Calculate the Left-hand side (LHS) coefficients of p+, p-, and p
#   2D reservoir
#   """
  
#   import numpy as np
  
#   Tx_min, Tx_plus, Ty_min, Ty_plus = T[0], T[1], T[2], T[3]
#   well_condition = well_dict['condition']
#   Gw = well_dict['Gw']

#   " Well term "
#   if Gw!=Gw:
#     # NaN, no well
#     A = 0

#   if Gw==Gw:
#     # there is well
#     if well_condition=='constant_fbhp':
#       # well in constant FBHP condition     
#       A = np.array(Gw) / (mu * B)
#     else:
#       A = 0

#   " Transmissibility term "
#   # summing the transmissibilities
#   T_sum = Tx_plus + Tx_min + Ty_plus + Ty_min
   
#   " Calculate coefficients "

#   # boundary blocks
#   if bound_loc==1:
#     px_plus, px_min, py_plus, py_min, p = Tx_plus, 0, Ty_plus, Ty_min, -(A + T_sum)
#     return px_min, px_plus, py_min, py_plus, p 

#   if bound_loc==14:
#     px_plus, px_min, py_plus, py_min, p = Tx_plus, 0, 0, Ty_min, -(A + T_sum)  
#     return px_min, px_plus, py_min, py_plus, p  

#   if bound_loc==13:
#     px_plus, px_min, py_plus, py_min, p = Tx_plus, 0, Ty_plus, 0, -(A + T_sum)  
#     return px_min, px_plus, py_min, py_plus, p  

#   if bound_loc==2:
#     px_plus, px_min, py_plus, py_min, p = 0, Tx_min, Ty_plus, Ty_min, -(A + T_sum) 
#     return px_min, px_plus, py_min, py_plus, p   

#   if bound_loc==24:
#     px_plus, px_min, py_plus, py_min, p = 0, Tx_min, 0, Ty_min, -(A + T_sum) 
#     return px_min, px_plus, py_min, py_plus, p   

#   if bound_loc==23:
#     px_plus, px_min, py_plus, py_min, p = 0, Tx_min, Ty_plus, 0, -(A + T_sum) 
#     return px_min, px_plus, py_min, py_plus, p    

#   if bound_loc==3:
#     px_plus, px_min, py_plus, py_min, p = Tx_plus, Tx_min, Ty_plus, 0, -(A + T_sum)  
#     return px_min, px_plus, py_min, py_plus, p  
      
#   if bound_loc==4:
#     px_plus, px_min, py_plus, py_min, p = Tx_plus, Tx_min, 0, Ty_min, -(A + T_sum)      
#     return px_min, px_plus, py_min, py_plus, p        

#   # interior blocks              
#   else: 
#     px_plus, px_min, py_plus, py_min, p = Tx_plus, Tx_min, Ty_plus, Ty_min, -(A + T_sum)  
#     return px_min, px_plus, py_min, py_plus, p
  
def rhs_constant1d_welltype(solver, bound_type, block_location, well_df, potential_term, qsc_b=None, T_pb=None, p_b=None):
  """
  Calculate the Right-hand side (RHS) constants (1D reservoir)

  T_pb = transmissibility at boundary with constant pressure condition
  potential_term = potential calculated using 'potential1d', 'potential2d', and 'potential3d'
  (for grid with ELEVATION only. If there's no ELEVATION, potential_term = 0)
  """  
  import numpy as np
  
  if solver=='incompressible':  
    if bound_type=='constant_pressure':
      rhs = 0 - (T_pb * p_b) + potential_term
    if bound_type=='no_flow':
      rhs = 0 + potential_term
    if bound_type=='constant_pressuregrad' or bound_type=='constant_rate':
      rhs = 0 - np.float64(qsc_b) + potential_term

  # well condition
  df = well_df.loc[well_df['well_loc'] == block_location]
  if df['well_condition'].values=='constant_fbhp':  
    # well in constant FBHP condition
    Gw, mu, B, pwf = df['well_Gw'], df['well_mu'], df['well_B'], df['well_value']    
    rhs = rhs - (Gw / (mu * B)) * pwf

  if df['well_condition'].values=='constant_rate': 
    # well in constant rate condition
    qsc = df['well_value']
    rhs = rhs - qsc
  
  if df['well_condition'].values=='constant_pressuregrad':
    # well in constant pressure gradient condition
    qsc = prodrate1d(df['well_condition'], p_grad=df['well_value'], Gw=df['well_Gw'], 
                    mu=df['well_mu'], B=df['well_B'], rw=df['well_rw'], 
                    kh=df['well_kh'], h=df['well_dz'])
    rhs = rhs - qsc
  
  if df['well_condition'].values=='shutin':
    rhs = rhs
  
  return rhs 

def rhs_constant2d_welltype(boundary_dict, well_dict, potential_term, 
                            dx, dy, dz, kx, ky, mu, B, solver='slicomp',
                            p_initial=None, reservoir_input=None, 
                            timestep=1):
  """
  Calculate the Right-hand side (RHS) constants (2D reservoir)

  solver = 'incompressible', 'slicomp', 'compressible'

  potential_term = potential calculated using 'potential1d', 'potential2d', and 'potential3d'
  (for grid with ELEVATION only. If there's no ELEVATION, potential_term = 0)
  """ 
  
  import numpy as np
  from boundary import boundary_flow2d_constant_pressuregrad  
   
  well_condition = well_dict['condition']
  well_value = well_dict['value']
  well_rw = well_dict['rw']
  Gw = well_dict['Gw']

  bound_loc = boundary_dict['loc']
  bound_type = boundary_dict['type']
  bound_value = boundary_dict['value']
  bound_transmissibility = boundary_dict['T']     

  " Transmissibility term "
  if bound_transmissibility==None:
    # Interior blocks, no boundary.
    rhs1 = 0

  else:
    # Boundary blocks.

    # if solver=='incompressible':  
    rhs1 = []
    for i in range(len(bound_type)):
      if bound_type[i]=='constant_pressure':
        bound_term = (bound_transmissibility[i] * bound_value[i])
      if bound_type[i]=='constant_pressuregrad':
        bound_term = boundary_flow2d_constant_pressuregrad(bound_loc[i], bound_value[i], potential_term, 
                                                            kx, ky, dx, dy, dz, mu, B)
      if bound_type[i]=='constant_rate':
        bound_term = bound_value[i] 
      if bound_type[i]=='no_flow':
        bound_term = 0  
      rhs1.append(bound_term)
    
    rhs1 = np.sum(rhs1)

  " Well term "

  if Gw!=Gw:
    # NaN, no well
    A = 0

  if Gw==Gw:
    # there is well
    if well_condition=='constant_fbhp':
      # well in constant FBHP condition     
      A = (np.array(Gw) / (mu * B) * np.array(well_value))
    if well_condition=='constant_pressuregrad':
      A = prodrate1d(well_condition, well_value, Gw, mu, B, rw, kx, dz) 
    if well_condition=='constant_rate':
      A = well_value
    if well_condition=='shutin':
      A = 0
  
  # calculate RHS constants
  rhs = -(rhs1 + A + potential_term)

  if solver=='incompressible':
    return rhs

  if solver=='slicomp':
    # add term 
    Vb = reservoir_input['dx'] * reservoir_input['dy'] * reservoir_input['dz']
    ct = reservoir_input['cpore'] + reservoir_input['cfluid']
    rhs_term = (Vb * reservoir_input['poro'] * ct) / (5.614583 * reservoir_input['B'] * timestep)  
    rhs = rhs - (rhs_term * p_initial)
    return rhs 

# def rhs_constant2d_welltype(solver, boundary_dict, well_dict, potential_term, 
#                             dx, dy, dz, kx, ky, mu, B):
#   """
#   Calculate the Right-hand side (RHS) constants (2D reservoir)

#   solver = 'incompressible', 'slicompressible', 'compressible'

#   potential_term = potential calculated using 'potential1d', 'potential2d', and 'potential3d'
#   (for grid with ELEVATION only. If there's no ELEVATION, potential_term = 0)
#   """ 
  
#   import numpy as np
#   from boundary import boundary_flow2d_constant_pressuregrad  
   
#   well_condition = well_dict['condition']
#   well_value = well_dict['value']
#   well_rw = well_dict['rw']
#   Gw = well_dict['Gw']

#   bound_loc = boundary_dict['loc']
#   bound_type = boundary_dict['type']
#   bound_value = boundary_dict['value']
#   bound_transmissibility = boundary_dict['T']     

#   " Transmissibility term "
#   if bound_transmissibility==None:
#     # Interior blocks, no boundary.
#     rhs1 = 0

#   else:
#     # Boundary blocks.

#     if solver=='incompressible':  
#       rhs1 = []
#       for i in range(len(bound_type)):
#         if bound_type[i]=='constant_pressure':
#           bound_term = (bound_transmissibility[i] * bound_value[i])
#         if bound_type[i]=='constant_pressuregrad':
#           bound_term = boundary_flow2d_constant_pressuregrad(bound_loc[i], bound_value[i], potential_term, 
#                                                               kx, ky, dx, dy, dz, mu, B)
#         if bound_type[i]=='constant_rate':
#           bound_term = bound_value[i] 
#         if bound_type[i]=='no_flow':
#           bound_term = 0  
#         rhs1.append(bound_term)
    
#     rhs1 = np.sum(rhs1)

#   " Well term "

#   if Gw!=Gw:
#     # NaN, no well
#     A = 0

#   if Gw==Gw:
#     # there is well
#     if well_condition=='constant_fbhp':
#       # well in constant FBHP condition     
#       A = (np.array(Gw) / (mu * B) * np.array(well_value))
#     if well_condition=='constant_pressuregrad':
#       A = prodrate1d(well_condition, well_value, Gw, mu, B, rw, kx, dz) 
#     if well_condition=='constant_rate':
#       A = well_value
#     if well_condition=='shutin':
#       A = 0
  
#   # calculate RHS constants
#   rhs = -(rhs1 + A + potential_term)
  
#   return rhs 

def fill2d_lhs_mat(bound_loc, block_index, xi, lhs_mat, px_min, px_plus, py_min, py_plus, p):
  """
  Fill the LHS coefficients into 2D matrix 
  For 2D reservoir

  Input:

  bound_loc = location of block coded (13, 14, 23, 24, etc.)
  block_index = block index matrix (created before simulation)
  xi = number of grid blocks in x-direction  
  lhs_mat = empty LHS matrix (created before simulation)
  px_min, px_plus, py_min, py_plus, p = coefficients of LHS

  Output:

  lhs_mat = LHS matrix has been filled with the LHS coefficients
  """
  
  import numpy as np
  
  i = block_index - 1

  # Boundary blocks
  if bound_loc==13:
    lhs_mat[i,i+1] = px_plus
    lhs_mat[i,i+xi] = py_plus
    lhs_mat[i,i] = p

  if bound_loc==23:
    lhs_mat[i,i-1] = px_min
    lhs_mat[i,i+xi] = py_plus
    lhs_mat[i,i] = p

  if bound_loc==14:
    lhs_mat[i,i+1] = px_plus
    lhs_mat[i,i-xi] = py_min
    lhs_mat[i,i] = p

  if bound_loc==24:
    lhs_mat[i,i-1] = px_min
    lhs_mat[i,i-xi] = py_min
    lhs_mat[i,i] = p

  if bound_loc==1:
    lhs_mat[i,i+1] = px_plus
    lhs_mat[i,i-xi] = py_min
    lhs_mat[i,i+xi] = py_plus
    lhs_mat[i,i] = p

  if bound_loc==2:
    lhs_mat[i,i-1] = px_min
    lhs_mat[i,i-xi] = py_min
    lhs_mat[i,i+xi] = py_plus
    lhs_mat[i,i] = p

  if bound_loc==3:
    lhs_mat[i,i-1] = px_min
    lhs_mat[i,i+1] = px_plus
    lhs_mat[i,i+xi] = py_plus
    lhs_mat[i,i] = p

  if bound_loc==4:
    lhs_mat[i,i-1] = px_min
    lhs_mat[i,i+1] = px_plus
    lhs_mat[i,i-xi] = py_min
    lhs_mat[i,i] = p   

  # Interior blocks
  if bound_loc==0:
    lhs_mat[i,i-1] = px_min
    lhs_mat[i,i+1] = px_plus
    lhs_mat[i,i-xi] = py_min
    lhs_mat[i,i+xi] = py_plus
    lhs_mat[i,i] = p

  return lhs_mat

def fill2d_rhs_mat(block_index, rhs_mat, rhs):
  """
  Fill the RHS constants into 2D matrix 
  For 2D reservoir

  Input:

  block_index = block index matrix (created before simulation)
  rhs_mat = empty RHS matrix (created before simulation)
  rhs = the RHS constant

  Output:

  rhs_mat = RHS matrix has been filled with the RHS coefficients
  """  
  import numpy as np
  
  i = block_index - 1
  rhs_mat[i,0] = rhs
  return rhs_mat
