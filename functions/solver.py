def lhs_coeffs2d_welltype(bound_loc, well_dict, T, mu, B):
  """
  Calculate the Left-hand side (LHS) coefficients of p+, p-, and p
  2D reservoir

  """
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
    return px_min, px_plus, py_min, py_plus, p 

  if bound_loc==14:
    px_plus, px_min, py_plus, py_min, p = Tx_plus, 0, 0, Ty_min, -(A + T_sum)  
    return px_min, px_plus, py_min, py_plus, p  

  if bound_loc==13:
    px_plus, px_min, py_plus, py_min, p = Tx_plus, 0, Ty_plus, 0, -(A + T_sum)  
    return px_min, px_plus, py_min, py_plus, p  

  if bound_loc==2:
    px_plus, px_min, py_plus, py_min, p = 0, Tx_min, Ty_plus, Ty_min, -(A + T_sum) 
    return px_min, px_plus, py_min, py_plus, p   

  if bound_loc==24:
    px_plus, px_min, py_plus, py_min, p = 0, Tx_min, 0, Ty_min, -(A + T_sum) 
    return px_min, px_plus, py_min, py_plus, p   

  if bound_loc==23:
    px_plus, px_min, py_plus, py_min, p = 0, Tx_min, Ty_plus, 0, -(A + T_sum) 
    return px_min, px_plus, py_min, py_plus, p    

  if bound_loc==3:
    px_plus, px_min, py_plus, py_min, p = Tx_plus, Tx_min, Ty_plus, 0, -(A + T_sum)  
    return px_min, px_plus, py_min, py_plus, p  
      
  if bound_loc==4:
    px_plus, px_min, py_plus, py_min, p = Tx_plus, Tx_min, 0, Ty_min, -(A + T_sum)      
    return px_min, px_plus, py_min, py_plus, p        

  # interior blocks              
  else: 
    px_plus, px_min, py_plus, py_min, p = Tx_plus, Tx_min, Ty_plus, Ty_min, -(A + T_sum)  
    return px_min, px_plus, py_min, py_plus, p

def rhs_constant2d_welltype(solver, boundary_dict, well_dict, potential_term, 
                            dx, dy, dz, kx, ky, mu, B):
  """
  Calculate the Right-hand side (RHS) constants (2D reservoir)

  solver = 'incompressible', 'slicompressible', 'compressible'

  potential_term = potential calculated using 'potential1d', 'potential2d', and 'potential3d'
  (for grid with ELEVATION only. If there's no ELEVATION, potential_term = 0)

  """ 
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

    if solver=='incompressible':  
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
  
  return rhs 
