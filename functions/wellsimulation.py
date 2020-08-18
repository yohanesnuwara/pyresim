"""
Code for calculating the FBHP and flow rate solution after solving pressure in each grid block
Producing well report

@author: Yohanes Nuwara
@email: ign.nuwara97@gmail.com
"""

def solution_well1d(well_df, p_sol):
  """
  Calculate Well FBHP and Rate after pressure has been solved

  If well condition:
  * 'constant_fbhp': rate estimated from FBHP, FBHP = FBHP
  * 'constant_rate': rate = rate, FBHP estimated from rate
  * 'shutin': rate = 0, FBHP equals to the solved grid pressure (= p_sol)

  Input:

  well_df = well dataframe
  p_sol = pressure solution (array)

  """
  import numpy as np

  num_of_wells = well_df['well_name'].count()

  rate_sol = []
  fbhp_sol = []

  for i in range(num_of_wells):
    if well_df['well_condition'].iloc[i] == 'constant_rate':
      mu, B, Gw, qsc = well_df['well_mu'].iloc[i], well_df['well_B'].iloc[i], well_df['well_Gw'].iloc[i], well_df['well_value'].iloc[i]
      loc = well_df['well_loc'].iloc[i]      
      p_sol_ = p_sol[loc-1] 

      factor = Gw / (mu * B)
      pwf = (qsc + (factor * p_sol_)) / factor 
      qsc = qsc

    if well_df['well_condition'].iloc[i] == 'constant_fbhp':
      mu, B, Gw, pwf = well_df['well_mu'].iloc[i], well_df['well_B'].iloc[i], well_df['well_Gw'].iloc[i], well_df['well_value'].iloc[i]
      loc = well_df['well_loc'].iloc[i]
      p_sol_ = p_sol[loc-1]      
      pwf = pwf
      qsc = -(Gw / (mu * B)) * (p_sol_ - pwf)  

    if well_df['well_condition'].iloc[i] == 'shutin': 
      loc = well_df['well_loc'].iloc[i]
      p_sol_ = p_sol[loc-1]       
      pwf = p_sol_
      qsc = 0

    if well_df['well_condition'].iloc[i] == 'constant_pressuregrad':     
      pwf = np.nan
      qsc = np.nan
    
    fbhp_sol.append(float(pwf))
    rate_sol.append(float(qsc))
  
  well_df['fbhp_sol'] = fbhp_sol
  well_df['rate_sol'] = rate_sol

  return well_df

def solution_well2d(well_df, p_sol):
  """
  Calculate Well FBHP and Rate after pressure has been solved
  2D reservoir

  If well condition:
  * 'constant_fbhp': rate estimated from FBHP, FBHP = FBHP
  * 'constant_rate': rate = rate, FBHP estimated from rate
  * 'shutin': rate = 0, FBHP equals to the solved grid pressure (= p_sol)

  Input:

  well_df = well dataframe
  p_sol = pressure solution (2D array)

  """
  import numpy as np

  num_of_wells = well_df['well_name'].count()

  rate_sol = []
  fbhp_sol = []

  for i in range(num_of_wells):
    if well_df['well_condition'].iloc[i] == 'constant_rate':
      mu, B, Gw, qsc = well_df['well_mu'].iloc[i], well_df['well_B'].iloc[i], well_df['well_Gw'].iloc[i], well_df['well_value'].iloc[i]
      loc = well_df['well_loc'].iloc[i]      

      # pressure (solution) at the well block
      xsc = (well_df['well_loc'].iloc[i])[0] - 1
      ysc = (well_df['well_loc'].iloc[i])[1] - 1      
      p_sol_ = p_sol[xsc, ysc]

      factor = Gw / (mu * B)
      pwf = (qsc + (factor * p_sol_)) / factor 
      qsc = qsc

    if well_df['well_condition'].iloc[i] == 'constant_fbhp':
      mu, B, Gw, pwf = well_df['well_mu'].iloc[i], well_df['well_B'].iloc[i], well_df['well_Gw'].iloc[i], well_df['well_value'].iloc[i]
      loc = well_df['well_loc'].iloc[i]
     
      # pressure (solution) at the well block
      xsc = (well_df['well_loc'].iloc[i])[0] - 1
      ysc = (well_df['well_loc'].iloc[i])[1] - 1      
      p_sol_ = p_sol[xsc, ysc]      
      
      pwf = pwf
      qsc = -(Gw / (mu * B)) * (p_sol_ - pwf)  

    if well_df['well_condition'].iloc[i] == 'shutin': 
      loc = well_df['well_loc'].iloc[i]

      # pressure (solution) at the well block
      xsc = (well_df['well_loc'].iloc[i])[0] - 1
      ysc = (well_df['well_loc'].iloc[i])[1] - 1      
      p_sol_ = p_sol[xsc, ysc]    
      
      pwf = p_sol_
      qsc = 0

    if well_df['well_condition'].iloc[i] == 'constant_pressuregrad':     
      pwf = np.nan
      qsc = np.nan
    
    fbhp_sol.append(float(pwf))
    rate_sol.append(float(qsc))
  
  well_df['fbhp_sol'] = fbhp_sol
  well_df['rate_sol'] = rate_sol

  return well_df

def well1d_report_slicomp(well_name, wells, well_df, p_sol_record, p_initial, schedule):
  """
  Produce well report of a well of interest, consisting of calculated
  FBHP and flow rate over time-evolved

  Input:

  well_name = name of the well of interest (string)
  wells = well information dictionary
  well_df = well information dataframe
  p_sol_record = array of pressure solved over timesteps
  p_initial = initial pressure array
  schedule = length of simulation

  Output:

  well_report = output dataframe
  """
  import numpy as np
  
  def solution_well1d_slicomp(well_df, p_sol):
    if well_df['well_condition'] == 'constant_rate':
      mu, B, Gw, qsc = well_df['well_mu'], well_df['well_B'], well_df['well_Gw'], well_df['well_value']

      factor = Gw / (mu * B)
      pwf = (qsc + (factor * p_sol)) / factor 
      qsc = qsc

    if well_df['well_condition'] == 'constant_fbhp':
      mu, B, Gw, pwf = well_df['well_mu'], well_df['well_B'], well_df['well_Gw'], well_df['well_value']    
      pwf = pwf
      qsc = -(Gw / (mu * B)) * (p_sol - pwf)  

    if well_df['well_condition'] == 'shutin':   
      pwf = p_sol
      qsc = 0

    if well_df['well_condition'] == 'constant_pressuregrad':     
      pwf = np.nan
      qsc = np.nan

    return pwf, qsc

  # get the well index from the wells dictionary
  well_index = np.where(wells['well_name']==well_name)[0][0]

  # get the grid block location 
  xsc = (wells['well_loc'])[well_index]

  # slice the well_df dataframe that consists the well of interest
  well_df2 = well_df.iloc[well_index]

  # get the pressure at time evolution
  xsc = np.int64(xsc) - 1
  p_sol2 = [np.float64(i[xsc]) for i in p_sol_record]
  p_sol2 = np.append(p_initial[xsc], p_sol2)

  # iterate over the time-evolved pressure to calculate FBHP and rate
  fbhp_sol = []; rate_sol = []
  for i in range(len(p_sol2)):
    pwf, qsc = solution_well1d_slicomp(well_df2, p_sol2[i])
    fbhp_sol.append(pwf); rate_sol.append(qsc)

  # create well report dataframe
  timestep = np.arange(0, schedule+1)
  well_report = pd.DataFrame({'time (day)': timestep, 'grid block pressure (psi)': p_sol2, 
                              'fbhp_sol (psi)': fbhp_sol, 'rate_sol (STB/D)': rate_sol}) 

  return well_report  

def well2d_report_slicomp(well_name, well_df, p_sol, schedule):
  """
  Produce well report of a well of interest, consisting of calculated
  FBHP and flow rate over time-evolved

  Input:

  well_name = name of the well of interest (string)
  well_df = well information dataframe
  p_sol = array of pressure solved over timesteps
  p_initial = initial pressure array
  schedule = length of simulation

  Output:

  well_report = output dataframe
  """
  import numpy as np
  
  def solution_well2d_slicomp(well_df, p_sol):
    if well_df['well_condition'].values == 'constant_rate':
      mu, B, Gw, qsc = well_df['well_mu'].values, well_df['well_B'].values, well_df['well_Gw'].values, well_df['well_value'].values

      factor = Gw / (mu * B)
      pwf = (qsc + (factor * p_sol)) / factor 
      qsc = qsc

    if well_df['well_condition'].values == 'constant_fbhp':
      mu, B, Gw, pwf = well_df['well_mu'].values, well_df['well_B'].values, well_df['well_Gw'].values, well_df['well_value'].values    
      pwf = pwf
      qsc = -(Gw / (mu * B)) * (p_sol - pwf)  

    if well_df['well_condition'].values == 'shutin':   
      pwf = p_sol
      qsc = 0

    if well_df['well_condition'].values == 'constant_pressuregrad':     
      pwf = np.nan
      qsc = np.nan

    return pwf, qsc

  # get the well index from the wells dictionary
  well_index = np.where(well_df['well_name']==well_name)[0][0]

  # get the grid block location (x-y coordinate)
  xysc = (well_df['well_loc'])[well_index]
  xsc = xysc[0] - 1
  ysc = xysc[1] - 1

  # get the pressure at time evolution
  p_sol2 = [np.float64(i[xsc,ysc]) for i in p_sol]

  # get the dataframe well_df that contains well of interest
  well_df2 = well_df.loc[well_df['well_name'] == well_name]

  # iterate over the time-evolved pressure to calculate FBHP and rate
  fbhp_sol = []; rate_sol = []
  for i in range(len(np.array(p_sol2))):
    pwf, qsc = solution_well2d_slicomp(well_df2, p_sol2[i])
    fbhp_sol.append(pwf); rate_sol.append(qsc)
  
  fbhp_sol = np.array(fbhp_sol).reshape(-1)
  rate_sol = np.array(rate_sol).reshape(-1)

  # create well report dataframe
  timestep = np.arange(0, schedule+1)
  well_report = pd.DataFrame({'time (day)': timestep, 'grid block pressure (psi)': p_sol2, 
                              'fbhp_sol (psi)': fbhp_sol, 'rate_sol (STB/D)': rate_sol}) 

  return well_report
