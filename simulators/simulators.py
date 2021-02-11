def run_simulation_1d_cylindrical(xi, dz, poro, kx, rho, B, mu, cpore, cfluid, dw, re, 
                                  inner_boundary, outer_boundary, well_value,
                                  p_initial, timestep, schedule):
  """
  1D Reservoir Simulation in Cylindrical Grids
  """
  import numpy as np
  import matplotlib.pyplot as plt
  import pandas as pd

  # from __future__ import print_function
#   from ipywidgets import interact, interactive, fixed, interact_manual, ToggleButtons
#   import ipywidgets as widgets  

  from cylindrical import boundary_floweq1d_cylindrical, calculate_bulk_cylindrical, horizontal_permeability, lhs_coeffs1d_cylindrical, rhs_constant1d_cylindrical, trans_r_min, trans_r_plus, transmissibility1d_boundary_cylindrical, transmissibility2d_boundary_cylindrical, transmissibility_inner_boundary1d

  from input_output import read_input, read_depth
  from boundary import boundary_floweq1d
  from gridding import source1d
  from solver import lhs_coeffs1d_welltype, rhs_constant1d_welltype
  from transmissibility import transmissibility1d, transmissibility1d_boundary
  from wellblock import fraction_wellblock_geometric_factor
  from wellsimulation import solution_well1d
  from potential import potential_term1d
  from synthetics import constant_depth1d
  from synthetics import synthetic_initial_pressure2d  

  """""""""""
  INPUT PROCESSING
  """""""""""

  west, east = inner_boundary, outer_boundary
  well_loc = np.array([1])

  # Calculate spacing from re, because simulator only accepts spacing
  spacing = np.pi * (re**2)

  # reservoir input dictionary
  reservoir_input = {'B': B, 'cfluid': cfluid * 1E-05, 'cpore': cpore * 1E-05,
                    'dz': dz, 'kh': 150, 'mu': mu, 'poro': poro, 'rho': rho, 
                    'xi': xi}

  # create block coordinates (Engineering Notation convention in Abou-Kassem)
  zi = 1
  x_ = np.arange(1, xi+1)
  z_ = np.arange(1, zi+1)

  x, z = np.meshgrid(x_, z_, indexing='ij')

  # calculate cylindrical grid properties: logarithmic spacing constant, 
  # grid size, and bulk volume
  alpha_tg, gridblock, rn, Vbulk = calculate_bulk_cylindrical(spacing, dw, dz, xi)

  dr = rn # grid size in r-direction

  # permeability, here kh is kx (because of 1D)
  kh = kx

  # assign all params to all blocks
  dz = np.array([[dz / zi]*zi]*xi) # grid size in z-direction
  kh = np.array([[kh]*zi]*xi) # horizontal permeability
  B = np.array([[B]*zi]*xi)
  mu = np.array([[mu]*zi]*xi)
  rho = np.array([[rho]*zi]*xi)

  # source block (production or injection well)
  qsc = source1d(well_value, well_loc, xi)  # call function HERE

  """""""""""
  SIMULATION
  """""""""""

  " Produce LHS matrix. In Slightly Compressible simulation, LHS can be assumed CONSTANT "

  lhs_mat = np.array([[0.] * xi] * xi)

  # set up empty array for boundary flow rate, and two transmissibilities 
  # for later computation of RHS and pressure solve at each timestep

  qsc_b_array = []; T_min_array = []; T_plus_array = []

  for i in range(xi):

      Tr_min = trans_r_min(dz[i], dz[i], (2 * np.pi), alpha_tg, kh[i], kh[i], mu[i], B[i])
      Tr_plus = trans_r_plus(dz[i], dz[i], (2 * np.pi), alpha_tg, kh[i], kh[i], mu[i], B[i])

      if i == 0:

          # left boundary

          # flow rate from boundary
          # is always CONSTANT RATE, with divided rates over the grid blocks
          qsc_b = west['value']

          ## LHS coeffs
          ## T_min is the inner boundary transmissibility. 
          T_plus = Tr_plus
          T_min = transmissibility1d_boundary_cylindrical(west['type'], 'west', 
                                                          dr[i], dz[i], Vbulk[i], 
                                                          kh[i], mu[i], B[i])

          p_plus, p_min, p = lhs_coeffs1d_cylindrical('west', (i + 1), T_plus, T_min, 
                                                      Vbulk[i], solver='slicomp',
                                                      reservoir_input=reservoir_input,
                                                      timestep=timestep)


          qsc_b_array.append(qsc_b)
          T_min_array.append(T_min)
          T_plus_array.append(T_plus)        

          ## fill in LHS matrix (lhs_mat)
          lhs_mat[i, i] = p
          lhs_mat[i, i + 1] = p_plus

      elif i == xi - 1:
          # right boundary

          ## flow rate from boundary
          qsc_b = boundary_floweq1d_cylindrical(east['type'], dr[i], dz[i], Vbulk[i], kh[i], mu[i], B[i], value=east['value'], no_block=(i + 1))

          ## LHS coeffs
          ## T_plus is the outer boundary transmissibility.         
          T_plus = transmissibility1d_boundary_cylindrical(east['type'], 'east', 
                                                          dr[i], dz[i], Vbulk[i], 
                                                          kh[i], mu[i], B[i])
          T_min = Tr_min

          p_plus, p_min, p = lhs_coeffs1d_cylindrical('east', (i + 1), T_plus, T_min, 
                                                      Vbulk[i], solver='slicomp',
                                                      reservoir_input=reservoir_input,
                                                      timestep=timestep)

          qsc_b_array.append(qsc_b)
          T_min_array.append(T_min)
          T_plus_array.append(T_plus)  

          ## fill in LHS matrix (lhs_mat)
          lhs_mat[i, i - 1] = p_min
          lhs_mat[i, i] = p


      else:
          # interior block
          T_plus, T_min = Tr_plus, Tr_min

          p_plus, p_min, p = lhs_coeffs1d_cylindrical(None, (i + 1), T_plus, T_min, 
                                                      Vbulk[i], solver='slicomp',
                                                      reservoir_input=reservoir_input,
                                                      timestep=timestep)

          qsc_b_array.append(qsc_b)
          T_min_array.append(T_min)
          T_plus_array.append(T_plus)                                                           

          ## fill in LHS matrix (lhs_mat)
          lhs_mat[i, i - 1] = p_min
          lhs_mat[i, i] = p
          lhs_mat[i, i + 1] = p_plus

      
  " Timestep evolution of computing RHS and solving the pressure "

  # initiate solution pressure with the initial pressure array (p_initial)
  p_sol = p_initial

  p_sol_record = []
  for k in range(schedule):

    rhs_mat = np.array([[0.] * 1] * xi)  
    for i in range(xi):
      # the pressure in grid block. FIRST timestep, it equals 'p_initial'
      # the NEXT timesteps, it equals the solved and updated pressure   
      p_sol = p_sol

      if i == 0:
          # left boundary

          ## potential term equals 0 in 1D cylindrical reservoir
          potential_term = 0

          ## RHS constants
          rhs = rhs_constant1d_cylindrical(west['type'], (i + 1), potential_term, 
                                          qsc_b_array[i], T_pb=T_min_array[i],
                                          p_b=west['value'], solver='slicomp', 
                                          p_initial=p_sol[i], 
                                          reservoir_input=reservoir_input,
                                          Vb=Vbulk[i],
                                          timestep=timestep)

          ## fill in RHS matrix (rhs_mat)   
          rhs_mat[i, 0] = rhs

      elif i == xi - 1:
          # right boundary                                               

          ## potential term equals 0 in 1D cylindrical reservoir
          potential_term = 0

          ## RHS constants       
          rhs = rhs_constant1d_cylindrical(east['type'], (i + 1), potential_term, 
                                          qsc_b_array[i], T_pb=T_plus_array[i], 
                                          p_b=east['value'], solver='slicomp', 
                                          p_initial=p_sol[i],
                                          reservoir_input=reservoir_input,
                                          Vb=Vbulk[i], 
                                          timestep=timestep) 

          ## fill in RHS matrix (rhs_mat)    
          rhs_mat[i, 0] = rhs

      else:   
          # interior blocks

          ## potential term equals 0 in 1D cylindrical reservoir
          potential_term = 0

          # RHS constants
          # add term 
          Vb = Vbulk[i]
          ct = reservoir_input['cpore'] + reservoir_input['cfluid']
          rhs_term = (Vb * reservoir_input['poro'] * ct) / (5.614583 * reservoir_input['B'] * timestep) 

          rhs = (-qsc[i] + potential_term) - (rhs_term * p_sol[i])

          ## fill in RHS matrix (rhs_mat)    
          rhs_mat[i, 0] = rhs 

    """""""""""
    PRESSURE SOLVER
    """""""""""
    p_sol = np.linalg.solve(lhs_mat, rhs_mat)  
    p_sol_record.append(p_sol) 

  """""""""""
  OUTPUT
  """""""""""

  p_sol_ = []

  for i in range(len(p_sol_record)):
    p_sol = p_sol_record[i].T.reshape(-1)
    p_sol = np.expand_dims(p_sol, axis=0)
    p_sol_.append(p_sol)  

  # merge the initial pressure to the solved pressure afterwards
  p_initial_ = p_initial.reshape((1,1,xi))
  p_sol_ = np.concatenate((p_initial_, p_sol_), axis=0)
  
  return p_sol_

def plot_simulation_1d_cylindrical(p_sol_, schedule, extent=(0,20,0,1), cmap="plasma", linewidths=0):
  """
  INTERACTIVE ANIMATION
  """
  import numpy as np
  import matplotlib.pyplot as plt
  
  from ipywidgets import interact, interactive, fixed, interact_manual, ToggleButtons
  import ipywidgets as widgets  

  min, max = np.round(np.amin(p_sol_)), np.round(np.amax(p_sol_))

  @interact

  def display_pressure(day=(0, schedule)):
    fig, ax = plt.subplots(figsize=(20,2)) 

    x = rn 
    y = np.array([0,1])
    X,Y = np.meshgrid(x,y)

    Z = np.concatenate((p_sol_[day], p_sol_[day]), axis=0)

    im = ax.pcolormesh(X, Y, Z, extent=extent, edgecolors='k', linewidths=linewidths, vmin=min, vmax=max, cmap=cmap)
#     im = ax.pcolormesh(X, Y, Z, edgecolors='k', linewidths=0.005, vmin=np.amin(p_sol_), vmax=np.amax(p_sol_))

    ax.set_title('Pressure at day {}'.format(day))
    cax = fig.add_axes([0.1, -0.2, 0.8, 0.05])
    fig.colorbar(im, cax=cax, orientation='horizontal')

    ax.set_xlim(0,20)

    plt.show()
