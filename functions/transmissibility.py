# calculate transmissibility of cylindrical grid (geom factor from Table 4-3, Abou-Kassem p. 99)

def trans_r_min(dz_now, dz_prev, dtheta, alpha_tg, kh_now, kh_prev, mu, B):
  """
  Calculate transmissibility of cylindrical grid in r- direction
  """
  # transmissibility geometric factor
  G_trans_r_min = (.001127 * dtheta) / (np.log(alpha_tg * np.log(alpha_tg) / (alpha_tg - 1)) / (dz_now * kh_now) + np.log((alpha_tg - 1) / np.log(alpha_tg)) / (dz_prev * kh_prev))
  # calculate transmissibility
  T_r_min = G_trans_r_min / (mu * B)
  return T_r_min

def trans_r_plus(dz_now, dz_next, dtheta, alpha_tg, kh_now, kh_next, mu, B):
  """
  Calculate transmissibility of cylindrical grid in r+ direction
  """
  # transmissibility geometric factor
  G_trans_r_plus = (.001127 * dtheta) / (np.log((alpa_tg - 1) / np.log(alpha_tg)) / (dz_now * kh_now) + np.log(alpha_tg * np.log(alpha_tg) / (alpha_tg - 1)) / (dz_next * kh_next))
  # calculate transmissibility
  T_r_plus = G_trans_r_plus / (mu * B)
  return T_r_plus

def trans_z_min(dz_now, dz_prev, dv_now, kz_now, kz_prev, mu, B):
  """
  Calculate transmissibility of cylindrical grid in z- direction
  """
  # transmissibility geometric factor
  G_trans_z_min = (2 * .001127 * (dv_now / dz_now)) / ((dz_now / kz_now) + (dz_prev / kz_prev))
  # calculate transmissibility
  T_z_min = G_trans_z_min / (mu * B)
  return T_z_min

def trans_z_plus(dz_now, dz_next, dv_now, kz_now, kz_next, mu, B):
  """
  Calculate transmissibility of cylindrical grid in z+ direction
  """
  # transmissibility geometric factor
  G_trans_z_plus = (2 * .001127 * (dv_now / dz_now)) / ((dz_now / kz_now) + (dz_next / kz_next))
  # calculate transmissibility
  T_z_plus = G_trans_z_plus / (mu * B)
  return T_z_plus

def trans_theta_min(dz_now, dz_prev, alpha_tg, dtheta_now, dtheta_prev, ktheta_now, ktheta_prev, mu, B):
  """
  Calculate transmissibility of cylindrical grid in θ- direction
  """
  # transmissibility geometric factor
  G_trans_theta_min = (2 * .001127 * np.log(alpha_tg)) / ((dtheta_now / (dz_now * ktheta_now)) + (dtheta_prev / (dz_prev * ktheta_prev)))
  # calculate transmissibility
  T_theta_min = G_trans_theta_min / (mu * B)
  return T_theta_min

def trans_theta_plus(dz_now, dz_next, alpha_tg, dtheta_now, dtheta_next, ktheta_now, ktheta_next, mu, B):
  """
  Calculate transmissibility of cylindrical grid in θ+ direction
  """
  # transmissibility geometric factor
  G_trans_theta_plus = (2 * .001127 * np.log(alpha_tg)) / ((dtheta_now / (dz_now * ktheta_now)) + (dtheta_next / (dz_next * ktheta_next)))
  # calculate transmissibility
  T_theta_plus = G_trans_theta_plus / (mu * B)
  return T_theta_plus
