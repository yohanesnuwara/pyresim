"""
Simulation in 1D Homogeneous Rectangular Reservoir Grids 

@author: Yohanes Nuwara
@email: ign.nuwara97@gmail.com
"""

from boundary_homogeneous import *
from transmissibility_homogeneous import *
from utilities_homogeneous import *

"""""""""""
INPUT
"""""""""""

# number of blocks
xi = 5

# define parameters, in this case blocks are homogeneous and same in size
dx = 1000 # ft
dy = 1200
dz = 75
kx = 15 # md
B = 1 # RB/STB
mu = 10 # cp

# source term
xsc = np.array([4]) # location of block where production / injection well is located
q = np.array([-150]) # flow rate of production / injection

# boundary conditions
p_bW = 5000 # pressure at left (West) boundary
q_bE = 0. # flow rate at right (East) boundary

"""""""""""
MAIN CODE
"""""""""""

" Create property grids "
# blocks location
block = np.arange(1, xi+1)

# source block (production or injection well)
qsc = source1d(q, xsc, xi) # call function HERE

" Produce flow equation "

print('Left-Hand Side (RHS) of Flow equation in each grid block')
print('1st term: Flow in X-direction from next block (Tx+)')
print('2nd term: Flow in X-direction from previous block (Tx-)')
print('3rd term: Source accumulation \n')

for i in range(len(block)):

  T_min, T_plus = transmissibility1d(dx, dy, dz, kx, mu, B)

  if i == 0:
    # constant pressure at left boundary
    qsc_b = boundary_floweq1d('constant_pressure', dx, dy, dz, kx, mu, B, value=p_bW, no_block=block[i])
    print('Boundary Block {}: {} (p{} - p{}) + {} + {}'.format(block[i], T_plus, block[i+1], block[i], qsc_b, qsc[i]))
  elif i == len(block)-1:
    # no flow at right boundary
    qsc_b = boundary_floweq1d('constant_rate', dx, dy, dz, kx, mu, B, value=q_bE, no_block=block[i])
    print('Boundary Block {}: {} (p{} - p{}) + {} + {}'.format(block[i], T_min, block[i-1], block[i], qsc_b, qsc[i]))
  else:
    print('Interior Block {}: {} (p{} - p{}) + {} (p{} - p{}) + {}'.format(block[i], T_min, block[i-1], block[i], T_plus, block[i+1], block[i], qsc[i]))
