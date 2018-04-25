import json
import os
import numpy as np
import math
import pandas as pd
import csv
import matplotlib.pyplot as plt
import matplotlib
from sklearn.metrics import mean_squared_error

# Read in actual values collected from extracting data.
actual_values = "C:/Users/mvane/Documents/Skunkworks/BMG/Data/test_for_script.csv"	

# Make dictionaries of the actual values of the GFA metrics
# Read in values and make into numpy arrays
actual_vals = pd.read_csv(actual_values)
act_form = actual_vals['formula']
#act_tg = actual_vals['PROPERTY: Tg (K)']
#act_tl = actual_vals['PROPERTY: Tl (K)']
#act_tx = actual_vals['PROPERTY: Tx (K)']
act_trg = actual_vals['PROPERTY: Trg'].as_matrix()
act_gamma = actual_vals['PROPERTY: $\gamma$'].as_matrix()
act_omega = actual_vals['PROPERTY: $\omega$'].as_matrix()

# Remove any NaN and replace with -100 (to flag for values that won't work)
# Create a matrix with each property in a row for each formula
all_act_props = [act_trg, act_gamma, act_omega]

for property in all_act_props:
	for i in range(0, len(act_form)):
		if math.isnan(property[i]):
			property[i] = -100
		else:
			pass

# Make arrays to hold the predicted values
pred_formulas = []
tg_vals = []
tl_vals = []
tx_vals = []
trg_vals = []
omega_vals = []
gamma_vals = []

# Read in json file from obtained using citrination_retrieve_predicted_vals
# Extract the predicted value from the json holding the predictions
folder_out = "C:/Users/mvane/Documents/GitHub/better-glasses/predictions_output/"
for pred_json in list(os.listdir(folder_out)):	
	# Open the predicted values json
	with open(folder_out + pred_json) as file:
		all_data = json.load(file)
		
	tg_vals.append(all_data['candidates'][0]['Property Tg'])
	tl_vals.append(all_data['candidates'][0]['Property Tl'])
	tx_vals.append(all_data['candidates'][0]['Property Tx'])
	trg_vals.append(all_data['candidates'][0]['Property Trg'])
	omega_vals.append(all_data['candidates'][0]['Property $\\omega$'])
	gamma_vals.append(all_data['candidates'][0]['Property $\\gamma$'])
	pred_formulas.append(all_data['candidates'][0]['formula'])

# Turn the tuple of [prediction, uncertainty] into 2 lists for each temp and for Trg, gamma, and omega
tg_pred = np.asarray([tg[0] for tg in tg_vals])
tl_pred = np.asarray([tl[0] for tl in tl_vals])
tx_pred = np.asarray([tx[0] for tx in tx_vals])
trg_pred = np.asarray([trg[0] for trg in trg_vals])
omega_pred = np.asarray([omega[0] for omega in omega_vals])
gamma_pred = np.asarray([gamma[0] for gamma in gamma_vals])
pred_form = np.asarray([form[0] for form in pred_formulas])

# Reformat np strings to plain old strings so they can be checked for equality later.
temp_form = []
for f in pred_form:
	f_str = str(f)
	temp_form.append(f_str)
pred_form = temp_form	

tg_pred_err = np.asarray([tg[1] for tg in tg_vals])
tl_pred_err = np.asarray([tl[1] for tl in tl_vals])
tx_pred_err = np.asarray([tx[1] for tx in tx_vals])

# Check if the formulas are in the same order. Add formulas that are not to lists to remove.
remove_indices = []
counter = 0
for i in range(0, len(act_form)):
	if str(act_form[i]) != str(pred_form[i]):
		remove_indices.append(i)
		counter+=1
	else:
		pass
		
if len(remove_indices) != 0:
	act_trg = np.delete(act_trg, remove_indices)
	act_gamma = np.delete(act_gamma, remove_indices)
	act_omega = np.delete(act_omega, remove_indices)
	tg_pred = np.delete(tg_pred, remove_indices)
	tl_pred = np.delete(tl_pred, remove_indices)
	tx_pred = np.delete(tx_pred, remove_indices)
	print('Removed %d alloys from set due to mismatched formula orders.'%counter)
else:
	pass

# Calculate GFA metrics using the predicted values
trg_calc = tg_pred/tl_pred
gamma_calc = tg_pred/(tx_pred + tl_pred)
omega_calc = (tg_pred/tx_pred) - 2*(tg_pred/(tg_pred + tl_pred))

# Filter out any actual values of -100 (which was set earlier to flag places w/o a value)
# in both the calculated and the actual GFA arrays
trg_delete = []
gamma_delete = []
omega_delete = []
for i in range(0, len(act_trg)):
	if act_trg[i] < 0:
		trg_delete.append(i)
	else:
		pass
	if act_gamma[i] < 0:
		gamma_delete.append(i)
	else:
		pass
	if act_omega[i] < 0:
		omega_delete.append(i)
	else:
		pass
		
act_trg = np.delete(act_trg, trg_delete)
trg_calc = np.delete(trg_calc, trg_delete)
act_gamma = np.delete(act_gamma, gamma_delete)
gamma_calc = np.delete(gamma_calc, gamma_delete)
act_omega = np.delete(act_omega, omega_delete)
omega_calc = np.delete(omega_calc, omega_delete)

# Compare to actual GFA values
trg_error = abs(trg_calc - act_trg)
gamma_error = abs(gamma_calc - act_gamma)
omega_error = abs(omega_calc - act_omega)
trg_rmse = math.sqrt(mean_squared_error(act_trg, trg_calc))
gamma_rmse = math.sqrt(mean_squared_error(act_gamma, gamma_calc))
omega_rmse = math.sqrt(mean_squared_error(act_omega, omega_calc))
print("Trg RMSE: " + str(trg_rmse))
print("Gamma RMSE: " + str(gamma_rmse))
print("Omega RMSE: " + str(omega_rmse))

trg_std = np.std(act_trg)
gamma_std = np.std(act_gamma)
omega_std = np.std(act_omega)

trg_ndme = trg_rmse/trg_std
gamma_ndme = gamma_rmse/gamma_std
omega_ndme = omega_rmse/omega_std
print("Trg NDME: " + str(trg_ndme))
print("Gamma NDME: " + str(gamma_ndme))
print("Omega NDME: " + str(omega_ndme))


# Make some plots of each GFA metrics
for i in ["Trg", "$\gamma", "$\omega"]:	
	plt.rc('font', size=20)          
	plt.rc('axes', titlesize=20)     
	plt.rc('axes', labelsize=20)
	plt.rc('xtick', labelsize=20)
	plt.rc('ytick', labelsize=20)
	plt.rc('figure', titlesize=20)
	if i == "Trg":
		plt.figure()
		plt.scatter(act_trg, trg_calc)
		# Adds y = x line to scatter
		plt.plot([0,1], 'k')
		plt.title("Trg")
		plt.xlabel("Actual Trg Value")
		plt.ylabel("Calculated Trg Value")
		plt.tight_layout()
		plt.savefig('Trg_parity.png')
	elif i == "$\gamma":
		plt.figure()
		plt.scatter(act_gamma, gamma_calc)
		# Adds y = x line to scatter
		plt.plot([0,1], 'k')
		plt.title('$%s$'%'\\gamma')
		plt.xlabel('Actual $%s$ Value'%'\\gamma')
		plt.ylabel('Calculated $%s$ Value'%'\\gamma')
		plt.tight_layout()
		plt.savefig('gamma_parity.png')
	else:
		plt.figure()
		plt.scatter(act_omega, omega_calc)
		# Adds y = x line to scatter
		plt.plot([0,1], 'k')
		plt.title('$%s$'%'\\omega')
		plt.xlabel('Actual $%s$ Value'%'\\omega')
		plt.ylabel('Calculated $%s$ Value'%'\\omega')
		plt.tight_layout()
		plt.savefig('omega_parity.png')
