"""
Codes to handle irregular grids
Given: the location of active blocks, and input property data

@author: Yohanes Nuwara
@email: ign.nuwara97@gmail.com
"""

def create_irregular_grid(x, y, xy_inactive):
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
  
  return x,y
  
def maskout_inactive_blocks(prop_in, x_inactive, y_inactive, xi):
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
  prop_out[~mask] = prop_in
  ## transposing to get shape equals to x 
  prop_out = prop_out.T
  
  return prop_out
