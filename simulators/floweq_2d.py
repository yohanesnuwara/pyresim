"""
Simulation in 2D Rectangular Reservoir Grids

@author: Yohanes Nuwara
@email: ign.nuwara97@gmail.com
"""

from boundary_homogeneous import *
from transmissibility_homogeneous import *
from utilities_homogeneous import *

"""""""""""
INPUT
"""""""""""

# number of blocks in x and y
xi = 4; yi = 3 

# define parameters, in this case blocks are homogeneous and same in size
dx = 250 # ft
dy = 300
dz = 100
kx = 270 # md
ky = 220
B = 1 # RB/STB
mu = 2 # cp

# source term
xysc = np.array([(3,2)]) # coordinate of source (x,y)
q = np.array([-4000]) # flow rate

# boundary conditions

east = {"type": "constant_pressuregrad", "value": 0.1}
west = {"type": "no_flow", "value": 0}
north = {"type": "constant_rate", "value": -500}
south = {"type": "constant_pressure", "value": 3000}

"""""""""""
MAIN CODE
"""""""""""

# source term
qsc = source2d(q, xysc, xi, yi)

# " Produce flow equations "

print('Left-Hand Side (RHS) of Flow equation in each block')
print('1st term: Flow in X-direction from next block (Tx+)')
print('2nd term: Flow in X-direction from previous block (Tx-)')
print('3rd term: Flow in Y-direction from next block (Ty+)')
print('4th term: Flow in Y-direction from previous block (Ty-)')
print('5th term: Source accumulation \n')

for i in range(xi):
  for j in range(yi):

    Tx_min, Tx_plus, Ty_min, Ty_plus = transmissibility2d(dx, dy, dz, kx, ky, mu, B) 

    if i==0:
      # boundaries in the West (no flow)
      # qsc_bW = 0
      qsc_bW = boundary_floweq2d(west['type'], 'west', dx, dy, dz, kx, ky, mu, B, value=west['value'], no_block=(i+1,j+1), no_blocks_shared=yi)

      if j==0:
        # southwest boundary has two face boundaries (cons press & no flow)
        # Tx- and Ty- are flow from boundaries
        qsc_bS = boundary_floweq2d(south['type'], 'south', dx, dy, dz, kx, ky, mu, B, value=south['value'], no_block=(i+1,j+1), no_blocks_shared=xi)
        print('southwest corner block {}'.format((i+1,j+1)))  
        print('Boundary Block {}: {} (p{} - p{}) + {} + {} (p{} - p{}) + {} + {} \n'.format((i+1,j+1), Tx_plus, (i+2,j+1), (i+1,j+1), qsc_bW, Ty_plus, (i+1,j+2), (i+1,j+1), qsc_bS, qsc[i,j]))         

      if j==yi-1:
        # northwest boundary has two face boundaries (cons rate & no flow)
        # Tx- and Ty+ are flow from boundaries
        qsc_bN = boundary_floweq2d(north['type'], 'north', dx, dy, dz, kx, ky, mu, B, value=north['value'], no_block=(i+1,j+1), no_blocks_shared=xi)
        print('northwest corner block {}'.format((i+1,j+1)))
        print('Boundary Block {}: {} (p{} - p{}) + {} + {} + {} (p{} - p{}) + {} \n'.format((i+1,j+1), Tx_plus, (i+2,j+1), (i+1,j+1), qsc_bW, qsc_bN, Ty_min, (i+1,j), (i+1,j+1), qsc[i,j]))         

      else:
        if j!=0 and j!=yi-1:
          # west boundary has no flow
          # Tx- is flow from boundary
          print('west block {}'.format((i+1,j+1)))   
          print('Boundary Block {}: {} (p{} - p{}) + {} + {} (p{} - p{}) + {} (p{} - p{}) + {} \n'.format((i+1,j+1), Tx_plus, (i+2,j+1), (i+1,j+1), qsc_bW, Ty_plus, (i+1,j+2), (i+1,j+1), Ty_min, (i+1,j), (i+1,j+1), qsc[i,j]))         
    
    elif i==xi-1:
      # boundaries in the East
      qsc_bE = boundary_floweq2d(east['type'], 'east', dx, dy, dz, kx, ky, mu, B, value=east['value'], no_block=(i+1,j+1), no_blocks_shared=yi)

      if j==0:
        # southeast boundary has two face boundaries (cons press grad & cons press)
        # Tx+ and Ty- are flow from boundaries
        qsc_bS = boundary_floweq2d(south['type'], 'south', dx, dy, dz, kx, ky, mu, B, value=south['value'], no_block=(i+1,j+1), no_blocks_shared=xi)
        print('southeast corner block {}'.format((i+1,j+1)))
        print('Boundary Block {}: {} + {} (p{} - p{}) + {} (p{} - p{}) + {} + {} \n'.format((i+1,j+1), qsc_bE, Tx_min, (i,j+1), (i+1,j+1), Ty_plus, (i+1,j+2), (i+1,j+1), qsc_bS, qsc[i,j]))

      if j==yi-1:
        # northeast boundary has two face boundaries (cons press grad & cons rate)
        # Tx+ and Ty+ are flow from boundaries
        qsc_bN = boundary_floweq2d(north['type'], 'north', dx, dy, dz, kx, ky, mu, B, value=north['value'], no_block=(i+1,j+1), no_blocks_shared=xi)
        print('northeast corner block {}'.format((i+1,j+1))) 
        print('Boundary Block {}: {} + {} (p{} - p{}) + {} + {} (p{} - p{}) + {} \n'.format((i+1,j+1), qsc_bE, Tx_min, (i,j+1), (i+1,j+1), qsc_bN, Ty_min, (i+1,j), (i+1,j+1), qsc[i,j]))

      else:
        if j!=0 and j!=yi-1:
          # east boundary has constant pressure gradient
          # Tx+ is flow from boundary
          print('east block {}'.format((i+1,j+1)))  
          print('Boundary Block {}: {} + {} (p{} - p{}) + {} (p{} - p{}) + {} (p{} - p{}) + {} \n'.format((i+1,j+1), qsc_bE, Tx_min, (i,j+1), (i+1,j+1), Ty_plus, (i+1,j+2), (i+1,j+1), Ty_min, (i+1,j), (i+1,j+1), qsc[i,j]))

    elif i!=0 and i!=xi-1:
      if j==0:
        # south boundary has constant pressure 
        # Ty- is flow from boundary
        qsc_bS = boundary_floweq2d(south['type'], 'south', dx, dy, dz, kx, ky, mu, B, value=south['value'], no_block=(i+1,j+1), no_blocks_shared=xi)
        print('south block {}'.format((i+1,j+1)))
        print('Boundary block {}: {} (p{} - p{}) + {} (p{} - p{}) + {} (p{} - p{}) + {} + {} \n'.format((i+1, j+1), Tx_plus, (i, j+1), (i+1, j+1), Tx_min, (i+2, j+1), (i+1, j+1), Ty_plus, (i+1, j+2), (i+1,j+1), qsc_bS, qsc[i,j]))

      if j==yi-1:  
        # north boundary has constant flow rate
        # Ty+ is flow from boundary        
        qsc_bN = boundary_floweq2d(north['type'], 'north', dx, dy, dz, kx, ky, mu, B, value=north['value'], no_block=(i+1,j+1), no_blocks_shared=xi)
        print('north block {}'.format((i+1,j+1)))           
        print('Boundary block {}: {} (p{} - p{}) + {} (p{} - p{}) + {} + {} (p{} - p{}) + {} \n'.format((i+1, j+1), Tx_plus, (i, j+1), (i+1, j+1), Tx_min, (i+2, j+1), (i+1, j+1), qsc_bN, Ty_min, (i+1, j), (i+1,j+1), qsc[i,j]))

      else:
        if j!=0 and j!=yi-1:
          # the interior blocks
          # no boundary flow
          print('interior block {}'.format((i+1,j+1)))
          print('Interior block {}: {} (p{} - p{}) + {} (p{} - p{}) + {} (p{} - p{}) + {} (p{} - p{}) + {} \n'.format((i+1, j+1), Tx_plus, (i, j+1), (i+1, j+1), Tx_min, (i+2, j+1), (i+1, j+1), Ty_plus, (i+1, j+2), (i+1, j+1), Ty_min, (i+1, j), (i+1,j+1), qsc[i,j]))
