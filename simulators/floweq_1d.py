@author: Yohanes Nuwara
@email: ign.nuwara97@gmail.com

# blocks location
block = np.arange(1, 5+1)

# define parameters, in this case blocks are homogeneous and same in size
dx = 1000 # ft
dy = 1200
dz = 75
kx = 15 # md
B = 1 # RB/STB
mu = 10 # cp

# assign all params to all blocks
dx = np.full(len(block), dx)
dy = np.full(len(block), dy)
dz = np.full(len(block), dz)
kx = np.full(len(block), kx)
B = np.full(len(block), B)
mu = np.full(len(block), mu)

# source term
qsc = np.zeros(len(block)) # initiate with zeros
qsc[3] = -150 # inject the source to block 4

# boundary conditions
p_bW = 5000 # pressure at left (West) boundary
q_bE = 0. # flow rate at right (East) boundary

print('Left-Hand Side (RHS) of Flow equation in each boundary block')
print('1st term: Flow in X-direction from adjacent block')
print('2nd term: Fictitious flow into boundary block')
print('3rd term: Source accumulation \n')

print('Left-Hand Side (RHS) of Flow equation in each internal block')
print('1st term: Flow in X-direction from previous block')
print('2nd term: Flow in X-direction from next block')
print('3rd term: Source accumulation \n')

for i in range(len(block)):
  A = dy[i] * dz[i]
  T_min = .001127 * (kx[i] * A) / (mu[i] * B[i] * dx[i])
  T_plus = T_min 
  if i == 0:
    # constant pressure at left boundary
    qsc_b = constant_pressure_bc1d(block[i], p_bW, dy[i], dz[i], kx[i], dx[i], mu[i], B[i])
    print('Boundary Block {}: {} (p{} - p{}) + {} + {}'.format(block[i], T_plus, block[i+1], block[i], qsc_b, qsc[i]))
  elif i == len(block)-1:
    # no flow at right boundary
    qsc_b = constant_rate_bc1d(q_bE)
    print('Boundary Block {}: {} (p{} - p{}) + {} + {}'.format(block[i], T_min, block[i-1], block[i], qsc_b, qsc[i]))
  else:
    print('Interior Block {}: {} (p{} - p{}) + {} (p{} - p{}) + {}'.format(block[i], T_min, block[i-1], block[i], T_plus, block[i+1], block[i], qsc[i]))
