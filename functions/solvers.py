"""
Codes for solving the reservoir simulation

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

def rhs_constant_welltype(solver, bound_type, block_location, well_df, qsc_b=None, T_pb=None, p_b=None):
  """
  Calculate the Right-hand side (RHS) constants
  All (1D, 2D, 3D) reservoir

  T_pb = transmissibility at boundary with constant pressure condition
  """  
  if solver=='incompressible':  
    if bound_type=='constant_pressure':
      rhs = - (T_pb * p_b) 
    if bound_type=='no_flow':
      rhs = 0
    if bound_type=='constant_pressuregrad' or bound_type=='constant_rate':
      rhs = - np.float64(qsc_b)

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
