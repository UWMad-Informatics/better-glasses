import pandas as pd
import os
import numpy as np
import math
from sklearn.metrics import mean_squared_error

# Actual Data
#act_data = pd.read_csv("/Users/vanessa/Documents/Skunkworks/BMG/Data/BMG_full_dataset_with_energies.csv")
act_data = pd.read_csv("C:\\Users\\mvane\\Documents\\Skunkworks\\BMG\\Data\\BMG_full_dataset_with_energies.csv")
act_form = act_data['formula'].values
act_trg = act_data['PROPERTY: Trg'].values
act_gamma = act_data['PROPERTY: $\\gamma$'].values
act_omega = act_data['PROPERTY: $\\omega$'].values

# Compute Stdev of each array, ignoring nan's
trg_std = np.nanstd(act_trg)
gamma_std = np.nanstd(act_gamma)
omega_std = np.nanstd(act_omega)

for arr in [act_trg,act_gamma,act_omega]:
	arr = np.nan_to_num(arr).tolist()

# Covert to dict with key as formula and a list with Trg, gamma, omega
act_dict = {}
for i in range(0, len(act_form)):
	act_dict[act_form[i]] = [act_trg[i], act_gamma[i], act_omega[i]]
trg_index = 0
gamma_index = 1
omega_index = 2

#TODO: figure out how to not hard code this
avg_trg_err = [0,0,0,0,0,0]
avg_gamma_err = [0,0,0,0,0,0]
avg_omega_err = [0,0,0,0,0,0]

# Predicted data folder
#folder = "/Users/vanessa/Documents/Skunkworks/BMG/Data/Au Predictions"
folder = "C:\\Users\\mvane\\Documents\\Skunkworks\\BMG\\Data\\Tb Predictions"
for file in os.listdir(folder):
	predicted_data = pd.read_csv(os.path.join(folder, file))
	form = predicted_data['formula']
	tg = predicted_data['Property Tg'].values
	tl = predicted_data['Property Tl'].values
	tx = predicted_data['Property Tx'].values
	
	num_predicted = len(form)
	trg = tg/tl
	gamma = tx/(tg + tl)
	omega = (tg/tx) - 2*(tg/(tg + tl))

	trg_loss = np.empty(num_predicted)
	gamma_loss = np.empty(num_predicted)
	omega_loss = np.empty(num_predicted)

	# Calculate absolute error
	for i in range(0, num_predicted):
		# Don't add nan values from original data
		if not math.isnan(act_dict[form[i]][trg_index]):
			trg_loss = np.append(trg_loss, math.sqrt(mean_squared_error([act_dict[form[i]][trg_index]],[trg[i]])))
		if not math.isnan(act_dict[form[i]][gamma_index]):
			gamma_loss = np.append(gamma_loss, math.sqrt(mean_squared_error([act_dict[form[i]][gamma_index]],[gamma[i]])))
		if not math.isnan(act_dict[form[i]][omega_index]):
			omega_loss = np.append(omega_loss, math.sqrt(mean_squared_error([act_dict[form[i]][omega_index]],[omega[i]])))

		temp_trg_err = np.mean(trg_loss).tolist()
		temp_gamma_err = np.mean(gamma_loss).tolist()
		temp_omega_err = np.mean(omega_loss).tolist()

		# Check to make sure there are already values at each position
		if avg_trg_err[num_predicted-1] != 0:
			avg_trg_err[num_predicted-1] = np.mean([temp_trg_err, avg_trg_err[num_predicted-1]])
			avg_gamma_err[num_predicted-1] = np.mean([temp_gamma_err, avg_gamma_err[num_predicted-1]])
			avg_omega_err[num_predicted-1] = np.mean([temp_omega_err, avg_omega_err[num_predicted-1]])
		else:
			avg_trg_err[num_predicted-1] = temp_trg_err
			avg_gamma_err[num_predicted-1] = temp_gamma_err
			avg_omega_err[num_predicted-1] = temp_omega_err

print("Trg NDME: " + str(avg_trg_err))
print("Gamma NDME: " + str(avg_gamma_err))
print("Omega NDME: " + str(avg_omega_err))
