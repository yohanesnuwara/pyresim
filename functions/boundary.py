"""
@author: Yohanes Nuwara
@email: ign.nuwara97@gmail.com
"""

def boundary2d_location(x, y, xi, yi):
  """ 
  Classify boundary for transmissibility
  Regular reservoir (without any inactive blocks)
  """
  
  import numpy as np

  T_identify = np.array([[0.]*yi]*xi)

  def transms(x, y, i, j, T):
    if x[i,j]==x[i,j]:
      t = T

    if x[i,j]!=x[i,j]:
      t = np.nan
    return t

  ## general transmissibility
  for i in range(xi):
    for j in range(yi):

      if i==0:
        if j==0:
          # Tx- and Ty- are flow from boundaries
          T_identify[i,j] = transms(x, y, i, j, 13)

        if j==yi-1:
          # Tx- and Ty+ are flow from boundaries
          T_identify[i,j] = transms(x, y, i, j, 14)        

        else:
          if j!=0 and j!=yi-1:
            # Tx- is flow from boundary
            T_identify[i,j] = transms(x, y, i, j, 1)

      elif i==xi-1:
        if j==0:
          # Tx+ and Ty- are flow from boundaries
          T_identify[i,j] = transms(x, y, i, j, 23)

        if j==yi-1:
          # Tx+ and Ty+ are flow from boundaries
          T_identify[i,j] = transms(x, y, i, j, 24)

        else:
          if j!=0 and j!=yi-1:
            # Tx+ is flow from boundary
            T_identify[i,j] = transms(x, y, i, j, 2)

      elif i!=0 and i!=xi-1:
        if j==0:
          # Ty- is flow from boundary
          T_identify[i,j] = transms(x, y, i, j, 3)

        if j==yi-1:  
          # Ty+ is flow from boundary        
          T_identify[i,j] = transms(x, y, i, j, 4)

        else:
          if j!=0 and j!=yi-1:
            # the interior blocks
            # no boundary flow
            T_identify[i,j] = transms(x, y, i, j, 0)
  
  return T_identify

def boundary_flow2d_constant_pressuregrad(bound_loc, value, potential_term, kx, ky, dx, dy, dz, mu, B):
  
  import numpy as np
  
  Ax = dy * dz
  Ay = dx * dz
  Az = dx * dy

  if bound_loc == 1:
    # characterize as Left boundary
    qsc = -(.001127 * (kx * Ax) / (mu * B)) * (value - potential_term)   
  if bound_loc == 3:
    # characterize as Left boundary
    qsc = -(.001127 * (ky * Ay) / (mu * B)) * (value - potential_term)           
  if bound_loc == 2:
    # characterize as Right boundary
    qsc = (.001127 * (kx * Ax) / (mu * B)) * (value - potential_term)
  if bound_loc == 4:
    # characterize as Right boundary
    qsc = (.001127 * (ky * Ay) / (mu * B)) * (value - potential_term)  
  return qsc   

def boundary_floweq1d(bound_type, dx, dy, dz, kx, mu, B, value, no_block=1):
    """
    Boundary Conditions for 1D Rectangular Reservoir (floweq simulation)
    Input:
    bound_type = type of boundary condition at West (bW) and East (bE) boundaries ('constant_pressure',
    'constant_pressuregrad', 'constant_rate', 'no_flow'
    dx, dy, dz = size of grid
    kx = permeability in x-direction
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
        Ax = dy * dz
        T = .001127 * (kx * Ax) / (mu * B * 0.5 * dx)
        qsc = '{} ({} - p{})'.format(T, value, no_block)

    if bound_type == 'constant_pressuregrad':
        Ax = dy * dz
        qsc = '{}'.format(np.round((.001127 * (kx * Ax) / (mu * B)) * (value - 0), 5))  # Eq 4.45, zero (p_grad - 0) because Z1=Z2

    if bound_type == 'constant_rate':
        qsc = '{}'.format(value)

    if bound_type == 'no_flow':
        qsc = 0

    return qsc

def boundary_floweq2d(bound_type, bound_loc, dx, dy, dz, kx, ky, mu, B, value, no_block=(2,1), no_blocks_shared=4):
    """
    Boundary Conditions for 2D Rectangular Reservoir (floweq simulation)
    Input:
    bound_type = type of boundary condition at West (bW) and East (bE) boundaries ('constant_pressure',
    'constant_pressuregrad', 'constant_rate', 'no_flow'
    bound_loc = location of boundary ('west', 'east', 'south', 'north')
    dx, dy, dz = size of grid
    kx, ky = permeability in x-direction and y-direction
    mu = fluid viscosity in boundary block
    B = fluid FVF in boundary block
    value = specify the boundary value, depends on the boundary conditions
    * if B.C. is 'constant_pressure', specify the pressure gradient: p_b
    * if B.C. is 'constant_pressuregrad', specify the pressure gradient: p_grad
    * if B.C. is 'constant_rate', specify the pressure gradient: q_b
    * if B.C. is 'no_flow', don't specify any value
    no_block = boundary block location (2D engineering notation: tuple (x,y))
    no_block_shared = amount of grid blocks at each of the boundaries (the west, east, etc.)
    Input example: West Boundary at grid block (5,4) has constant pressure gradient of 0.5 psi/ft.
    Grid properties dx, dy, dz, kx, mu, B are known. There are 7 grids in the West.
    > boundary_floweq2d('constant_pressuregrad', 'west', dx=dx, dy=dx, dz=dz, kx=kx, mu=mu, B=B, p_grad=0.1, no_block=(5,4), no_blocks_shared=7)
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

    Ax = dy * dz; Ay = dx * dz

    if bound_type == 'constant_pressure':
        if bound_loc == 'east' or bound_loc == 'west':
          T = .001127 * (kx * Ax) / (mu * B * 0.5 * dx)
          qsc = '{} ({} - p{})'.format(T, value, no_block)
        if bound_loc == 'south' or bound_loc == 'north':
          T = .001127 * (ky * Ay) / (mu * B * 0.5 * dy)
          qsc = '{} ({} - p{})'.format(T, value, no_block)

    if bound_type == 'constant_pressuregrad':
        if bound_loc == 'west':
          # characterize as Left boundary
          qsc = '{}'.format(np.round(-(.001127 * (kx * Ax) / (mu * B)) * (value - 0), 5)) # Eq 4.45, zero (p_grad - 0) because Z1=Z2  
        if bound_loc == 'south':
          # characterize as Left boundary
          qsc = '{}'.format(np.round(-(.001127 * (ky * Ay) / (mu * B)) * (value - 0), 5))             
        if bound_loc == 'east':
          # characterize as Right boundary
          qsc = '{}'.format(np.round((.001127 * (kx * Ax) / (mu * B)) * (value - 0), 5))  
        if bound_loc == 'north':
          # characterize as Right boundary
          qsc = '{}'.format(np.round((.001127 * (ky * Ay) / (mu * B)) * (value - 0), 5))  # Eq 4.45, zero (p_grad - 0) because Z1=Z2            
    
    if bound_type == 'constant_rate':
        qsc = (1 / no_blocks_shared) * value
    
    if bound_type == 'no_flow':
        qsc = 0
    return(qsc)
