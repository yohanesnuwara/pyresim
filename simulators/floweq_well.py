"""
Simulation in Cylindrical (Well-represented) Reservoir Grids in 2D

@author: Yohanes Nuwara
@email: ign.nuwara97@gmail.com
"""

from boundary import *
from transmissibility import *

" Inputs "

# number of blocks in x and z
# in well representation, x is r
xi = 4; zi = 3 

# define parameters, in this case blocks are homogeneous and same in size
h = 30 # ft
poro = .23
kh = 150 # horizontal perm, md
ratio_kv_kh = .3
rho = 62.4 # lbm/ft3
B = 1 # RB/B
mu = .5 # cp
dw = 0.5 # well diameter, ft
spacing = 20 # acre

# source term
# well produces in top 20 ft, means: in block (1,2) or block 5
xsc = 1; zsc = 2  
q = -2000

# boundaries
p_bB = 4000 # bottom boundary, constant pressure in psia
q_bU = 0 # upper boundary, no flow
q_bO = 0 # outer boundary, no flow
q_bI = q # inner boundary, production flow (Q)

" Main code starts here "

# create block coordinates (Engineering Notation convention in Abou-Kassem)
x_ = np.arange(1, xi+1)
z_ = np.arange(1, zi+1)

x, z = np.meshgrid(x_, z_, indexing='ij')

spacing = spacing * 43560 # acre to ft2

# permeability, here kh is assumed kx, kv is assumed kz
kx = kh
kz = kv = kh * ratio_kv_kh

# assign all params to all blocks
dz = np.array([[h / zi]*zi]*xi)
kx = np.array([[kx]*zi]*xi)
kz = np.array([[kz]*zi]*xi)
B = np.array([[B]*zi]*xi)
mu = np.array([[mu]*zi]*xi)
rho = np.array([[rho]*zi]*xi)

qsc = np.array([[0]*zi]*xi) # initiate with zeros
qsc[xsc-1,zsc-1] = q # inject the source to block

" Grid geometry (grid spacing, grid elevation, bulk volume) "

# calculate gridblock spacing and to produce dx
re = np.sqrt(spacing / np.pi)
rw = 0.5 * dw

nr = xi
α_tg = (re / rw)**(1 / nr)

r1 = ((α_tg * np.log(α_tg)) / (α_tg - 1)) * rw # 1st gridblock

rn = []

for i in range(2, nr+1):
  rn_ = α_tg**(i-1) * r1
  rn.append(rn_)

rn = np.append(r1, rn)

dx = np.array([[0.]*zi]*xi)

for i in range(xi): 
  dx[i,:] = rn[i]

# calculate elevation
elev = np.cumsum(dz[1,:])
elev = elev[::-1]

d_elev = np.array([[0.]*zi]*xi)

for i in range(zi): 
  d_elev[:,i] = elev[i] - 0.5 * dz[:,i]

# calculate bulk volume
θ = 2 * np.pi
delta_z = h / zi

Vbulk_ri = []
for i in range(nr-1):
  Vbulk_ = (((α_tg**2 - 1)**2 / (α_tg**2 * np.log(α_tg**2))) * rn[i]**2) * (0.5 * θ) * delta_z
  Vbulk_ri.append(Vbulk_)

## calculation for rn (last grid block)
Vbulk_rn = (1 - (np.log (α_tg) / (α_tg - 1))**2 * (α_tg**2 - 1) / (α_tg**2 * np.log(α_tg**2))) * re**2 * (0.5 * θ) * delta_z

## append both Vbulk_ri and Vbulk_rn
Vbulk = np.append(Vbulk_ri, Vbulk_rn)

dv = np.array([[0.]*zi]*xi)

for i in range(xi): 
  dv[i,:] = Vbulk[i]

" Calculate transmissibilities "
T_r_min = np.array([[0.]*zi]*xi)
T_r_plus = np.array([[0.]*zi]*xi)
T_z_min = np.array([[0.]*zi]*xi)
T_z_plus = np.array([[0.]*zi]*xi)

for i in range(xi):
  for j in range(zi):

    if i==0:
      # boundaries in the Inner
      # qsc_bI = constant_rate_bc2d(T_r_min[i,j], 0, yi)

      if j==0:
        # Bottom inner corner boundary has two face boundaries (cons rate & cons press)
        # Tr- and Tz- are flow from boundaries
        T_r_min[i,j] = T_z_min[i,j] = np.nan
        T_r_plus[i,j] = trans_r_plus(dz[i,j], dz[i+1,j], (2 * np.pi), α_tg, kx[i,j], kx[i+1,j], mu[i,j], B[i,j])
        T_z_plus[i,j] = trans_z_plus(dz[i,j], dz[i,j+1], dv[i,j], kz[i,j], kz[i,j+1], mu[i,j], B[i,j])

      if j==zi-1:
        # Upper inner boundary has two face boundaries (cons rate & no flow)
        # Tr- and Tz+ are flow from boundaries
        T_r_min[i,j] = T_z_plus[i,j] = np.nan 
        T_r_plus[i,j] = trans_r_plus(dz[i,j], dz[i+1,j], (2 * np.pi), α_tg, kx[i,j], kx[i+1,j], mu[i,j], B[i,j])
        T_z_min[i,j] = trans_z_min(dz[i,j], dz[i,j-1], dv[i,j], kz[i,j], kz[i,j-1], mu[i,j], B[i,j])                 

      else:
        if j!=0 and j!=zi-1:
          # Inner boundary has cons rate
          # Tr- is flow from boundary
          T_r_min[i,j] = np.nan
          T_r_plus[i,j] = trans_r_plus(dz[i,j], dz[i+1,j], (2 * np.pi), α_tg, kx[i,j], kx[i+1,j], mu[i,j], B[i,j])
          T_z_min[i,j] = trans_z_min(dz[i,j], dz[i,j+1], dv[i,j], kz[i,j], kz[i,j+1], mu[i,j], B[i,j])           
          T_z_plus[i,j] = trans_z_plus(dz[i,j], dz[i,j-1], dv[i,j], kz[i,j], kz[i,j-1], mu[i,j], B[i,j])  

    elif i==xi-1:
      # boundaries in the Outer
      # qsc_bO = constant_pressuregrad_bc1d('east', pg_bE, dy[i,j], dz[i,j], kx[i,j], mu[i,j], B[i,j])

      if j==0:
        # Bottom outer corner boundary has two face boundaries (no flow & cons press)
        # Tr+ and Tz- are flow from boundaries
        T_r_plus[i,j] = T_z_min[i,j] = np.nan
        T_r_min[i,j] = trans_r_min(dz[i,j], dz[i-1,j], (2 * np.pi), α_tg, kx[i,j], kx[i-1,j], mu[i,j], B[i,j])      
        T_z_plus[i,j] = trans_z_plus(dz[i,j], dz[i,j+1], dv[i,j], kz[i,j], kz[i,j+1], mu[i,j], B[i,j])   

      if j==zi-1:
        # Upper outer boundary has two face boundaries (no flow & no flow)
        # Tr+ and Tz+ are flow from boundaries
        T_r_plus[i,j] = T_z_plus[i,j] = np.nan
        T_r_min[i,j] = trans_r_min(dz[i,j], dz[i-1,j], (2 * np.pi), α_tg, kx[i,j], kx[i-1,j], mu[i,j], B[i,j])
        T_z_min[i,j] = trans_z_min(dz[i,j], dz[i,j-1], dv[i,j], kz[i,j], kz[i,j-1], mu[i,j], B[i,j])           

      else:
        if j!=0 and j!=zi-1:
          # Outer boundary has no flow
          # Tr+ is flow from boundary
          T_r_plus[i,j] = np.nan
          T_r_min[i,j] = trans_r_min(dz[i,j], dz[i-1,j], (2 * np.pi), α_tg, kx[i,j], kx[i-1,j], mu[i,j], B[i,j])
          T_z_min[i,j] = trans_z_min(dz[i,j], dz[i,j-1], dv[i,j], kz[i,j], kz[i,j-1], mu[i,j], B[i,j])           
          T_z_plus[i,j] = trans_z_plus(dz[i,j], dz[i,j+1], dv[i,j], kz[i,j], kz[i,j+1], mu[i,j], B[i,j])   

    elif i!=0 and i!=xi-1:
      # boundaries in the Upper OR Bottom 
      if j==0:
        # Bottom boundary has constant pressure 
        # Tz- is flow from boundary
        T_z_min[i,j] = np.nan
        T_r_min[i,j] = trans_r_min(dz[i,j], dz[i-1,j], (2 * np.pi), α_tg, kx[i,j], kx[i-1,j], mu[i,j], B[i,j])
        T_r_plus[i,j] = trans_r_plus(dz[i,j], dz[i+1,j], (2 * np.pi), α_tg, kx[i,j], kx[i+1,j], mu[i,j], B[i,j])        
        T_z_plus[i,j] = trans_z_plus(dz[i,j], dz[i,j+1], dv[i,j], kz[i,j], kz[i,j+1], mu[i,j], B[i,j])   

      if j==zi-1:  
        # Uper boundary has no flow
        # Tz+ is flow from boundary  
        T_z_plus[i,j] = np.nan   
        T_r_min[i,j] = trans_r_min(dz[i,j], dz[i-1,j], (2 * np.pi), α_tg, kx[i,j], kx[i-1,j], mu[i,j], B[i,j])
        T_r_plus[i,j] = trans_r_plus(dz[i,j], dz[i+1,j], (2 * np.pi), α_tg, kx[i,j], kx[i+1,j], mu[i,j], B[i,j])
        T_z_min[i,j] = trans_z_min(dz[i,j], dz[i,j-1], dv[i,j], kz[i,j], kz[i,j-1], mu[i,j], B[i,j])               

      else:
        if j!=0 and j!=zi-1:
          # the interior blocks
          # no boundary flow
          T_r_min[i,j] = trans_r_min(dz[i,j], dz[i-1,j], (2 * np.pi), α_tg, kx[i,j], kx[i-1,j], mu[i,j], B[i,j])
          T_r_plus[i,j] = trans_r_plus(dz[i,j], dz[i+1,j], (2 * np.pi), α_tg, kx[i,j], kx[i+1,j], mu[i,j], B[i,j])
          T_z_min[i,j] = trans_z_min(dz[i,j], dz[i,j-1], dv[i,j], kz[i,j], kz[i,j-1], mu[i,j], B[i,j])           
          T_z_plus[i,j] = trans_z_plus(dz[i,j], dz[i,j+1], dv[i,j], kz[i,j], kz[i,j+1], mu[i,j], B[i,j])   

" Preconditioning for the INNER boundary flow from production rate "
# mirroring the transmissibilities to replace the nan values

import copy

T_r_min_updated = T_r_min.copy()

for j in range(zi):
  if j<zsc-1:
    T_r_min_updated[0,j] = 0
  if j>=zsc-1:
    T_r_min_updated[0,j] = T_r_min[1,j]

T_sum = np.sum(T_r_min_updated[0,:])

" Print grid geometry, print transmissibility, calculate flow, and print flow equation "

print('Table 4-6: Grid Geometry and Flow Equation of Cylindrical Reservoir around Well')
print('ri: grid spacing (ft)')
print('Δz: grid thickness (ft)')
print('Z: elevation (ft) from top reservoir (0 ft)')
print('Vb: bulk volume (ft3) \n') 

print('Left-Hand Side (RHS) of Flow equation in each block')
print('1st term: Flow in r-direction from next block (Tr+)')
print('2nd term: Flow in r-direction from previous block (Tr-)')
print('3rd term: Flow in z-direction from next block (Tz+)')
print('4th term: Flow in z-direction from previous block (Tz-)')
print('5th term: Source accumulation \n')

for i in range(xi):
  for j in range(zi):

    # Flow from boundaries (I: inner, O: outer, B: bottom, U: upper)

    if i==0:
      # boundaries in the Inner
      # constant flow from source point at block (1,2)
      """
      take notice, this Inner part is QUITE TRICKY. First, we need to 
      calculate the flow rate in the boundary shared by the flow rate
      of the production well. Below is the implementation for p. 107 (Eq 4.28)
      before in the preconditioning section, we calculated T_sum
      """
      if j<zsc-1:
        qsc_bI = 0
      if j>=zsc-1:
        qsc_bI = (T_r_min_updated[i,j] / T_sum) * q

      # differentiating the boundary
      if j==0:
        # Bottom inner corner boundary has two face boundaries (cons rate & cons press)
        # Tr- and Tz- are flow from boundaries

        qsc_bB = constant_pressure_well2d('bottom', (i+1,j+1), p_bB, h, d_elev[i,j], kz[i,j], dz[i,j], dv[i,j], mu[i,j], B[i,j], rho[i,j])

        print('bottom inner corner block {}'.format((i+1,j+1)))  
        print('Geometry, ri: {}, Δz: {}, Z: {}, Vb: {}'.format(np.round(dx[i,j], 5), np.round(dz[i,j], 5), d_elev[i,j], np.round(dv[i,j], 5)))
        print('Transmissibility, r- direction: {}, r+ direction: {}, z- direction: {}, z+ direction: {}'.format(T_r_min[i,j], T_r_plus[i,j], T_z_min[i,j], T_z_plus[i,j]))

        print('Boundary Block {}: {} (p{} - p{}) + {} + {} (p{} - p{}) + {} + {} \n'.format((i+1,j+1), T_r_plus[i,j], (i+2,j+1), (i+1,j+1), qsc_bI, T_z_plus[i,j], (i+1,j+2), (i+1,j+1), qsc_bB, qsc[i,j]))         

      if j==zi-1:
        # Upper inner boundary has two face boundaries (cons rate & no flow)
        # Tr- and Tz+ are flow from boundaries

        qsc_bU = q_bU # no flow

        print('upper inner corner block {}'.format((i+1,j+1)))
        print('Geometry, ri: {}, Δz: {}, Z: {}, Vb: {}'.format(np.round(dx[i,j], 5), np.round(dz[i,j], 5), d_elev[i,j], np.round(dv[i,j], 5)))
        print('Transmissibility, r- direction: {}, r+ direction: {}, z- direction: {}, z+ direction: {}'.format(T_r_min[i,j], T_r_plus[i,j], T_z_min[i,j], T_z_plus[i,j]))

        print('Boundary Block {}: {} (p{} - p{}) + {} + {} + {} (p{} - p{}) + {} \n'.format((i+1,j+1), T_r_plus[i,j], (i+2,j+1), (i+1,j+1), qsc_bI, qsc_bU, T_z_min[i,j], (i+1,j), (i+1,j+1), qsc[i,j]))         

      else:
        if j!=0 and j!=zi-1:
          # Inner boundary has cons rate
          # Tr- is flow from boundary

          print('inner block {}'.format((i+1,j+1)))   
          print('Geometry, ri: {}, Δz: {}, Z: {}, Vb: {}'.format(np.round(dx[i,j], 5), np.round(dz[i,j], 5), d_elev[i,j], np.round(dv[i,j], 5)))
          print('Transmissibility, r- direction: {}, r+ direction: {}, z- direction: {}, z+ direction: {}'.format(T_r_min[i,j], T_r_plus[i,j], T_z_min[i,j], T_z_plus[i,j]))

          print('Boundary Block {}: {} (p{} - p{}) + {} + {} (p{} - p{}) + {} (p{} - p{}) + {} \n'.format((i+1,j+1), T_r_plus[i,j], (i+2,j+1), (i+1,j+1), qsc_bI, T_z_plus[i,j], (i+1,j+2), (i+1,j+1), T_z_min[i,j], (i+1,j), (i+1,j+1), qsc[i,j]))         
    
    elif i==xi-1:
      # boundaries in the Outer
      # no flow

      qsc_bO = q_bO
      
      if j==0:
        # Bottom outer corner boundary has two face boundaries (no flow & cons press)
        # Tr+ and Tz- are flow from boundaries

        qsc_bB = constant_pressure_well2d('bottom', (i+1,j+1), p_bB, h, d_elev[i,j], kz[i,j], dz[i,j], dv[i,j], mu[i,j], B[i,j], rho[i,j])

        print('bottom outer corner block {}'.format((i+1,j+1)))
        print('Geometry, ri: {}, Δz: {}, Z: {}, Vb: {}'.format(np.round(dx[i,j], 5), np.round(dz[i,j], 5), d_elev[i,j], np.round(dv[i,j], 5)))
        print('Transmissibility, r- direction: {}, r+ direction: {}, z- direction: {}, z+ direction: {}'.format(T_r_min[i,j], T_r_plus[i,j], T_z_min[i,j], T_z_plus[i,j]))

        print('Boundary Block {}: {} + {} (p{} - p{}) + {} (p{} - p{}) + {} + {} \n'.format((i+1,j+1), qsc_bO, T_r_min[i,j], (i,j+1), (i+1,j+1), T_z_plus[i,j], (i+1,j+2), (i+1,j+1), qsc_bB, qsc[i,j]))

      if j==zi-1:
        # Upper outer boundary has two face boundaries (no flow & no flow)
        # Tr+ and Tz+ are flow from boundaries

        qsc_bU = q_bU # no flow

        print('upper outer corner block {}'.format((i+1,j+1))) 
        print('Geometry, ri: {}, Δz: {}, Z: {}, Vb: {}'.format(np.round(dx[i,j], 5), np.round(dz[i,j], 5), d_elev[i,j], np.round(dv[i,j], 5)))
        print('Transmissibility, r- direction: {}, r+ direction: {}, z- direction: {}, z+ direction: {}'.format(T_r_min[i,j], T_r_plus[i,j], T_z_min[i,j], T_z_plus[i,j]))

        print('Boundary Block {}: {} + {} (p{} - p{}) + {} + {} (p{} - p{}) + {} \n'.format((i+1,j+1), qsc_bO, T_r_min[i,j], (i,j+1), (i+1,j+1), qsc_bU, T_z_min[i,j], (i+1,j), (i+1,j+1), qsc[i,j]))

      else:
        if j!=0 and j!=zi-1:
          # Outer boundary has no flow
          # Tr+ is flow from boundary

          print('outer block {}'.format((i+1,j+1)))  
          print('Geometry, ri: {}, Δz: {}, Z: {}, Vb: {}'.format(np.round(dx[i,j], 5), np.round(dz[i,j], 5), d_elev[i,j], np.round(dv[i,j], 5)))
          print('Transmissibility, r- direction: {}, r+ direction: {}, z- direction: {}, z+ direction: {}'.format(T_r_min[i,j], T_r_plus[i,j], T_z_min[i,j], T_z_plus[i,j]))

          print('Boundary Block {}: {} + {} (p{} - p{}) + {} (p{} - p{}) + {} (p{} - p{}) + {} \n'.format((i+1,j+1), qsc_bO, T_r_min[i,j], (i,j+1), (i+1,j+1), T_z_plus[i,j], (i+1,j+2), (i+1,j+1), T_z_min[i,j], (i+1,j), (i+1,j+1), qsc[i,j]))

    elif i!=0 and i!=xi-1:
      # boundaries in the Upper OR Bottom 
      if j==0:
        # Bottom boundary has constant pressure 
        # Tz- is flow from boundary

        qsc_bB = constant_pressure_well2d('bottom', (i+1,j+1), p_bB, h, d_elev[i,j], kz[i,j], dz[i,j], dv[i,j], mu[i,j], B[i,j], rho[i,j])

        print('bottom block {}'.format((i+1,j+1)))
        print('Geometry, ri: {}, Δz: {}, Z: {}, Vb: {}'.format(np.round(dx[i,j], 5), np.round(dz[i,j], 5), d_elev[i,j], np.round(dv[i,j], 5)))
        print('Transmissibility, r- direction: {}, r+ direction: {}, z- direction: {}, z+ direction: {}'.format(T_r_min[i,j], T_r_plus[i,j], T_z_min[i,j], T_z_plus[i,j]))

        print('Boundary block {}: {} (p{} - p{}) + {} (p{} - p{}) + {} (p{} - p{}) + {} + {} \n'.format((i+1, j+1), T_r_plus[i,j], (i, j+1), (i+1, j+1), T_r_min[i,j], (i+2, j+1), (i+1, j+1), T_z_plus[i,j], (i+1, j+2), (i+1,j+1), qsc_bB, qsc[i,j]))

      if j==zi-1:  
        # Upper boundary has no flow
        # Tz+ is flow from boundary  

        qsc_bU = q_bU # no flow

        print('upper block {}'.format((i+1,j+1)))        
        print('Geometry, ri: {}, Δz: {}, Z: {}, Vb: {}'.format(np.round(dx[i,j], 5), np.round(dz[i,j], 5), d_elev[i,j], np.round(dv[i,j], 5)))
        print('Transmissibility, r- direction: {}, r+ direction: {}, z- direction: {}, z+ direction: {}'.format(T_r_min[i,j], T_r_plus[i,j], T_z_min[i,j], T_z_plus[i,j]))

        print('Boundary block {}: {} (p{} - p{}) + {} (p{} - p{}) + {} + {} (p{} - p{}) + {} \n'.format((i+1, j+1), T_r_plus[i,j], (i, j+1), (i+1, j+1), T_r_min[i,j], (i+2, j+1), (i+1, j+1), qsc_bU, T_z_min[i,j], (i+1, j), (i+1,j+1), qsc[i,j]))

      else:
        if j!=0 and j!=zi-1:
          # the interior blocks
          # no boundary flow
          
          print('interior block {}'.format((i+1,j+1)))
          print('Geometry, ri: {}, Δz: {}, Z: {}, Vb: {}'.format(np.round(dx[i,j], 5), np.round(dz[i,j], 5), d_elev[i,j], np.round(dv[i,j], 5)))
          print('Transmissibility, r- direction: {}, r+ direction: {}, z- direction: {}, z+ direction: {}'.format(T_r_min[i,j], T_r_plus[i,j], T_z_min[i,j], T_z_plus[i,j]))

          print('Interior block {}: {} (p{} - p{}) + {} (p{} - p{}) + {} (p{} - p{}) + {} (p{} - p{}) + {} \n'.format((i+1, j+1), T_r_plus[i,j], (i, j+1), (i+1, j+1), T_r_min[i,j], (i+2, j+1), (i+1, j+1), T_z_plus[i,j], (i+1, j+2), (i+1, j+1), T_z_min[i,j], (i+1, j), (i+1,j+1), qsc[i,j]))
