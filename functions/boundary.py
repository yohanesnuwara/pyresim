"""
Codes for boundary conditions

@author: Yohanes Nuwara
@email: ign.nuwara97@gmail.com
"""

def constant_pressure_bc1d(no_block, p_b, dy, dz, kx, dx, mu, B):
  """
  Flow expression for 1D, 2D, 3D constant pressure boundary block

  Input:

  no_block = boundary block location
  p_b = pressure at the boundary
  dy, dz = these two can be interchangeable depends on the boundary location
  * if the boundary block receives constant pressure boundary in y direction: input as dx, dz
  * if the boundary block receives constant pressure boundary in x direction: input as dy, dz
  * if the boundary block receives constant pressure boundary in z direction: input as dx, dy
  kx = can be interchangeable depends on the boundary location
  * if the boundary block receives constant pressure boundary in y direction: input as ky
  * if the boundary block receives constant pressure boundary in x direction: input as kx
  * if the boundary block receives constant pressure boundary in z direction: input as kz
  dx = can be interchangeable depends on the boundary location
  * if the boundary block receives constant pressure boundary in y direction: input as dy
  * if the boundary block receives constant pressure boundary in x direction: input as dx
  * if the boundary block receives constant pressure boundary in z direction: input as dz
  mu = fluid viscosity in boundary block
  B = fluid FVF in boundary block

  Output:

  qsc = Flow expression as string 
  
  e.g.: '0.757 (3000 - p(2,1))')  
  where: 0.757 is the calculated transmissibility, 3000 is the p_b, and (2,1)
  is the no_block (boundary location)
  """
  Ax = dy * dz
  T = .001127 * (kx * Ax) / (mu * B * 0.5 * dx)
  qsc = '{} ({} - p{})'.format(T, p_b, no_block)
  return(qsc)

def constant_pressuregrad_bc1d(p_grad, dy, dz, kx, mu, B):
  """
  Flow expression for 1D, 2D, 3D constant pressure gradient boundary block

  Input:

  p_grad = pressure gradient at the boundary
  dy, dz = these two can be interchangeable depends on the boundary location
  * if the boundary block receives constant pressure boundary in y direction: input as dx, dz
  * if the boundary block receives constant pressure boundary in x direction: input as dy, dz
  * if the boundary block receives constant pressure boundary in z direction: input as dx, dy
  kx = can be interchangeable depends on the boundary location
  * if the boundary block receives constant pressure boundary in y direction: input as ky
  * if the boundary block receives constant pressure boundary in x direction: input as kx
  * if the boundary block receives constant pressure boundary in z direction: input as kz
  mu = fluid viscosity in boundary block
  B = fluid FVF in boundary block

  Output:

  qsc = Flow expression as string 
  
  e.g.: '100.5'
  where: 100.5 is the calculated flow rate 
  """

  Ax = dy * dz
  qsc = '{}'.format(np.round((.001127 * (kx * Ax) / (mu * B)) * (p_grad - 0), 5)) # Eq 4.45, zero (p_grad - 0) because Z1=Z2
  return(qsc)

def constant_rate_bc1d(q_b):
  """
  Flow expression for 1D (only) constant rate gradient boundary block
  (either no flow or specified rate)

  Input:

  q_b = constant rate at the boundary
  * if no flow, input q_b = 0
  * if flow is specified, input the value to q_b

  Output:

  qsc = Flow expression as string 
  
  e.g.: '100.5' or '0.'
  where: 10.5 and 0 is exactly the flow rate 
  """
  qsc = '{}'.format(q_b)
  return(qsc)

def constant_rate_bc2d(T, q_b, no_blocks_shared):
  """
  Flow expression for 2D, 3D constant pressure boundary block
  (either no flow or specified rate)

  Input:

  T = transmissibility into boundary block
  q_b = constant rate at the boundary
  * if no flow, input q_b = 0
  * if flow is specified, input the value to q_b  
  no_blocks_shared = number of boundary blocks shared by the flow boundary
  e.g. in 4x3 size 2D reservoir, 
  * if the flow at East/West boundary is specified, no_blocks_shared = 3. 
  * if the flow at North/South boundary is specified, no_blocks_shared = 4.

  Output:

  qsc = Flow expression as string 
  
  e.g.: '50.5'
  where: 50.5 is the calculated flow rate at the boundary block after shared
  """
  qsc = T / (no_blocks_shared * T) * q_b
  return(qsc)
