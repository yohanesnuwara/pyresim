"""
Code for calculating the FBHP and flow rate solution after solving pressure in each grid block
Producing well report

@author: Yohanes Nuwara
@email: ign.nuwara97@gmail.com
"""

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
