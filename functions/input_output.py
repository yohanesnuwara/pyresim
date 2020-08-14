"""
Codes for input-output of PyReSim

@author: Yohanes Nuwara
@email: ign.nuwara97@gmail.com
"""

def read_input(filepath):
  """
  Read input data (TXT file)

  Input:

  filepath = path to the input file (TXT format)

  Output:

  reservoir_input = reservoir data input (as Python dictionary format)
  contains:
  xi, yi, dx, dy, dz, kx, ky, kz, poro, rho, cpore, mu, B

  west_boundary, east_boundary, south_boundary, north_boundary = 
  reservoir boundary information (as Python dictionary format)
  contains: 
  * type (boundary type: 'constant_pressure', 'constant_pressuregrad', 'constant_rate', 'no_flow')
  * loc (location of grid blocks: either 'all' means all gridblocks have the same boundary, OR the specified coordinates)
  * value (boundary value: 'constant_pressure' in psi, 'constant_pressuregrad' in psi/ft, 'constant_rate' in STB/D)

  well = well information (as Python dictionary format)  
  contains:
  * name (well name)
  * rw (well radius in inch)
  * loc = (well coordinate)
  * skin (well skin)
  * well_config (well configuration for wells in the RESERVOIR BOUNDARY: 0, 1, 2, and 3. See DOCS for details)  
  * condition (well operating conditions: 'constant_fbhp', 'constant_pressuregrad', 'constant_rate', 'shutin')
  * value (value of the operating conditions: 'constant_fbhp' in psi, 'constant_pressuregrad' in psi/ft, 'constant_rate' in STB/D)

  """
  import numpy as np

  # reservoir input
  prop = np.loadtxt(filepath, max_rows=1, skiprows=12)
  xi, yi, zi = (prop[0]).astype(int), (prop[1]).astype(int), (prop[2]).astype(int)
  dx, dy, dz = prop[3], prop[4], prop[5]
  kx, ky, kz, poro, rho = prop[6], prop[7], prop[8], prop[9], prop[10]
  cpore, mu, B = prop[11], prop[12], prop[13]

  if yi==0 and zi==0:
    # reservoir is 1D

    ## create reservoir input dictionary
    reservoir_input = {'xi': xi, 'dx': dx, 'kx': kx, 'poro': poro, 'rho': rho, 
                       'cpore': cpore, 'mu': mu, 'B': B}

    # well input
    skiprow_wells = np.array([22,25,28,31,37,40])
    wells = []
    for i in range(len(skiprow_wells)):
      well = np.loadtxt(filepath, max_rows=1, skiprows=skiprow_wells[i], delimiter=',')
      wells.append(well)

    well_xsc, well_rw, well_skin, well_value, well_config = wells[0], wells[2], wells[3], wells[4], wells[5]
    well_name = np.loadtxt(filepath, max_rows=1, skiprows=19, delimiter=',', dtype=np.str) 
    well_condition = np.loadtxt(filepath, max_rows=1, skiprows=34, delimiter=',', dtype=np.str)

    well_loc = well_xsc.tolist()

    ## create well information dictionary
    well = {'well_name': well_name,
            'well_loc': well_loc,
            'well_rw': well_rw,
            'well_skin': well_skin,
            'well_condition': well_condition,
            'well_value': well_value,
            'well_config': well_config}

    # reservoir boundary
    skiprow_type = np.array([54, 67])
    skiprow_value = np.array([57, 70])
    skiprow_loc = np.array([51, 64])

    btype = []; bvalue = []; bloc = []
    for i in range(len(skiprow_type)):
      type = np.loadtxt(filepath, max_rows=1, skiprows=skiprow_type[i], dtype=np.str)
      value = np.loadtxt(filepath, max_rows=1, skiprows=skiprow_value[i])
      loc = np.loadtxt(filepath, max_rows=1, skiprows=skiprow_loc[i], dtype=np.str)
      btype.append(type); bvalue.append(value); bloc.append(loc)

    west_type, east_type = btype[0], btype[1]
    west_value, east_value = bvalue[0], bvalue[1]
    west_loc, east_loc = bloc[0], bloc[1]

    ## create reservoir boundary information

    east_boundary = {"type": east_type,
                      "value": east_value,
                      "loc": east_loc}

    west_boundary = {"type": west_type,
                      "value": west_value,
                      "loc": west_loc} 

    return reservoir_input, well, west_boundary, east_boundary 

  if yi!=0 and zi==0:
    # reservoir is 2D

    ## create reservoir input dictionary
    reservoir_input = {'xi': xi, 'yi': yi, 'dx': dx, 'dy': dy, 'dz': dz, 'kx': kx, 
                        'ky': ky, 'poro': poro, 'rho': rho, 'cpore': cpore, 
                        'mu': mu, 'B': B}

    # well input
    skiprow_wells = np.array([22,25,28,31,37,40])
    wells = []
    for i in range(len(skiprow_wells)):
      well = np.loadtxt(filepath, max_rows=1, skiprows=skiprow_wells[i], delimiter=',')
      wells.append(well)

    well_xsc, well_ysc, well_rw, well_skin, well_value, well_config = wells[0], wells[1], wells[2], wells[3], wells[4], wells[5]
    well_name = np.loadtxt(filepath, max_rows=1, skiprows=19, delimiter=',', dtype=np.str) 
    well_condition = np.loadtxt(filepath, max_rows=1, skiprows=34, delimiter=',', dtype=np.str)

    ## merge the xsc and ysc well coordinates into one coordinate
    well_loc = np.zeros((len(well_xsc),2))
    for i in range(len(well_xsc)):
      well_loc[i] = [well_xsc[i], well_ysc[i]]

    well_loc = well_loc.astype(int)
    well_loc = well_loc.tolist()

    ## create well information dictionary
    well = {'well_name': well_name,
            'well_loc': well_loc,
            'well_rw': well_rw,
            'well_skin': well_skin,
            'well_condition': well_condition,
            'well_value': well_value,
            'well_config': well_config}

    # reservoir boundary
    skiprow_type = np.array([54, 67, 80, 93])
    skiprow_value = np.array([57, 70, 83, 96])
    skiprow_loc = np.array([51, 64, 77, 90])

    btype = []; bvalue = []; bloc = []
    for i in range(len(skiprow_type)):
      type = np.loadtxt(filepath, max_rows=1, skiprows=skiprow_type[i], dtype=np.str)
      value = np.loadtxt(filepath, max_rows=1, skiprows=skiprow_value[i])
      loc = np.loadtxt(filepath, max_rows=1, skiprows=skiprow_loc[i], dtype=np.str)
      btype.append(type); bvalue.append(value); bloc.append(loc)

    west_type, east_type, south_type, north_type = btype[0], btype[1], btype[2], btype[3]
    west_value, east_value, south_value, north_value = bvalue[0], bvalue[1], bvalue[2], bvalue[3]
    west_loc, east_loc, south_loc, north_loc = bloc[0], bloc[1], bloc[2], bloc[3]

    ## create reservoir boundary information

    east_boundary = {"type": east_type,
                      "value": east_value,
                      "loc": east_loc}

    west_boundary = {"type": west_type,
                      "value": west_value,
                      "loc": west_loc}

    north_boundary = {"type": north_type,
                      "value": north_value,
                      "loc": north_loc}

    south_boundary = {"type": south_type,
                      "value": south_value,
                      "loc": south_loc}   

    return reservoir_input, well, west_boundary, east_boundary, south_boundary, north_boundary 
