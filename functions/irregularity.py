"""
Codes to handle irregular reservoir geometry

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
