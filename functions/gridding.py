"""
@author: Yohanes Nuwara
@email: ign.nuwara97@gmail.com
"""

def create_irregular_grid(x, y, xy_inactive):
  """
  Create irregular grids based on the defined inactive blocks
  and original dimension

  Input:

  x, y = meshes in X and Y-direction after Numpy meshgrid (2D numpy array)
  xy_inactive = list of inactive block coordinates
  e.g: [(1,1), (2,3), (3,4)]
  """
  import numpy as np
  x, y = x.astype('float64'), y.astype('float64')

  ## create index array from the inactive blocks
  x_inactive = []
  y_inactive = []
  for i in range(len(xy_inactive)):
    x_inactive.append(xy_inactive[i][0])
    y_inactive.append(xy_inactive[i][1])

  x_inactive, y_inactive = np.array(x_inactive) - 1, np.array(y_inactive) - 1

  ## mask out the inactive blocks from the meshgrid  
  for i, j in zip(x_inactive, y_inactive):
    x[i,j], y[i,j] = np.nan, np.nan  
  
  return x, y, x_inactive, y_inactive

def maskout_inactive_blocks(prop_in, x_inactive, y_inactive, xi):
  """
  Mask out the properties from inactive blocks in irregular reservoir
  """
  import numpy as np

  prop_in = np.reshape(prop_in, (-1, xi))
  prop_in = prop_in.astype('float64')

  for i, j in zip(y_inactive, x_inactive):
    prop_in[i,j] = np.nan
  prop_out = np.transpose(prop_in)
  return prop_out

def fill_active_blocks(prop_in, x):
  import numpy as np
  import copy

  ## create copy of x (x consists of location of ACTIVE and INACTIVE blocks)
  prop_out = x.copy()
  prop_out = prop_out.T
  ## return True if NaN, False if not NaN (masking array) 
  mask = np.isnan(prop_out)
  ## fill the True values of mask to replace NaN, with values of ACTIVE grids
  if prop_in.dtype.type is np.str_:
    prop_out = prop_out.astype(str)
    prop_out[~mask] = prop_in
  else: 
    prop_out[~mask] = prop_in
  ## transposing to get shape equals to x 
  prop_out = prop_out.T
  
  return prop_out

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
  qsc = np.array([[0.]*yi]*xi)

  # replace the zeros at coordinate of source term, with the rate of source term
  for i, j, k in zip(xsc, ysc, range(len(q))):
    qsc[i][j] = q[k]    
  return qsc
