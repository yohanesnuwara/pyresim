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
