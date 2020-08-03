"""
Simulation in 3D Homogeneous Rectangular Reservoir Grids

@author: Yohanes Nuwara
@email: ign.nuwara97@gmail.com
"""

from boundary_homogeneous import *
from transmissibility_homogeneous import *
from utilities_homogeneous import *

"""""""""""
INPUT
"""""""""""

xi = 4; yi = 3; zi = 3 # number of blocks in x, y, z

# define parameters, in this case blocks are homogeneous and same in size
dx = 250 # ft
dy = 300
dz = 33.333
kx = 270 # md
ky = 220
kz = 50
B = 1 # RB/STB
mu = 2 # cp
rho = 55 # fluid density, lbm/ft3

# source term
# define the coordinates 
xyzsc = np.array([(3,2,2), (2,1,3), (4,1,1), (2,1,1)])

# define rate of each source term 
q = np.array([-133.3, 100, -25, 50]) 

# boundary conditions

bottom = {"type": "constant_pressuregrad", "value": -0.5}
upper = {"type": "constant_pressure", "value": 3000}
east = {"type": "constant_rate", "value": -200}
west = {"type": "no_flow", "value": 0}
north = {"type": "constant_pressure", "value": 1500}
south = {"type": "constant_rate", "value": 100}

"""""""""""
MAIN CODE
"""""""""""

# source term
qsc = source3d(q, xyzsc, xi, yi, zi)

# " Produce flow equations "

print('Right-Hand Side (RHS) of Flow equation in each block')
print('1st term: Flow in X-direction from next block')
print('2nd term: Flow in X-direction from previous block')
print('3rd term: Flow in Y-direction from next block')
print('4th term: Flow in Y-direction from previous block')
print('5th term: Flow in Z-direction from next block')
print('6th term: Flow in Z-direction from previous block')
print('7th term: Source accumulation \n')

for i in range(xi):
  for j in range(yi):
    for k in range(zi):

      # calculate transmissibility
      Tx_min, Tx_plus, Ty_min, Ty_plus, Tz_min, Tz_plus = transmissibility3d(dx, dy, dz, kx, ky, kz, mu, B)

      # calculate potential term for z-direction flow
      Z_gamma_min, Z_gamma_plus = potential3d(dz, rho)   

      ## West Boundaries
      if i==0:
        qsc_bW = boundary_floweq3d(west['type'], 'west', dx, dy, dz, kx, ky, kz, mu, B, rho, west['value'], no_block=(i+1,j+1,k+1), no_blocks_shared=yi*zi)

        if j==0:
          qsc_bS = boundary_floweq3d(south['type'], 'south', dx, dy, dz, kx, ky, kz, mu, B, rho, south['value'], no_block=(i+1,j+1,k+1), no_blocks_shared=xi*zi)

          if k==0:
            # bottom southwest corner boundary
            # 3 faces. Tx-, Ty-, Tz-
            qsc_bB = boundary_floweq3d(bottom['type'], 'bottom', dx, dy, dz, kx, ky, kz, mu, B, rho, bottom['value'], no_block=(i+1,j+1,k+1), no_blocks_shared=xi*yi)            
            print('Bottom southwest corner boundary block')
            print('Block {}: [{} (p{} - p{})] + [{}] + [{} (p{} - p{})] + [{}] + [{} (p{} - p{}) - ({})] + [{}] + [{}] \n'.format((i+1,j+1,k+1), Tx_plus, (i+2,j+1,k+1), (i+1,j+1,k+1), qsc_bW, Ty_plus, (i+1,j+2,k+1), (i+1,j+1,k+1), qsc_bS, Tz_plus, (i+1,j+1,k+2), (i+1,j+1,k+1), Z_gamma_plus, qsc_bB, qsc[i,j,k]))
          
          if k==zi-1:
            # upper southwest corner boundary
            # 3 faces. Tx-, Ty-, Tz+
            qsc_bU = boundary_floweq3d(upper['type'], 'upper', dx, dy, dz, kx, ky, kz, mu, B, rho, upper['value'], no_block=(i+1,j+1,k+1), no_blocks_shared=xi*yi)
            print('Upper southwest corner boundary block')
            print('Block {}: [{} (p{} - p{})] + [{}] + [{} (p{} - p{})] + [{}] + [{}] + [{} (p{} - p{}) - ({})] + [{}] \n'.format((i+1,j+1,k+1), Tx_plus, (i+2,j+1,k+1), (i+1,j+1,k+1), qsc_bW, Ty_plus, (i+1,j+2,k+1), (i+1,j+1,k+1), qsc_bS, qsc_bU, Tz_min, (i+1,j+1,k), (i+1,j+1,k+1), Z_gamma_min, qsc[i,j,k]))
          
          if k!=0 and k!=zi-1:
            # central southwest corner boundary
            # 2 faces. Tx-, Ty-
            print('Central southwest corner boundary block')
            print('Block {}: [{} (p{} - p{})] + [{}] + [{} (p{} - p{})] + [{}] + [{} (p{} - p{}) - ({})] + [{} (p{} - p{}) - ({})] + [{}] \n'.format((i+1,j+1,k+1), Tx_plus, (i+2,j+1,k+1), (i+1,j+1,k+1), qsc_bW, Ty_plus, (i+1,j+2,k+1), (i+1,j+1,k+1), qsc_bS, Tz_plus, (i+1,j+1,k+2), (i+1,j+1,k+1), Z_gamma_plus, Tz_min, (i+1,j+1,k), (i+1,j+1,k+1), Z_gamma_min, qsc[i,j,k]))

        if j==yi-1:
          qsc_bN = boundary_floweq3d(north['type'], 'north', dx, dy, dz, kx, ky, kz, mu, B, rho, north['value'], no_block=(i+1,j+1,k+1), no_blocks_shared=xi*zi)
          if k==0:
            # bottom northwest corner boundary
            # 3 faces. Tx-, Ty+, Tz-            
            qsc_bB = boundary_floweq3d(bottom['type'], 'bottom', dx, dy, dz, kx, ky, kz, mu, B, rho, bottom['value'], no_block=(i+1,j+1,k+1), no_blocks_shared=xi*yi)
            print('Bottom northwest corner boundary block')
            print('Block {}: [{} (p{} - p{})] + [{}] + [{}] + [{} (p{} - p{})] + [{} (p{} - p{}) - ({})] + [{}] + [{}] \n'.format((i+1,j+1,k+1), Tx_plus, (i+2,j+1,k+1), (i+1,j+1,k+1), qsc_bW, qsc_bN, Ty_min, (i+1,j,k+1), (i+1,j+1,k+1), Tz_plus, (i+1,j+1,k+2), (i+1,j+1,k+1), Z_gamma_plus, qsc_bB, qsc[i,j,k]))

          if k==zi-1:
            # upper northwest corner boundary
            # 3 faces. Tx-, Ty+, Tz+            
            qsc_bU = boundary_floweq3d(upper['type'], 'upper', dx, dy, dz, kx, ky, kz, mu, B, rho, upper['value'], no_block=(i+1,j+1,k+1), no_blocks_shared=xi*yi)
            print('Upper northwest corner boundary block')
            print('Block {}: [{} (p{} - p{})] + [{}] + [{}] + [{} (p{} - p{})] + [{}] + [{} (p{} - p{}) - ({})] + [{}] \n'.format((i+1,j+1,k+1), Tx_plus, (i+2,j+1,k+1), (i+1,j+1,k+1), qsc_bW, qsc_bN, Ty_min, (i+1,j,k+1), (i+1,j+1,k+1), qsc_bU, Tz_min, (i+1,j+1,k), (i+1,j+1,k+1), Z_gamma_min, qsc[i,j,k]))
          
          if k!=0 and k!=zi-1:
            # central northwest corner boundary
            # 3 faces. Tx-, Ty+
            print('Central northwest corner boundary block')
            print('Block {}: [{} (p{} - p{})] + [{}] + [{}] + [{} (p{} - p{})] + [{} (p{} - p{}) - ({})] + [{} (p{} - p{}) - ({})] + [{}] \n'.format((i+1,j+1,k+1), Tx_plus, (i+2,j+1,k+1), (i+1,j+1,k+1), qsc_bW, qsc_bN, Ty_min, (i+1,j,k+1), (i+1,j+1,k+1), Tz_plus, (i+1,j+1,k+2), (i+1,j+1,k+1), Z_gamma_plus, Tz_min, (i+1,j+1,k), (i+1,j+1,k+1), Z_gamma_min, qsc[i,j,k]))

        if j!=0 and j!=yi-1:
          if k==0:
            # bottom west boundary
            # 2 faces. Tx-, Tz-
            qsc_bB = boundary_floweq3d(bottom['type'], 'bottom', dx, dy, dz, kx, ky, kz, mu, B, rho, bottom['value'], no_block=(i+1,j+1,k+1), no_blocks_shared=xi*yi)
            print('Bottom west boundary block')
            print('Block {}: [{} (p{} - p{})] + [{}] + [{} (p{} - p{})] + [{} (p{} - p{})] + [{} (p{} - p{}) - ({})] + [{}] + [{}] \n'.format((i+1,j+1,k+1), Tx_plus, (i+2,j+1,k+1), (i+1,j+1,k+1), qsc_bW, Ty_plus, (i+1,j+2,k+1), (i+1,j+1,k+1), Ty_min, (i+1,j,k+1), (i+1,j+1,k+1), Tz_plus, (i+1,j+1,k+2), (i+1,j+1,k+1), Z_gamma_plus, qsc_bB, qsc[i,j,k]))

          if k==zi-1:
            # upper west boundary
            # 2 faces. Tx-, Tz+            
            qsc_bU = boundary_floweq3d(upper['type'], 'upper', dx, dy, dz, kx, ky, kz, mu, B, rho, upper['value'], no_block=(i+1,j+1,k+1), no_blocks_shared=xi*yi)
            print('Upper west boundary block')
            print('Block {}: [{} (p{} - p{})] + [{}] + [{} (p{} - p{})] + [{} (p{} - p{})] + [{}] + [{} (p{} - p{}) - ({})] + [{}] \n'.format((i+1,j+1,k+1), Tx_plus, (i+2,j+1,k+1), (i+1,j+1,k+1), qsc_bW, Ty_plus, (i+1,j+2,k+1), (i+1,j+1,k+1), Ty_min, (i+1,j,k+1), (i+1,j+1,k+1), qsc_bU, Tz_min, (i+1,j+1,k), (i+1,j+1,k+1), Z_gamma_min, qsc[i,j,k]))

          if k!=0 and k!=zi-1:
            # central west boundary
            # 1 face. Tx-
            print('Central west boundary block')
            print('Block {}: [{} (p{} - p{})] + [{}] + [{} (p{} - p{})] + [{} (p{} - p{})] + [{} (p{} - p{}) - ({})] + [{} (p{} - p{}) - ({})] + [{}] \n'.format((i+1,j+1,k+1), Tx_plus, (i+2,j+1,k+1), (i+1,j+1,k+1), qsc_bW, Ty_plus, (i+1,j+2,k+1), (i+1,j+1,k+1), Ty_min, (i+1,j,k+1), (i+1,j+1,k+1), Tz_plus, (i+1,j+1,k+2), (i+1,j+1,k+1), Z_gamma_plus, Tz_min, (i+1,j+1,k), (i+1,j+1,k+1), Z_gamma_min, qsc[i,j,k]))

      ## East Boundaries
      if i==xi-1:
        if j==0:
          qsc_bS = boundary_floweq3d(south['type'], 'south', dx, dy, dz, kx, ky, kz, mu, B, rho, south['value'], no_block=(i+1,j+1,k+1), no_blocks_shared=xi*zi)
          if k==0:
            # bottom southeast corner boundary
            # 3 faces. Tx+, Ty-, Tz-            
            qsc_bB = boundary_floweq3d(bottom['type'], 'bottom', dx, dy, dz, kx, ky, kz, mu, B, rho, bottom['value'], no_block=(i+1,j+1,k+1), no_blocks_shared=xi*yi)
            print('Bottom southeast corner boundary block')
            print('Block {}: [{}] + [{} (p{} - p{})] + [{} (p{} - p{})] + [{}] + [{} (p{} - p{}) - ({})] + [{}] + [{}] \n'.format((i+1,j+1,k+1), qsc_bE, Tx_min, (i,j+1,k+1), (i+1,j+1,k+1), Ty_plus, (i+1,j+2,k+1), (i+1,j+1,k+1), qsc_bS, Tz_plus, (i+1,j+1,k+2), (i+1,j+1,k+1), Z_gamma_plus, qsc_bB, qsc[i,j,k]))

          if k==zi-1:
            # upper southeast corner boundary
            # 3 faces. Tx+, Ty-, Tz+            
            qsc_bU = boundary_floweq3d(upper['type'], 'upper', dx, dy, dz, kx, ky, kz, mu, B, rho, upper['value'], no_block=(i+1,j+1,k+1), no_blocks_shared=xi*yi)
            print('Upper southeast corner boundary block')
            print('Block {}: [{}] + [{} (p{} - p{})] + [{} (p{} - p{})] + [{}] + [{}] + [{} (p{} - p{}) - ({})] + [{}] \n'.format((i+1,j+1,k+1), qsc_bE, Tx_min, (i,j+1,k+1), (i+1,j+1,k+1), Ty_plus, (i+1,j+2,k+1), (i+1,j+1,k+1), qsc_bS, qsc_bU, Tz_min, (i+1,j+1,k), (i+1,j+1,k+1), Z_gamma_min, qsc[i,j,k]))

          if k!=0 and k!=zi-1:
            # central southeast corner boundary
            # 2 faces. Tx+, Ty-
            print('Central southeast corner boundary block')
            print('Block {}: [{}] + [{} (p{} - p{})] + [{} (p{} - p{})] + [{}] + [{} (p{} - p{}) - ({})] + [{} (p{} - p{}) - ({})] + [{}] \n'.format((i+1,j+1,k+1), qsc_bE, Tx_min, (i,j+1,k+1), (i+1,j+1,k+1), Ty_plus, (i+1,j+2,k+1), (i+1,j+1,k+1), qsc_bS, Tz_plus, (i+1,j+1,k+2), (i+1,j+1,k+1), Z_gamma_plus, Tz_min, (i+1,j+1,k), (i+1,j+1,k+1), Z_gamma_min, qsc[i,j,k]))

        if j==yi-1:
          qsc_bN = boundary_floweq3d(north['type'], 'north', dx, dy, dz, kx, ky, kz, mu, B, rho, north['value'], no_block=(i+1,j+1,k+1), no_blocks_shared=xi*zi)
          if k==0:
            # bottom northeast corner boundary
            # 3 faces. Tx+, Ty+, Tz-            
            qsc_bB = boundary_floweq3d(bottom['type'], 'bottom', dx, dy, dz, kx, ky, kz, mu, B, rho, bottom['value'], no_block=(i+1,j+1,k+1), no_blocks_shared=xi*yi)
            print('Bottom northeast corner boundary block')
            print('Block {}: [{}] + [{} (p{} - p{})] + [{}] + [{} (p{} - p{})] + [{} (p{} - p{}) - ({})] + [{}] + [{}] \n'.format((i+1,j+1,k+1), qsc_bE, Tx_min, (i,j+1,k+1), (i+1,j+1,k+1), qsc_bN, Ty_min, (i+1,j,k+1), (i+1,j+1,k+1), Tz_plus, (i+1,j+1,k+2), (i+1,j+1,k+1), Z_gamma_plus, 5, qsc[i,j,k]))

          if k==zi-1:
            # upper northeast corner boundary
            # 3 faces. Tx+, Ty+, Tz+            
            qsc_bU = boundary_floweq3d(upper['type'], 'upper', dx, dy, dz, kx, ky, kz, mu, B, rho, upper['value'], no_block=(i+1,j+1,k+1), no_blocks_shared=xi*yi)
            print('Upper northeast corner boundary block')
            print('Block {}: [{}] + [{} (p{} - p{})] + [{}] + [{} (p{} - p{})] + [{}] + [{} (p{} - p{}) - ({})] + [{}] \n'.format((i+1,j+1,k+1), qsc_bE, Tx_min, (i,j+1,k+1), (i+1,j+1,k+1), qsc_bN, Ty_min, (i+1,j,k+1), (i+1,j+1,k+1), qsc_bU, Tz_min, (i+1,j+1,k), (i+1,j+1,k+1), Z_gamma_min, qsc[i,j,k]))

          if k!=0 and k!=zi-1:
            # central northeast corner boundary
            # 2 faces. Tx+, Ty+
            print('Central northeast corner boundary block')
            print('Block {}: [{}] + [{} (p{} - p{})] + [{}] + [{} (p{} - p{})] + [{} (p{} - p{}) - ({})] + [{} (p{} - p{}) - ({})] + [{}] \n'.format((i+1,j+1,k+1), qsc_bE, Tx_min, (i,j+1,k+1), (i+1,j+1,k+1), qsc_bN, Ty_min, (i+1,j,k+1), (i+1,j+1,k+1), Tz_plus, (i+1,j+1,k+2), (i+1,j+1,k+1), Z_gamma_plus, Tz_min, (i+1,j+1,k), (i+1,j+1,k+1), Z_gamma_min, qsc[i,j,k]))

        if j!=0 and j!=yi-1:
          if k==0:
            # bottom east boundary
            # 2 faces. Tx+, Tz-            
            qsc_bB = boundary_floweq3d(bottom['type'], 'bottom', dx, dy, dz, kx, ky, kz, mu, B, rho, bottom['value'], no_block=(i+1,j+1,k+1), no_blocks_shared=xi*yi)
            print('Bottom east boundary block')
            print('Block {}: [{}] + [{} (p{} - p{})] + [{} (p{} - p{})] + [{} (p{} - p{})] + [{} (p{} - p{}) - ({})] + [{}] + [{}] \n'.format((i+1,j+1,k+1), qsc_bE, Tx_min, (i,j+1,k+1), (i+1,j+1,k+1), Ty_plus, (i+1,j+2,k+1), (i+1,j+1,k+1), Ty_min, (i+1,j,k+1), (i+1,j+1,k+1), Tz_plus, (i+1,j+1,k+2), (i+1,j+1,k+1), Z_gamma_plus, qsc_bB, qsc[i,j,k]))

          if k==zi-1:
            # upper east boundary
            # 2 faces. Tx+, Tz+            
            qsc_bU = boundary_floweq3d(upper['type'], 'upper', dx, dy, dz, kx, ky, kz, mu, B, rho, upper['value'], no_block=(i+1,j+1,k+1), no_blocks_shared=xi*yi)
            print('Upper east boundary block')
            print('Block {}: [{}] + [{} (p{} - p{})] + [{} (p{} - p{})] + [{} (p{} - p{})] + [{}] + [{} (p{} - p{}) - ({})] + [{}] \n'.format((i+1,j+1,k+1), qsc_bE, Tx_min, (i,j+1,k+1), (i+1,j+1,k+1), Ty_plus, (i+1,j+2,k+1), (i+1,j+1,k+1), Ty_min, (i+1,j,k+1), (i+1,j+1,k+1), qsc_bU, Tz_min, (i+1,j+1,k), (i+1,j+1,k+1), Z_gamma_min, qsc[i,j,k]))

          if k!=0 and k!=zi-1:
            # central east boundary
            # 1 face. Tx+
            print('Central east boundary block')
            print('Block {}: [{}] + [{} (p{} - p{})] + [{} (p{} - p{})] + [{} (p{} - p{})] + [{} (p{} - p{}) - ({})] + [{} (p{} - p{}) - ({})] + [{}] \n'.format((i+1,j+1,k+1), qsc_bE, Tx_min, (i,j+1,k+1), (i+1,j+1,k+1), Ty_plus, (i+1,j+2,k+1), (i+1,j+1,k+1), Ty_min, (i+1,j,k+1), (i+1,j+1,k+1), Tz_plus, (i+1,j+1,k+2), (i+1,j+1,k+1), Z_gamma_plus, Tz_min, (i+1,j+1,k), (i+1,j+1,k+1), Z_gamma_min, qsc[i,j,k]))

      ## North, South, Bottom, Upper Boundaries and Interior Blocks
      if i!=0 and i!=xi-1:
        if j==0:
          qsc_bS = boundary_floweq3d(south['type'], 'south', dx, dy, dz, kx, ky, kz, mu, B, rho, south['value'], no_block=(i+1,j+1,k+1), no_blocks_shared=xi*zi)
          if k==0:
            # bottom south boundary
            # 2 faces. Ty-, Tz-            
            qsc_bB = boundary_floweq3d(bottom['type'], 'bottom', dx, dy, dz, kx, ky, kz, mu, B, rho, bottom['value'], no_block=(i+1,j+1,k+1), no_blocks_shared=xi*yi)
            print('Bottom south boundary block')
            print('Block {}: [{} (p{} - p{})] + [{} (p{} - p{})] + [{} (p{} - p{})] + [{}] + [{} (p{} - p{}) - ({})] + [{}] + [{}] \n'.format((i+1,j+1,k+1), Tx_plus, (i+2,j+1,k+1), (i+1,j+1,k+1), Tx_min, (i,j+1,k+1), (i+1,j+1,k+1), Ty_plus, (i+1,j+2,k+1), (i+1,j+1,k+1), qsc_bS, Tz_plus, (i+1,j+1,k+2), (i+1,j+1,k+1), Z_gamma_plus, qsc_bB, qsc[i,j,k]))

          if k==zi-1:
            # upper south boundary
            # 2 faces. Ty-, Tz+            
            qsc_bU = boundary_floweq3d(upper['type'], 'upper', dx, dy, dz, kx, ky, kz, mu, B, rho, upper['value'], no_block=(i+1,j+1,k+1), no_blocks_shared=xi*yi)
            print('Upper south boundary block')
            print('Block {}: [{} (p{} - p{})] + [{} (p{} - p{})] + [{} (p{} - p{})] + [{}] + [{}] + [{} (p{} - p{}) - ({})] + [{}] \n'.format((i+1,j+1,k+1), Tx_plus, (i+2,j+1,k+1), (i+1,j+1,k+1), Tx_min, (i,j+1,k+1), (i+1,j+1,k+1), Ty_plus, (i+1,j+2,k+1), (i+1,j+1,k+1), qsc_bS, qsc_bU, Tz_min, (i+1,j+1,k), (i+1,j+1,k+1), Z_gamma_min, qsc[i,j,k]))

          if k!=0 and k!=zi-1:
            # central south boundary
            # 1 face. Ty-
            print('Central south boundary block')
            print('Block {}: [{} (p{} - p{})] + [{} (p{} - p{})] + [{} (p{} - p{})] + [{}] + [{} (p{} - p{}) - ({})] + [{} (p{} - p{}) - ({})] + [{}] \n'.format((i+1,j+1,k+1), Tx_plus, (i+2,j+1,k+1), (i+1,j+1,k+1), Tx_min, (i,j+1,k+1), (i+1,j+1,k+1), Ty_plus, (i+1,j+2,k+1), (i+1,j+1,k+1), qsc_bS, Tz_plus, (i+1,j+1,k+2), (i+1,j+1,k+1), Z_gamma_plus, Tz_min, (i+1,j+1,k), (i+1,j+1,k+1), Z_gamma_min, qsc[i,j,k]))

        if j==yi-1:
          qsc_bN = boundary_floweq3d(north['type'], 'north', dx, dy, dz, kx, ky, kz, mu, B, rho, north['value'], no_block=(i+1,j+1,k+1), no_blocks_shared=xi*zi)
          if k==0:
            # bottom north boundary
            # 2 faces. Ty+, Tz-            
            qsc_bB = boundary_floweq3d(bottom['type'], 'bottom', dx, dy, dz, kx, ky, kz, mu, B, rho, bottom['value'], no_block=(i+1,j+1,k+1), no_blocks_shared=xi*yi)
            print('Bottom north boundary block')
            print('Block {}: [{} (p{} - p{})] + [{} (p{} - p{})] + [{}] + [{} (p{} - p{})] + [{} (p{} - p{}) - ({})] + [{}] + [{}] \n'.format((i+1,j+1,k+1), Tx_plus, (i+2,j+1,k+1), (i+1,j+1,k+1), Tx_min, (i,j+1,k+1), (i+1,j+1,k+1), qsc_bN, Ty_min, (i+1,j,k+1), (i+1,j+1,k+1), Tz_plus, (i+1,j+1,k+2), (i+1,j+1,k+1), Z_gamma_plus, qsc_bB, qsc[i,j,k]))

          if k==zi-1:
            # upper north boundary
            # 2 faces. Ty+, Tz+            
            qsc_bU = boundary_floweq3d(upper['type'], 'upper', dx, dy, dz, kx, ky, kz, mu, B, rho, upper['value'], no_block=(i+1,j+1,k+1), no_blocks_shared=xi*yi)
            print('Upper north boundary block')
            print('Block {}: [{} (p{} - p{})] + [{} (p{} - p{})] + [{}] + [{} (p{} - p{})] + [{}] + [{} (p{} - p{}) - ({})] + [{}] \n'.format((i+1,j+1,k+1), Tx_plus, (i+2,j+1,k+1), (i+1,j+1,k+1), Tx_min, (i,j+1,k+1), (i+1,j+1,k+1), qsc_bN, Ty_min, (i+1,j,k+1), (i+1,j+1,k+1), qsc_bU, Tz_min, (i+1,j+1,k), (i+1,j+1,k+1), Z_gamma_min, qsc[i,j,k]))

          if k!=0 and k!=zi-1:
            # central north boundary
            # 1 face. Ty+
            print('Central north boundary block')
            print('Block {}: [{} (p{} - p{})] + [{} (p{} - p{})] + [{}] + [{} (p{} - p{})] + [{} (p{} - p{}) - ({})] + [{} (p{} - p{}) - ({})] + [{}] \n'.format((i+1,j+1,k+1), Tx_plus, (i+2,j+1,k+1), (i+1,j+1,k+1), Tx_min, (i,j+1,k+1), (i+1,j+1,k+1), qsc_bN, Ty_min, (i+1,j,k+1), (i+1,j+1,k+1), Tz_plus, (i+1,j+1,k+2), (i+1,j+1,k+1), Z_gamma_plus, Tz_min, (i+1,j+1,k), (i+1,j+1,k+1), Z_gamma_min, qsc[i,j,k]))

        if j!=0 and j!=yi-1:
          if k==0:
            # bottom boundary
            # 1 face. Tz-            
            qsc_bB = boundary_floweq3d(bottom['type'], 'bottom', dx, dy, dz, kx, ky, kz, mu, B, rho, bottom['value'], no_block=(i+1,j+1,k+1), no_blocks_shared=xi*yi)
            print('Bottom boundary block')
            print('Block {}: [{} (p{} - p{})] + [{} (p{} - p{})] + [{} (p{} - p{})] + [{} (p{} - p{})] + [{} (p{} - p{}) - ({})] + [{}] + [{}] \n'.format((i+1,j+1,k+1), Tx_plus, (i+2,j+1,k+1), (i+1,j+1,k+1), Tx_min, (i,j+1,k+1), (i+1,j+1,k+1), Ty_plus, (i+1,j+2,k+1), (i+1,j+1,k+1), Ty_min, (i+1,j,k+1), (i+1,j+1,k+1), Tz_plus, (i+1,j+1,k+2), (i+1,j+1,k+1), Z_gamma_plus, qsc_bB, qsc[i,j,k]))

          if k==zi-1:
            # upper boundary
            # 1 face. Tz+            
            qsc_bU = boundary_floweq3d(upper['type'], 'upper', dx, dy, dz, kx, ky, kz, mu, B, rho, upper['value'], no_block=(i+1,j+1,k+1), no_blocks_shared=xi*yi)
            print('Upper boundary block')
            print('Block {}: [{} (p{} - p{})] + [{} (p{} - p{})] + [{} (p{} - p{})] + [{} (p{} - p{})] + [{}] + [{} (p{} - p{}) - ({})] + [{}] \n'.format((i+1,j+1,k+1), Tx_plus, (i+2,j+1,k+1), (i+1,j+1,k+1), Tx_min, (i,j+1,k+1), (i+1,j+1,k+1), Ty_plus, (i+1,j+2,k+1), (i+1,j+1,k+1), Ty_min, (i+1,j,k+1), (i+1,j+1,k+1), qsc_bU, Tz_min, (i+1,j+1,k), (i+1,j+1,k+1), Z_gamma_min, qsc[i,j,k]))

          if k!=0 and k!=zi-1:
            # interior blocks
            # 0 face. Flow totally inter-block, no contact to boundaries.
            print('Interior block')
            print('Block {}: [{} (p{} - p{})] + [{} (p{} - p{})] + [{} (p{} - p{})] + [{} (p{} - p{})] + [{} (p{} - p{}) - ({})] + [{} (p{} - p{}) - ({})] + [{}] \n'.format((i+1,j+1,k+1), Tx_plus, (i+2,j+1,k+1), (i+1,j+1,k+1), Tx_min, (i,j+1,k+1), (i+1,j+1,k+1), Ty_plus, (i+1,j+2,k+1), (i+1,j+1,k+1), Ty_min, (i+1,j,k+1), (i+1,j+1,k+1), Tz_plus, (i+1,j+1,k+2), (i+1,j+1,k+1), Z_gamma_plus, Tz_min, (i+1,j+1,k), (i+1,j+1,k+1), Z_gamma_min, qsc[i,j,k]))
