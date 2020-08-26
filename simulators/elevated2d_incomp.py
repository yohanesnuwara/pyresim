""""""""
This simulator is temporary

incorporating depth to the dictionary of each loop
non_boundary({depth: })
""""""""

import warnings

warnings.filterwarnings("ignore", category=FutureWarning)

"""""""""""
PUT THE INPUT TXT DATA
"""""""""""

filepath = '/content/pyresim/input/intermediate/intermediate2d_input.txt'

# call the read_input function to read input data
reservoir_input, wells, west_boundary, east_boundary, south_boundary, north_boundary = read_input(filepath)

"""""""""""
RESERVOIR DEPTH

* If you have depth data (reservoir is ELEVATED), read the data using 
  'read_depth' function
* If you don't have and you want to simulate ELEVATED reservoir, 
  create your own synthetic data
* If you don't have and you want to simulate NON-ELEVATED reservoir, 
  create constant depth using 'constant_depth1d'
"""""""""""

# create 2D synthetic depth 
# south has depth 3,000 ft gradually decreases to 550 ft at north 
x, y = np.meshgrid(np.arange(1, xi+1), np.arange(1, yi+1), indexing='ij')
z_array = 0.5 * (100 * y + 1000)

"""""""""""
INPUT PROCESSING
"""""""""""

# number of blocks in x and y
xi = reservoir_input['xi']
yi = reservoir_input['yi']

# define parameters, in this case blocks are homogeneous and same in size
dx = reservoir_input['dx'] 
dy = reservoir_input['dy']
dz = reservoir_input['dz']
kx = reservoir_input['kx']
ky = reservoir_input['ky']
B = reservoir_input['B']
mu = reservoir_input['mu']

# well information (dataframe)
well_name = wells['well_name']
well_rw = wells['well_rw'] / 12  # wellbore radius, inch to ft
well_skin = wells['well_skin']
well_loc = wells['well_loc']
well_condition = wells['well_condition']
well_value = wells['well_value']
well_config = wells['well_config']

"""""""""""
GRIDDING
"""""""""""

" Create grid points "
# meshgrid the original points
x_ = np.arange(1, xi + 1)
y_ = np.arange(1, yi + 1)

x, y = np.meshgrid(x_, y_, indexing='ij')

" Handle irregularities "
# NOTHING. The grid is regular

" Classify the location of boundary with codes (1, 12, 13, etc) "
bound_loc = boundary2d_location(x, y, xi, yi)

"""""""""""
WELL INFORMATION PROCESSING
"""""""""""

# source block (production or injection well)
qsc = source2d(well_value, np.array(well_loc), xi, yi)  # call function HERE

# Calculate wellblock geometric factor
kh, r_eq, Gw = [], [], []

for i in range(len(well_config)):
    kh_, r_eq_, Gw_ = fraction_wellblock_geometric_factor(dx, dy, kx, ky, well_skin[i],
                                                          well_rw[i], dz, well_config[i])
    kh.append(kh_);
    r_eq.append(r_eq_);
    Gw.append(Gw_)

# create WELLBLOCK PROPERTY 
# inject (fill) the operating wells to 'qsc' grid that we created before
# the values won't be filled in the 'qsc' grid that has value = 0
qsc = qsc.astype('float')
qsc[qsc == 0] = np.nan

well_value = qsc
well_condition = fill_active_blocks(well_condition, qsc)
well_rw = fill_active_blocks(well_rw, qsc)
well_Gw = fill_active_blocks(np.array(Gw), qsc)
well_mu = fill_active_blocks(np.array(mu), qsc)
well_B = fill_active_blocks(np.array(B), qsc)

"""""""""""
SIMULATION
"""""""""""

def lookup(i, j, bound_dict):
    """
    Determine the type and value of boundary at a grid block
    given the boundary dictionary
    """
    if bound_dict['loc'] == 'all':
        bound_type = bound_dict['type']
        bound_value = bound_dict['value']
    else:
        x, y = i + 1, j + 1

        id1 = (np.where(np.all(bound_dict['loc'] == np.array([x, y]), axis=-1)))[0][0]
        id2 = (np.where(np.all((bound_dict['loc'][id1]) == np.array([x, y]), axis=-1)))[0][0]

        bound_type = (bound_dict['type'])[id1]
        bound_value = (bound_dict['value'])[id1]
    return bound_type, bound_value

# Create block index
block_index = np.arange(1, (xi * yi) + 1)
block_index = (np.reshape(block_index, (-1, xi))).T

# Create empty matrix for LHS and RHS
lhs_mat = np.array([[0.] * (xi * yi)] * (xi * yi))
rhs_mat = np.array([[0.] * 1] * (xi * yi))

for i in range(xi):
    for j in range(yi):

        if bound_loc[i, j] == 13:
            """""""""""
            MODIFY THIS W.R.T. THE GRID BLOCK LOCATION 
            """""""""""

            # get the TYPE and VALUE of the boundary from the BOUNDARY DICTIONARY
            b1_type, b1_value = lookup(i, j, west_boundary)
            b3_type, b3_value = lookup(i, j, south_boundary)

            # create boundary dictionary
            boundary = {'loc': np.array([1, 3]),
                        'type': np.array([b1_type, b3_type]),
                        'value': np.array([b1_value, b3_value])}

            # create non-boundary dictionary
            non_boundary = {'loc': np.array([2, 4]), 
                            'depth': np.array([z_array[i+1,j], z_array[i,j+1]])}

            # create well dictionary
            well = {'condition': well_condition[i, j],
                    'value': well_value[i, j],
                    'rw': well_rw[i, j],
                    'Gw': well_Gw[i, j]}

        if bound_loc[i, j] == 14:
            """""""""""
            MODIFY THIS W.R.T. THE GRID BLOCK LOCATION 
            """""""""""

            # get the TYPE and VALUE of the boundary from the BOUNDARY DICTIONARY
            b1_type, b1_value = lookup(i, j, west_boundary)
            b4_type, b4_value = lookup(i, j, north_boundary)

            # create boundary dictionary
            boundary = {'loc': np.array([1, 4]),
                        'type': np.array([b1_type, b4_type]),
                        'value': np.array([b1_value, b4_value])}

            # create non-boundary dictionary
            non_boundary = {'loc': np.array([2, 3]),
                            'depth': np.array([z_array[i+1,j], z_array[i,j-1]])}                            

            # create well dictionary
            well = {'condition': well_condition[i, j],
                    'value': well_value[i, j],
                    'rw': well_rw[i, j],
                    'Gw': well_Gw[i, j]}

        if bound_loc[i, j] == 23:
            """""""""""
            MODIFY THIS W.R.T. THE GRID BLOCK LOCATION 
            """""""""""

            # get the TYPE and VALUE of the boundary from the BOUNDARY DICTIONARY
            b2_type, b2_value = lookup(i, j, east_boundary)
            b3_type, b3_value = lookup(i, j, south_boundary)

            # create boundary dictionary
            boundary = {'loc': np.array([2, 3]),
                        'type': np.array([b2_type, b3_type]),
                        'value': np.array([b2_value, b3_value])}

            # create non-boundary dictionary
            non_boundary = {'loc': np.array([1, 4]),
                            'depth': np.array([z_array[i-1,j], z_array[i,j+1]])}

            # create well dictionary
            well = {'condition': well_condition[i, j],
                    'value': well_value[i, j],
                    'rw': well_rw[i, j],
                    'Gw': well_Gw[i, j]}

        if bound_loc[i, j] == 24:
            """""""""""
            MODIFY THIS W.R.T. THE GRID BLOCK LOCATION 
            """""""""""

            # get the TYPE and VALUE of the boundary from the BOUNDARY DICTIONARY
            b2_type, b2_value = lookup(i, j, east_boundary)
            b4_type, b4_value = lookup(i, j, north_boundary)

            # create boundary dictionary
            boundary = {'loc': np.array([2, 4]),
                        'type': np.array([b2_type, b4_type]),
                        'value': np.array([b2_value, b4_value])}

            # create non-boundary dictionary
            non_boundary = {'loc': np.array([1, 3]),
                            'depth': np.array([z_array[i-1,j], z_array[i,j-1]])}                            

            # create well dictionary
            well = {'condition': well_condition[i, j],
                    'value': well_value[i, j],
                    'rw': well_rw[i, j],
                    'Gw': well_Gw[i, j]}

        if bound_loc[i, j] == 1:
            """""""""""
            MODIFY THIS W.R.T. THE GRID BLOCK LOCATION 
            """""""""""

            # get the TYPE and VALUE of the boundary from the BOUNDARY DICTIONARY
            b1_type, b1_value = lookup(i, j, west_boundary)

            # create boundary dictionary
            boundary = {'loc': np.array([1]),
                        'type': np.array([b1_type]),
                        'value': np.array([b1_value])}

            # create non-boundary dictionary
            non_boundary = {'loc': np.array([2, 3, 4]),
                            'depth': np.array([z_array[i+1,j], z_array[i,j-1], 
                                               z_array[i,j+1]])}                            

            # create well dictionary
            well = {'condition': well_condition[i, j],
                    'value': well_value[i, j],
                    'rw': well_rw[i, j],
                    'Gw': well_Gw[i, j]}

        if bound_loc[i, j] == 2:
            """""""""""
            MODIFY THIS W.R.T. THE GRID BLOCK LOCATION 
            """""""""""

            # get the TYPE and VALUE of the boundary from the BOUNDARY DICTIONARY
            b2_type, b2_value = lookup(i, j, east_boundary)

            # create boundary dictionary
            boundary = {'loc': np.array([2]),
                        'type': np.array([b2_type]),
                        'value': np.array([b2_value])}

            # create non-boundary dictionary
            non_boundary = {'loc': np.array([1, 3, 4]),   
                            'depth': np.array([z_array[i-1,j], z_array[i,j-1], 
                                               z_array[i,j+1]])}                                                                                 

            # create well dictionary
            well = {'condition': well_condition[i, j],
                    'value': well_value[i, j],
                    'rw': well_rw[i, j],
                    'Gw': well_Gw[i, j]}

        if bound_loc[i, j] == 3:
            """""""""""
            MODIFY THIS W.R.T. THE GRID BLOCK LOCATION 
            """""""""""

            # get the TYPE and VALUE of the boundary from the BOUNDARY DICTIONARY
            b3_type, b3_value = lookup(i, j, south_boundary)

            # create boundary dictionary
            boundary = {'loc': np.array([3]),
                        'type': np.array([b3_type]),
                        'value': np.array([b3_value])}

            # create non-boundary dictionary
            non_boundary = {'loc': np.array([1, 2, 4]),
                            'depth': np.array([z_array[i-1,j], z_array[i+1,j], 
                                               z_array[i,j+1]])}                            
                            
            # create well dictionary
            well = {'condition': well_condition[i, j],
                    'value': well_value[i, j],
                    'rw': well_rw[i, j],
                    'Gw': well_Gw[i, j]}

        if bound_loc[i, j] == 4:
            """""""""""
            MODIFY THIS W.R.T. THE GRID BLOCK LOCATION 
            """""""""""

            # get the TYPE and VALUE of the boundary from the BOUNDARY DICTIONARY
            b4_type, b4_value = lookup(i, j, north_boundary)

            # create boundary dictionary
            boundary = {'loc': np.array([4]),
                        'type': np.array([b4_type]),
                        'value': np.array([b4_value])}

            # create non-boundary dictionary
            non_boundary = {'loc': np.array([1, 2, 3]),
                            'depth': np.array([z_array[i-1,j], z_array[i+1,j], 
                                               z_array[i,j-1]])}                                                        

            # create well dictionary
            well = {'condition': well_condition[i, j],
                    'value': well_value[i, j],
                    'rw': well_rw[i, j],
                    'Gw': well_Gw[i, j]}

        if bound_loc[i, j] == 0.0:
            """""""""""
            MODIFY THIS W.R.T. THE GRID BLOCK LOCATION 
            """""""""""
            # create boundary dictionary
            # no boundary
            boundary = {'loc': None,
                        'type': None,
                        'value': None}

            # create non-boundary dictionary
            non_boundary = {'loc': np.array([1, 2, 3, 4]),
                            'depth': np.array([z_array[i-1,j], z_array[i+1,j], 
                                               z_array[i,j-1], z_array[i,j+1]])}                             

            # create well dictionary
            well = {'condition': well_condition[i, j],
                    'value': well_value[i, j],
                    'rw': well_rw[i, j],
                    'Gw': well_Gw[i, j]}            

        """""""""""
        DO NOT MODIFY THIS
        """""""""""

        # calculate INTER-BLOCK transmissibilities
        T = transmissibility2d(dx, dy, dz, kx, ky, mu, B)
        T = np.array(T)

        # calculate BOUNDARY transmissibilities

        if bound_loc[i, j] == 0.0:
            # Interior blocks. All side are non-boundary, so flow are all inter-block
            T = T
            boundary['T'] = None

        else:
            # Boundary blocks.
            bound_T = []
            for k in range(len(boundary['loc'])):
                a = boundary['loc'][k]
                _ = transmissibility2d_boundary(boundary['loc'][k], boundary['type'][k],
                                                dx, dy, dz, kx, ky, mu, B)
                T[a - 1] = _
                bound_T.append(_)

            boundary['T'] = bound_T

        # calculate LHS coefficients
        px_min, px_plus, py_min, py_plus, p = lhs_coeffs2d_welltype(bound_loc[i, j],
                                                                    well, T, mu, B, 
                                                                    solver='incompressible') 

        # calculate potential term 
        # Equals 0. the grid block is not elevated
        potential_term = 0

        # calculate RHS constants
        rhs = rhs_constant2d_welltype(boundary, well, 0, dx, dy, 
                                      dz, kx, ky, mu, B, solver='incompressible')

        # fill in LHS matrix
        lhs_mat = fill2d_lhs_mat(bound_loc[i, j], block_index[i, j], xi, lhs_mat,
                                 px_min, px_plus, py_min, py_plus, p)

        # fill in RHS matrix
        rhs_mat = fill2d_rhs_mat(block_index[i, j], rhs_mat, rhs)

"""""""""""
PRESSURE SOLVER
"""""""""""
p_sol = np.linalg.solve(lhs_mat, rhs_mat)

p_sol = p_sol.T.reshape(-1)

"""""""""""
DISPLAY PRESSURE
"""""""""""

# display well
xsc = np.array(well_loc)[:,0]
ysc = np.array(well_loc)[:,1]

p_sol = p_sol.reshape(-1, xi)
plt.figure(figsize=(10,6))
plt.imshow(p_sol, cmap='rainbow', origin='lower')
plt.colorbar()
# plt.scatter(xsc, ysc, color='black')
plt.show()
