"""
Simulation in 2D Rectangular Reservoir Grids

@author: Yohanes Nuwara
@email: ign.nuwara97@gmail.com
"""

xi = 4; yi = 3 # number of blocks in x and y

# create block coordinates (Engineering Notation convention in Abou-Kassem)
x_ = np.arange(1, xi+1)
y_ = np.arange(1, yi+1)

x, y = np.meshgrid(x_, y_, indexing='ij')

# plot grid points
plt.scatter(x, y)

# Python starts indexing from 0. So, block 1,1 refers to [0,0], block 2,1
# refers to [1,0] and so on. In other words, block i,j refers to [i-1,j-1]

# print('Block {},{}'.format(x[2,1], y[2,1])) # print block 3,2

# define parameters, in this case blocks are homogeneous and same in size
dx = 250 # ft
dy = 300
dz = 100
kx = 270 # md
ky = 220
B = 1 # RB/STB
mu = 2 # cp

# assign all params to all blocks
dx = np.array([[dx]*yi]*xi)
dy = np.array([[dy]*yi]*xi)
dz = np.array([[dz]*yi]*xi)
kx = np.array([[kx]*yi]*xi)
ky = np.array([[ky]*yi]*xi)
B = np.array([[B]*yi]*xi)
mu = np.array([[mu]*yi]*xi)

# source term
xsc = 3; ysc = 2 # grid point (x and y coordinate) of the source 
q = -4000 

qsc = np.array([[0]*yi]*xi) # initiate with zeros
qsc[xsc-1,ysc-1] = q # inject the source to block 3,2

# plot the injected grid point
plt.scatter(x[xsc-1,ysc-1], y[xsc-1,ysc-1], color='red')

# boundary blocks
q_bN = -500 # flow rate at North boundary
p_bS = 3000 # pressure at South boundary
q_bW = 0 # flow rate at West boundary
pg_bE = .1 # pressure gradient at East boundary

print('Left-Hand Side (RHS) of Flow equation in each block')
print('1st term: Flow in X-direction from next block (Tx+)')
print('2nd term: Flow in X-direction from previous block (Tx-)')
print('3rd term: Flow in Y-direction from next block (Ty+)')
print('4th term: Flow in Y-direction from previous block (Ty-)')
print('5th term: Source accumulation \n')

for i in range(xi):
  for j in range(yi):

    Ax = dy[i,j] * dz[i,j]
    Ay = dx[i,j] * dz[i,j]

    # flow to x direction
    Tx_min = .001127 * (kx[i,j] * Ax) / (mu[i,j] * B[i,j] * dx[i,j])
    Tx_plus = Tx_min

    # flow to y direction
    Ty_min = .001127 * (ky[i,j] * Ay) / (mu[i,j] * B[i,j] * dy[i,j])
    Ty_plus = Ty_min 

    if i==0:
      # boundaries in the West
      qsc_bW = constant_rate_bc2d(Tx_min, 0, yi)

      if j==0:
        # southwest boundary has two face boundaries (cons press & no flow)
        # Tx- and Ty- are flow from boundaries
        qsc_bS = constant_pressure_bc1d((i+1,j+1), p_bS, dx[i,j], dz[i,j], ky[i,j], dy[i,j], mu[i,j], B[i,j])
        print('southwest corner block {}'.format((i+1,j+1)))  
        print('Boundary Block {}: {} (p{} - p{}) + {} + {} (p{} - p{}) + {} + {} \n'.format((i+1,j+1), Tx_plus, (i+2,j+1), (i+1,j+1), qsc_bW, Ty_plus, (i+1,j+2), (i+1,j+1), qsc_bS, qsc[i,j]))         

      if j==yi-1:
        # northwest boundary has two face boundaries (cons rate & cons press)
        # Tx- and Ty+ are flow from boundaries
        qsc_bN = constant_rate_bc2d(Ty_plus, q_bN, xi)
        print('northwest corner block {}'.format((i+1,j+1)))
        print('Boundary Block {}: {} (p{} - p{}) + {} + {} + {} (p{} - p{}) + {} \n'.format((i+1,j+1), Tx_plus, (i+2,j+1), (i+1,j+1), qsc_bW, qsc_bN, Ty_min, (i+1,j), (i+1,j+1), qsc[i,j]))         


      else:
        if j!=0 and j!=yi-1:
          # west boundary has no flow
          # Tx+ is flow from boundary
          print('west block {}'.format((i+1,j+1)))   
          print('Boundary Block {}: {} (p{} - p{}) + {} + {} (p{} - p{}) + {} (p{} - p{}) + {} \n'.format((i+1,j+1), Tx_plus, (i+2,j+1), (i+1,j+1), qsc_bW, Ty_plus, (i+1,j+2), (i+1,j+1), Ty_min, (i+1,j), (i+1,j+1), qsc[i,j]))         
    
    elif i==xi-1:
      # boundaries in the East
      qsc_bE = constant_pressuregrad_bc1d('east', pg_bE, dy[i,j], dz[i,j], kx[i,j], mu[i,j], B[i,j])

      if j==0:
        # southeast boundary has two face boundaries (cons press grad & cons press)
        # Tx+ and Ty- are flow from boundaries
        qsc_bS = constant_pressure_bc1d((i+1,j+1), p_bS, dx[i,j], dz[i,j], ky[i,j], dy[i,j], mu[i,j], B[i,j])
        print('southeast corner block {}'.format((i+1,j+1)))
        print('Boundary Block {}: {} + {} (p{} - p{}) + {} (p{} - p{}) + {} + {} \n'.format(block[i], qsc_bE, Tx_min, (i,j+1), (i+1,j+1), Ty_plus, (i+1,j+2), (i+1,j+1), qsc_bS, qsc[i,j]))

      if j==yi-1:
        # northeast boundary has two face boundaries (cons press grad & cons rate)
        # Tx+ and Ty+ are flow from boundaries
        qsc_bN = constant_rate_bc2d(Ty_plus, q_bN, xi)
        print('northeast corner block {}'.format((i+1,j+1))) 
        print('Boundary Block {}: {} + {} (p{} - p{}) + {} + {} (p{} - p{}) + {} \n'.format(block[i], qsc_bE, Tx_min, (i,j+1), (i+1,j+1), qsc_bN, Ty_min, (i+1,j), (i+1,j+1), qsc[i,j]))

      else:
        if j!=0 and j!=yi-1:
          # east boundary has constant pressure gradient
          # Tx- is flow from boundary
          print('east block {}'.format((i+1,j+1)))  
          print('Boundary Block {}: {} + {} (p{} - p{}) + {} (p{} - p{}) + {} (p{} - p{}) + {} \n'.format(block[i], qsc_bE, Tx_min, (i,j+1), (i+1,j+1), Ty_plus, (i+1,j+2), (i+1,j+1), Ty_min, (i+1,j), (i+1,j+1), qsc[i,j]))


    elif i!=0 and i!=xi-1:
      if j==0:
        # south boundary has constant pressure 
        # Ty- is flow from boundary
        qsc_bS = constant_pressure_bc1d((i+1,j+1), p_bS, dx[i,j], dz[i,j], ky[i,j], dy[i,j], mu[i,j], B[i,j])
        print('south block {}'.format((i+1,j+1)))
        print('Boundary block {}: {} (p{} - p{}) + {} (p{} - p{}) + {} (p{} - p{}) + {} + {} \n'.format((i+1, j+1), Tx_plus, (i, j+1), (i+1, j+1), Tx_min, (i+2, j+1), (i+1, j+1), Ty_plus, (i+1, j+2), (i+1,j+1), qsc_bS, qsc[i,j]))

      if j==yi-1:  
        # north boundary has constant flow rate
        # Ty+ is flow from boundary        
        qsc_bN = constant_rate_bc2d(Ty_plus, q_bN, xi)
        print('north block {}'.format((i+1,j+1)))           
        print('Boundary block {}: {} (p{} - p{}) + {} (p{} - p{}) + {} + {} (p{} - p{}) + {} \n'.format((i+1, j+1), Tx_plus, (i, j+1), (i+1, j+1), Tx_min, (i+2, j+1), (i+1, j+1), qsc_bN, Ty_min, (i+1, j), (i+1,j+1), qsc[i,j]))

      else:
        if j!=0 and j!=yi-1:
          # the interior blocks
          # no boundary flow
          print('interior block {}'.format((i+1,j+1)))
          print('Interior block {}: {} (p{} - p{}) + {} (p{} - p{}) + {} (p{} - p{}) + {} (p{} - p{}) + {} \n'.format((i+1, j+1), Tx_plus, (i, j+1), (i+1, j+1), Tx_min, (i+2, j+1), (i+1, j+1), Ty_plus, (i+1, j+2), (i+1, j+1), Ty_min, (i+1, j), (i+1,j+1), qsc[i,j]))
