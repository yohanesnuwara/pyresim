"""
2D Simulation to calculate wellblock geometric factor, prorate (production rate), and FBHP
(Given the different operating conditions of the wells)

@author: Yohanes Nuwara
@email: ign.nuwara97@gmail.com
"""

from wellblock import *
from irregular_grid import *

" Input "

xi = 6; yi = 6

# define grid point location of inactive blocks
xy_inactive = [(1,6)]

# wellbore diameter
dw = 7
rw = (0.5 * dw) / 12 # inch to ft

## the COMPLETE grids (2D array)
dx_complete = np.tile([200, 300, 350, 250, 300, 400], yi)
dy_complete = np.repeat([250, 350, 450, 200, 150, 250], xi)
dz_complete = np.full(36, 40)

kx_ = np.array([73, 86, 99, 128, 137, 156])
ky_ = np.array([65, 88, 117, 142, 121, 106])

# well information
well_config = {'A': 0, 'B': 1, 'C': 1, 'D': 2, 'E': 2, 'F': 3, 'G': 3, 'H': 3, 
               'I': 3, 'J': 3, 'K': 0}

well_loc = {'A': (2,4), 'B': (2,1), 'C': (5,6), 'D': (6,3), 'E': (1,4), 
            'F': (6,1), 'G': (6,6), 'H': (2,6), 'I': (1,5), 'J': (1,1), 
            'K': (4,3)}

well_rw = {'A': rw, 'B': rw, 'C': rw, 'D': rw, 'E': rw, 'F': rw, 'G': rw, 'H': rw, 
           'I': rw, 'J': rw, 'K': rw}

" Create grid points "

# gridblocks

## meshgrid the original points
x_ = np.arange(1, xi+1)
y_ = np.arange(1, yi+1)
x, y = np.meshgrid(x_, y_, indexing='ij')
kx, ky = np.meshgrid(kx_, ky_, indexing='ij')

## call function create_irregular_grid
x, y, x_inactive, y_inactive = create_irregular_grid(x, y, xy_inactive)

" Create property grids "

# handle the COMPLETE grids, call function maskout_inactive_blocks
dx = maskout_inactive_blocks(dx_complete, x_inactive, y_inactive, xi)
dy = maskout_inactive_blocks(dy_complete, x_inactive, y_inactive, xi)
dz = maskout_inactive_blocks(dz_complete, x_inactive, y_inactive, xi)
kx = maskout_inactive_blocks(kx.T, x_inactive, y_inactive, xi)
ky = maskout_inactive_blocks(ky.T, x_inactive, y_inactive, xi)

# plt.imshow(dx)
# plt.gca().xaxis.tick_top()
# plt.show()

" Calculate wellblock geometric factor "

for i in well_config:
  xloc = well_loc[i][0]
  yloc = well_loc[i][1]
  xsc = xloc - 1; ysc = yloc - 1
  kh, r_eq, Gw = fraction_wellblock_geometric_factor(dx[xsc, ysc], dy[xsc,ysc], kx[xsc,ysc], ky[xsc,ysc], 0, well_rw[i], dz[xsc,ysc], well_config[i])
  print('Well {}: {}'.format(i, Gw))
