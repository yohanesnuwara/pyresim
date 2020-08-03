"""
Codes for gridding utilities in homogeneous reservoir
@author: Yohanes Nuwara
@email: ign.nuwara97@gmail.com
"""

def gridproperty1d(prop, xi):
  """
  Create property grid for 1D rectangular reservoir
  same size, homogeneous

  Input: 

  prop = property (as float, same value across the block)
  xi = dimension in x-direction

  Output:

  prop = property grids (as 1D numpy array)
  """
  import numpy as np
  block = np.arange(1, xi+1)
  prop = np.full(len(block), prop)
  return prop 

def source1d(q, xsc, xi):
  """
  Create source grid for 1D rectangular reservoir

  Input:

  q = amount of production / injection rate (+ value for injection, - value for
  production)
  xsc = location of production / injection well
  xi = dimension in x-direction

  Output:

  qsc = source grid (1D numpy array), informs source value at each grid
  """
  import numpy as np
  xsc = np.array(xsc) - 1
  block = np.arange(1, xi+1)  
  qsc = np.zeros(len(block)) # initiate with zeros

  for i, j in zip(xsc, range(len(q))):
    qsc[i] = q[j]

  return qsc

def create_grid2d(xi, yi):
  import numpy as np
  x_ = np.arange(1, xi+1)
  y_ = np.arange(1, yi+1)

  x, y = np.meshgrid(x_, y_, indexing='ij')
  return x, y

def gridproperty2d(prop, xi, yi):
  import numpy as np
  prop = np.array([[prop]*yi]*xi)
  return prop    

def source2d(q, xysc, xi, yi):
  """
  Create source grid for 2D rectangular reservoir

  Input:

  q = amount of production / injection rate (+ value for injection, - value for
  production)
  xysc = location of production / injection well (x,y)
  xi, yi = dimension in x-direction and y-direction

  Output:

  qsc = source grid (1D numpy array), informs source value at each grid
  """    
  import numpy as np
  xsc = xysc[:,0] - 1 
  ysc = xysc[:,1] - 1

  # initiate with zeros.
  qsc = np.array([[0]*yi]*xi)

  # replace the zeros at coordinate of source term, with the rate of source term
  for i, j, k in zip(xsc, ysc, range(len(q))):
    qsc[i][j] = q[k]    
  return qsc

def source3d(q, xyzsc, xi, yi, zi):
  """
  Create source grid for 2D rectangular reservoir

  Input:

  q = amount of production / injection rate (+ value for injection, - value for
  production)
  xyzsc = location of production / injection well (x,y,z)
  xi, yi, zi = dimension in x-direction, y-direction, z-direction

  Output:

  qsc = source grid (1D numpy array), informs source value at each grid
  """  
  import numpy as np
  xsc = xyzsc[:,0] - 1 
  ysc = xyzsc[:,1] - 1
  zsc = xyzsc[:,2] - 1    

  # initiate with zeros.
  qsc = np.array([[[0]*zi]*yi]*xi)

  # replace the zeros at coordinate of source term, with the rate of source term
  for i, j, k, l in zip(xsc, ysc, zsc, range(len(q))):
    qsc[i][j][k] = q[l]    
  return qsc       
