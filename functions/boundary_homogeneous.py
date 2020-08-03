"""
Codes for boundary conditions in homogeneous reservoir
@author: Yohanes Nuwara
@email: ign.nuwara97@gmail.com
"""

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

def boundary_floweq3d(bound_type, bound_loc, dx, dy, dz, kx, ky, kz, mu, B, rho, value, no_block=(2,1,3), no_blocks_shared=4):
    """
    Boundary Conditions for 3D Rectangular Reservoir (floweq simulation)

    Input:

    bound_type = type of boundary condition at West (bW) and East (bE) boundaries ('constant_pressure',
    'constant_pressuregrad', 'constant_rate', 'no_flow'
    bound_loc = location of boundary ('west', 'east', 'south', 'north')
    dx, dy, dz = size of grid
    kx, ky, kz = permeability in x-direction, y-direction, z-direction
    mu = fluid viscosity in boundary block
    B = fluid FVF in boundary block
    rho = fluid density

    value = specify the boundary value, depends on the boundary conditions
    * if B.C. is 'constant_pressure', specify the pressure gradient: p_b
    * if B.C. is 'constant_pressuregrad', specify the pressure gradient: p_grad
    * if B.C. is 'constant_rate', specify the pressure gradient: q_b
    * if B.C. is 'no_flow', don't specify any value

    no_block = boundary block location (3D engineering notation: tuple (x,y,z))
    no_block_shared = amount of grid blocks at each of the boundaries (the west, east, etc.)

    Input example: Bottom Boundary at grid block (5,4,1) has constant pressure of 2500 psia.
    Grid properties dx, dy, dz, kx, mu, B are known. There are 7 grids in the West.

    > boundary_floweq3d('constant_pressure', 'bottom', dx=dx, dy=dx, dz=dz, kx=kx, mu=mu, B=B, rho=rho, p_grad=0.1, no_block=(5,4), no_blocks_shared=7)

    Output:

    qsc = flow equation (string format)

    * if B.C. is 'constant_pressure',
    e.g.: '0.757 (3000 - p(2,1,3))')
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

    Ax = dy * dz 
    Ay = dx * dz 
    Az = dx * dy            

    if bound_type == 'constant_pressure':

        if bound_loc == 'bottom':
            Z = dz
            gamma = .21584E-3 * rho * 32.174
            Z_gamma = Z * gamma
            T = .001127 * (kz * Az) / (mu * B * 0.5 * dz)            
            qsc = '{} ({} - p{} - ({}))'.format(T, value, no_block, Z_gamma)
        if bound_loc == 'upper':
            Z = -dz
            gamma = .21584E-3 * rho * 32.174
            Z_gamma = Z * gamma
            T = .001127 * (kz * Az) / (mu * B * 0.5 * dz)
            qsc = '{} ({} - p{} - ({}))'.format(T, value, no_block, Z_gamma)
        if bound_loc == 'east' or bound_loc == 'west':
          T = .001127 * (kx * Ax) / (mu * B * 0.5 * dx)
          qsc = '{} ({} - p{})'.format(T, value, no_block)
        if bound_loc == 'south' or bound_loc == 'north':
          T = .001127 * (ky * Ay) / (mu * B * 0.5 * dy)
          qsc = '{} ({} - p{})'.format(T, value, no_block)


    if bound_type == 'constant_pressuregrad':

        Ax = dy * dz
        if bound_loc == 'bottom':
            Z = 0.5 * dz
            gamma = .21584E-3 * rho * 32.174
            Z_gamma = Z * gamma
            qsc = '{}'.format(np.round(-(.001127 * (kz * Az) / (mu * B)) * (value - Z_gamma), 5))
        if bound_loc == 'upper':
            Z = -0.5 * dz
            gamma = .21584E-3 * rho * 32.174
            Z_gamma = Z * gamma
            qsc = '{}'.format(np.round((.001127 * (kz * Az) / (mu * B)) * (value - Z_gamma), 5))
        if bound_loc == 'west':
          # characterize as Left boundary
          qsc = '{}'.format(np.round(-(.001127 * (kx * Ax) / (mu * B)) * (value - 0), 5))  # Eq 4.45, zero (p_grad - 0) because Z1=Z2
        if bound_loc == 'south':
          # characterize as Left boundary
          qsc = '{}'.format(np.round(-(.001127 * (ky * Ay) / (mu * B)) * (value - 0), 5))  # Eq 4.45, zero (p_grad - 0) because Z1=Z2            
        if bound_loc == 'east':
          # characterize as Right boundary
          qsc = '{}'.format(np.round((.001127 * (kx * Ax) / (mu * B)) * (value - 0), 5))  # Eq 4.45, zero (p_grad - 0) because Z1=Z2
        if bound_loc == 'north':
          # characterize as Right boundary
          qsc = '{}'.format(np.round((.001127 * (ky * Ay) / (mu * B)) * (value - 0), 5))  # Eq 4.45, zero (p_grad - 0) because Z1=Z2            
    
    if bound_type == 'constant_rate':
        qsc = (1 / no_blocks_shared) * value

    if bound_type == 'no_flow':
        qsc = 0

    return (qsc)
