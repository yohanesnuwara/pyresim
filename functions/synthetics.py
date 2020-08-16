"""
Codes to create synthetic data

@author: Yohanes Nuwara
@email: ign.nuwara97@gmail.com
"""

def synthetic_halves_boundary(xi, yi):
  """
  Create a synthetic irregular boundary condition
  as halves of each side as different boundary condition (B.C.)

  e.g. 2D regular reservoir has 100x50 dimension
  in the north and south are divided into 25 and 25 grids with 2 different B.Cs
  in the west and east are divided into 50 and 50 grids with 2 different B.Cs

  Input: 

  xi, yi = reservoir dimension (NOTE: xi, yi should be divisible by 2)

  Output:

  w_b1, w_b2 = each halves of the west boundary coordinates
  e_b1, e_b2 = each halves of the east boundary coordinates
  s_b1, s_b2 = each halves of the south boundary coordinates
  n_b1, n_b2 = each halves of the north boundary coordinates      
  """

  w_b1 = []; e_b1 = []
  for i in range(1,np.int((0.5*yi)+1)):
    arr1 = [1,i]
    arr2 = [xi,i]
    w_b1.append(arr1)
    e_b1.append(arr2) 

  s_b1 = []; n_b1 = []
  for i in range(1,np.int((0.5*xi)+1)):
    arr1 = [i,1]
    arr2 = [i,xi]
    s_b1.append(arr1)
    n_b1.append(arr2) 

  w_b2 = []; e_b2 = []
  for i in range(np.int((0.5*yi)+1),yi+1):
    arr1 = [1,i]
    arr2 = [xi,i] 
    w_b2.append(arr1)
    e_b2.append(arr2)

  s_b2 = []; n_b2 = []
  for i in range(np.int((0.5*xi)+1),xi+1):
    arr1 = [i,1]
    arr2 = [i,xi]
    s_b2.append(arr1)
    n_b2.append(arr2) 
  
  return w_b1, w_b2, e_b1, e_b2, s_b1, s_b2, n_b1, n_b2
