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
