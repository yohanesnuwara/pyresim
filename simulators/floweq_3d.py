"""
Simulation in 3D Rectangular Reservoir Grids

@author: Yohanes Nuwara
@email: ign.nuwara97@gmail.com
"""

xi = 4; yi = 3; zi = 3 # number of blocks in x, y, z

# create block coordinates (Engineering Notation convention in Abou-Kassem)
x_ = np.arange(1, xi+1)
y_ = np.arange(1, yi+1)
z_ = np.arange(1, zi+1)

# meshgrid the block coordinates
x, y, z = np.meshgrid(x_, y_, z_, indexing='ij')

# print('Block {},{},{}'.format(x[2,1,1], y[2,1,1], z[2,1,1]))

# plot the grid points
# fig = plt.figure(figsize = (10, 7)) 
# ax = plt.axes(projection ="3d") 
# ax.scatter3D(x, y, z)
# # ax.scatter3D(x[2,1,1], y[2,1,1], z[2,1,1], s=50, color='red')
# plt.show()

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

# boundary conditions
pg_bB = -0.5 # bottom, cons press grad psi/ft
p_bU = 3000 # upper, cons press psi
q_bW = 0 # west, no flow
q_bE = -200 # east, cons flow rate STB/D
q_bS = 100 # south, cons flow rate STB/D
p_bN = 1500 # north, cons press psi 

# assign all params to all blocks
# why yi*xi? Python describes a 3D array as (z, rows, columns), OR (z,y,x)
dx = np.array([[[dx]*zi]*yi]*xi)
dy = np.array([[[dy]*zi]*yi]*xi)
dz = np.array([[[dz]*zi]*yi]*xi)
kx = np.array([[[kx]*zi]*yi]*xi)
ky = np.array([[[ky]*zi]*yi]*xi)
kz = np.array([[[kz]*zi]*yi]*xi)
B = np.array([[[B]*zi]*yi]*xi)
mu = np.array([[[mu]*zi]*yi]*xi)
rho = np.array([[[rho]*zi]*yi]*xi)

# source term

# define the x and y reservoir coordinates 
xsc = np.array([3, 2, 4, 2])
ysc = np.array([2, 1, 1, 1])
zsc = np.array([2, 3, 1, 1])

# Python starts indexing from 0. So, block 1,1 refers to [0,0], block 2,1
# refers to [1,0] and so on. In other words, block i,j refers to [i-1,j-1]
xsc = xsc - 1; ysc = ysc - 1; zsc = zsc - 1

# define rate of each source term 
q = np.array([-133.3, 100, -25, 50]) 

# initiate with zeros. same method with above dx, dy, kx, ky, etc.
qsc = np.array([[[0]*zi]*yi]*xi)

# replace the zeros at coordinate of source term, with the rate of source term
for i, j, k, l in zip(xsc, ysc, zsc, range(len(q))):
  qsc[i][j][k] = q[l]

# # plot the injected grid point
# for i, j, k in zip(xsc, ysc, zsc):
#   ax.scatter3D(x[i,j,k], y[i,j,k], z[i,j,k], s=50, color='red')

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

      Ax = dy[i,j,k] * dz[i,j,k]
      Ay = dx[i,j,k] * dz[i,j,k]
      Az = dx[i,j,k] * dy[i,j,k]

      # flow to x direction
      Tx_min = .001127 * (kx[i,j,k] * Ax) / (mu[i,j,k] * B[i,j,k] * dx[i,j,k])
      Tx_plus = Tx_min

      # flow to y direction
      Ty_min = .001127 * (ky[i,j,k] * Ay) / (mu[i,j,k] * B[i,j,k] * dy[i,j,k])
      Ty_plus = Ty_min 

      # flow to y direction
      Tz_min = .001127 * (kz[i,j,k] * Az) / (mu[i,j,k] * B[i,j,k] * dz[i,j,k])
      Tz_plus = Tz_min

      # in 3D case (unlike 1D, 2D), the term γ is not neglected, because there is Z
      # for example: block (3,2,1) and block (3,2,2) has Z = -33.33 ft
      # block (3,2,3) and block (3,2,2) has Z = 33.33 ft
      # then, γ is multiplied by Z

      # Z for flow from below (positive sign, vector)
      Z_min = dz[i,j,k]

      # Z for flow from above (negative sign, vector)
      Z_plus = - dz[i,j,k]

      # gamma
      gamma_min = .21584E-3 * rho[i,j,k] * 32.174
      gamma_plus = gamma_min

      Z_gamma_min = Z_min * gamma_min
      Z_gamma_plus = Z_plus * gamma_plus

      # boundary flows
      qsc_bB = constant_pressuregrad_bc3d('bottom', pg_bB, dx[i,j,k], dy[i,j,k], kz[i,j,k], mu[i,j,k], B[i,j,k], rho[i,j,k]) # bottom
      qsc_bU = constant_pressure_bc3d('upper', (i+1,j+1,k+1), p_bU, dx[i,j,k], dy[i,j,k], kz[i,j,k], dz[i,j,k], mu[i,j,k], B[i,j,k], rho[i,j,k]) # upper
      qsc_bS = constant_rate_bc2d(Ty_min, q_bS, (xi*yi)) # south
      qsc_bN = constant_pressure_bc3d('north', (i+1,j+1,k+1), p_bN, dx[i,j,k], dz[i,j,k], ky[i,j,k], dy[i,j,k], mu[i,j,k], B[i,j,k], rho[i,j,k]) # north
      qsc_bW = constant_rate_bc2d(Tx_min, q_bW, (yi*zi)) # west
      qsc_bE = constant_rate_bc2d(Tx_plus, q_bE, (yi*zi)) # east

      ## West Boundaries
      if i==0:
        if j==0:
          if k==0:
            # bottom southwest corner boundary
            # 3 faces. Tx-, Ty-, Tz-

            print('Bottom southwest corner boundary block')
            print('Block {}: [{} (p{} - p{})] + [{}] + [{} (p{} - p{})] + [{}] + [{} (p{} - p{}) - ({})] + [{}] + [{}] \n'.format((i+1,j+1,k+1), Tx_plus, (i+2,j+1,k+1), (i+1,j+1,k+1), qsc_bW, Ty_plus, (i+1,j+2,k+1), (i+1,j+1,k+1), qsc_bS, Tz_plus, (i+1,j+1,k+2), (i+1,j+1,k+1), Z_gamma_plus, qsc_bB, qsc[i,j,k]))
          
          if k==zi-1:
            # upper southwest corner boundary
            # 3 faces. Tx-, Ty-, Tz+
            print('Upper southwest corner boundary block')
            print('Block {}: [{} (p{} - p{})] + [{}] + [{} (p{} - p{})] + [{}] + [{}] + [{} (p{} - p{}) - ({})] + [{}] \n'.format((i+1,j+1,k+1), Tx_plus, (i+2,j+1,k+1), (i+1,j+1,k+1), qsc_bW, Ty_plus, (i+1,j+2,k+1), (i+1,j+1,k+1), qsc_bS, qsc_bU, Tz_min, (i+1,j+1,k), (i+1,j+1,k+1), Z_gamma_min, qsc[i,j,k]))
          
          if k!=0 and k!=zi-1:
            # central southwest corner boundary
            # 2 faces. Tx-, Ty-
            print('Central southwest corner boundary block')
            print('Block {}: [{} (p{} - p{})] + [{}] + [{} (p{} - p{})] + [{}] + [{} (p{} - p{}) - ({})] + [{} (p{} - p{}) - ({})] + [{}] \n'.format((i+1,j+1,k+1), Tx_plus, (i+2,j+1,k+1), (i+1,j+1,k+1), qsc_bW, Ty_plus, (i+1,j+2,k+1), (i+1,j+1,k+1), qsc_bS, Tz_plus, (i+1,j+1,k+2), (i+1,j+1,k+1), Z_gamma_plus, Tz_min, (i+1,j+1,k), (i+1,j+1,k+1), Z_gamma_min, qsc[i,j,k]))

        if j==yi-1:
          if k==0:
            # bottom northwest corner boundary
            # 3 faces. Tx-, Ty+, Tz-
            print('Bottom northwest corner boundary block')
            print('Block {}: [{} (p{} - p{})] + [{}] + [{}] + [{} (p{} - p{})] + [{} (p{} - p{}) - ({})] + [{}] + [{}] \n'.format((i+1,j+1,k+1), Tx_plus, (i+2,j+1,k+1), (i+1,j+1,k+1), qsc_bW, qsc_bN, Ty_min, (i+1,j,k+1), (i+1,j+1,k+1), Tz_plus, (i+1,j+1,k+2), (i+1,j+1,k+1), Z_gamma_plus, qsc_bB, qsc[i,j,k]))

          if k==zi-1:
            # upper northwest corner boundary
            # 3 faces. Tx-, Ty+, Tz+
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
            print('Bottom west boundary block')
            print('Block {}: [{} (p{} - p{})] + [{}] + [{} (p{} - p{})] + [{} (p{} - p{})] + [{} (p{} - p{}) - ({})] + [{}] + [{}] \n'.format((i+1,j+1,k+1), Tx_plus, (i+2,j+1,k+1), (i+1,j+1,k+1), qsc_bW, Ty_plus, (i+1,j+2,k+1), (i+1,j+1,k+1), Ty_min, (i+1,j,k+1), (i+1,j+1,k+1), Tz_plus, (i+1,j+1,k+2), (i+1,j+1,k+1), Z_gamma_plus, qsc_bB, qsc[i,j,k]))

          if k==zi-1:
            # upper west boundary
            # 2 faces. Tx-, Tz+
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
          if k==0:
            # bottom southeast corner boundary
            # 3 faces. Tx+, Ty-, Tz-
            print('Bottom southeast corner boundary block')
            print('Block {}: [{}] + [{} (p{} - p{})] + [{} (p{} - p{})] + [{}] + [{} (p{} - p{}) - ({})] + [{}] + [{}] \n'.format((i+1,j+1,k+1), qsc_bE, Tx_min, (i,j+1,k+1), (i+1,j+1,k+1), Ty_plus, (i+1,j+2,k+1), (i+1,j+1,k+1), qsc_bS, Tz_plus, (i+1,j+1,k+2), (i+1,j+1,k+1), Z_gamma_plus, qsc_bB, qsc[i,j,k]))

          if k==zi-1:
            # upper southeast corner boundary
            # 3 faces. Tx+, Ty-, Tz+
            print('Upper southeast corner boundary block')
            print('Block {}: [{}] + [{} (p{} - p{})] + [{} (p{} - p{})] + [{}] + [{}] + [{} (p{} - p{}) - ({})] + [{}] \n'.format((i+1,j+1,k+1), qsc_bE, Tx_min, (i,j+1,k+1), (i+1,j+1,k+1), Ty_plus, (i+1,j+2,k+1), (i+1,j+1,k+1), qsc_bS, qsc_bU, Tz_min, (i+1,j+1,k), (i+1,j+1,k+1), Z_gamma_min, qsc[i,j,k]))

          if k!=0 and k!=zi-1:
            # central southeast corner boundary
            # 2 faces. Tx+, Ty-
            print('Central southeast corner boundary block')
            print('Block {}: [{}] + [{} (p{} - p{})] + [{} (p{} - p{})] + [{}] + [{} (p{} - p{}) - ({})] + [{} (p{} - p{}) - ({})] + [{}] \n'.format((i+1,j+1,k+1), qsc_bE, Tx_min, (i,j+1,k+1), (i+1,j+1,k+1), Ty_plus, (i+1,j+2,k+1), (i+1,j+1,k+1), qsc_bS, Tz_plus, (i+1,j+1,k+2), (i+1,j+1,k+1), Z_gamma_plus, Tz_min, (i+1,j+1,k), (i+1,j+1,k+1), Z_gamma_min, qsc[i,j,k]))

        if j==yi-1:
          if k==0:
            # bottom northeast corner boundary
            # 3 faces. Tx+, Ty+, Tz-
            print('Bottom northeast corner boundary block')
            print('Block {}: [{}] + [{} (p{} - p{})] + [{}] + [{} (p{} - p{})] + [{} (p{} - p{}) - ({})] + [{}] + [{}] \n'.format((i+1,j+1,k+1), qsc_bE, Tx_min, (i,j+1,k+1), (i+1,j+1,k+1), qsc_bN, Ty_min, (i+1,j,k+1), (i+1,j+1,k+1), Tz_plus, (i+1,j+1,k+2), (i+1,j+1,k+1), Z_gamma_plus, 5, qsc[i,j,k]))

          if k==zi-1:
            # upper northeast corner boundary
            # 3 faces. Tx+, Ty+, Tz+
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
            print('Bottom east boundary block')
            print('Block {}: [{}] + [{} (p{} - p{})] + [{} (p{} - p{})] + [{} (p{} - p{})] + [{} (p{} - p{}) - ({})] + [{}] + [{}] \n'.format((i+1,j+1,k+1), qsc_bE, Tx_min, (i,j+1,k+1), (i+1,j+1,k+1), Ty_plus, (i+1,j+2,k+1), (i+1,j+1,k+1), Ty_min, (i+1,j,k+1), (i+1,j+1,k+1), Tz_plus, (i+1,j+1,k+2), (i+1,j+1,k+1), Z_gamma_plus, qsc_bB, qsc[i,j,k]))

          if k==zi-1:
            # upper east boundary
            # 2 faces. Tx+, Tz+
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
          if k==0:
            # bottom south boundary
            # 2 faces. Ty-, Tz-
            print('Bottom south boundary block')
            print('Block {}: [{} (p{} - p{})] + [{} (p{} - p{})] + [{} (p{} - p{})] + [{}] + [{} (p{} - p{}) - ({})] + [{}] + [{}] \n'.format((i+1,j+1,k+1), Tx_plus, (i+2,j+1,k+1), (i+1,j+1,k+1), Tx_min, (i,j+1,k+1), (i+1,j+1,k+1), Ty_plus, (i+1,j+2,k+1), (i+1,j+1,k+1), qsc_bS, Tz_plus, (i+1,j+1,k+2), (i+1,j+1,k+1), Z_gamma_plus, qsc_bB, qsc[i,j,k]))

          if k==zi-1:
            # upper south boundary
            # 2 faces. Ty-, Tz+
            print('Upper south boundary block')
            print('Block {}: [{} (p{} - p{})] + [{} (p{} - p{})] + [{} (p{} - p{})] + [{}] + [{}] + [{} (p{} - p{}) - ({})] + [{}] \n'.format((i+1,j+1,k+1), Tx_plus, (i+2,j+1,k+1), (i+1,j+1,k+1), Tx_min, (i,j+1,k+1), (i+1,j+1,k+1), Ty_plus, (i+1,j+2,k+1), (i+1,j+1,k+1), qsc_bS, qsc_bU, Tz_min, (i+1,j+1,k), (i+1,j+1,k+1), Z_gamma_min, qsc[i,j,k]))

          if k!=0 and k!=zi-1:
            # central south boundary
            # 1 face. Ty-
            print('Central south boundary block')
            print('Block {}: [{} (p{} - p{})] + [{} (p{} - p{})] + [{} (p{} - p{})] + [{}] + [{} (p{} - p{}) - ({})] + [{} (p{} - p{}) - ({})] + [{}] \n'.format((i+1,j+1,k+1), Tx_plus, (i+2,j+1,k+1), (i+1,j+1,k+1), Tx_min, (i,j+1,k+1), (i+1,j+1,k+1), Ty_plus, (i+1,j+2,k+1), (i+1,j+1,k+1), qsc_bS, Tz_plus, (i+1,j+1,k+2), (i+1,j+1,k+1), Z_gamma_plus, Tz_min, (i+1,j+1,k), (i+1,j+1,k+1), Z_gamma_min, qsc[i,j,k]))

        if j==yi-1:
          if k==0:
            # bottom north boundary
            # 2 faces. Ty+, Tz-
            print('Bottom north boundary block')
            print('Block {}: [{} (p{} - p{})] + [{} (p{} - p{})] + [{}] + [{} (p{} - p{})] + [{} (p{} - p{}) - ({})] + [{}] + [{}] \n'.format((i+1,j+1,k+1), Tx_plus, (i+2,j+1,k+1), (i+1,j+1,k+1), Tx_min, (i,j+1,k+1), (i+1,j+1,k+1), qsc_bN, Ty_min, (i+1,j,k+1), (i+1,j+1,k+1), Tz_plus, (i+1,j+1,k+2), (i+1,j+1,k+1), Z_gamma_plus, qsc_bB, qsc[i,j,k]))

          if k==zi-1:
            # upper north boundary
            # 2 faces. Ty+, Tz+
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
            print('Bottom boundary block')
            print('Block {}: [{} (p{} - p{})] + [{} (p{} - p{})] + [{} (p{} - p{})] + [{} (p{} - p{})] + [{} (p{} - p{}) - ({})] + [{}] + [{}] \n'.format((i+1,j+1,k+1), Tx_plus, (i+2,j+1,k+1), (i+1,j+1,k+1), Tx_min, (i,j+1,k+1), (i+1,j+1,k+1), Ty_plus, (i+1,j+2,k+1), (i+1,j+1,k+1), Ty_min, (i+1,j,k+1), (i+1,j+1,k+1), Tz_plus, (i+1,j+1,k+2), (i+1,j+1,k+1), Z_gamma_plus, qsc_bB, qsc[i,j,k]))

          if k==zi-1:
            # upper boundary
            # 1 face. Tz+
            print('Upper boundary block')
            print('Block {}: [{} (p{} - p{})] + [{} (p{} - p{})] + [{} (p{} - p{})] + [{} (p{} - p{})] + [{}] + [{} (p{} - p{}) - ({})] + [{}] \n'.format((i+1,j+1,k+1), Tx_plus, (i+2,j+1,k+1), (i+1,j+1,k+1), Tx_min, (i,j+1,k+1), (i+1,j+1,k+1), Ty_plus, (i+1,j+2,k+1), (i+1,j+1,k+1), Ty_min, (i+1,j,k+1), (i+1,j+1,k+1), qsc_bU, Tz_min, (i+1,j+1,k), (i+1,j+1,k+1), Z_gamma_min, qsc[i,j,k]))

          if k!=0 and k!=zi-1:
            # interior blocks
            # 0 face. Flow totally inter-block, no contact to boundaries.
            print('Interior block')
            print('Block {}: [{} (p{} - p{})] + [{} (p{} - p{})] + [{} (p{} - p{})] + [{} (p{} - p{})] + [{} (p{} - p{}) - ({})] + [{} (p{} - p{}) - ({})] + [{}] \n'.format((i+1,j+1,k+1), Tx_plus, (i+2,j+1,k+1), (i+1,j+1,k+1), Tx_min, (i,j+1,k+1), (i+1,j+1,k+1), Ty_plus, (i+1,j+2,k+1), (i+1,j+1,k+1), Ty_min, (i+1,j,k+1), (i+1,j+1,k+1), Tz_plus, (i+1,j+1,k+2), (i+1,j+1,k+1), Z_gamma_plus, Tz_min, (i+1,j+1,k), (i+1,j+1,k+1), Z_gamma_min, qsc[i,j,k]))
