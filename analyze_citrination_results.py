import json
import os
import numpy as np
import math
import pandas as pd
import csv
import matplotlib.pyplot as plt

# Read in json file from obtained using citrination_retrieve_predicted_vals
# "/Users/vanessa/Documents/GitHub/better-glasses/PredictedValuesFromCitrination.txt"
filename = "C:/Users/mvane/Documents/GitHub/better-glasses/predictions_4416.txt"
log_rc_files = "C:/Users/mvane/Documents/Skunkworks/BMG/Data/rc_values.csv"
actual_values = "C:/Users/mvane/Documents/Skunkworks/BMG/Data/test_for_script.csv"	

# Make dictionaries of the actual values of the GFA metrics
# Read in values and make into numpy arrays
actual_vals = pd.read_csv(actual_values)
act_form = actual_vals['formula']
#act_tg = actual_vals['PROPERTY: Tg (K)']
#act_tl = actual_vals['PROPERTY: Tl (K)']
#act_tx = actual_vals['PROPERTY: Tx (K)']
act_trg = actual_vals['PROPERTY: Trg']
act_gamma = actual_vals['PROPERTY: $\gamma$']
act_omega = actual_vals['PROPERTY: $\omega$']

# Remove any NaN and replace with -100 (to flag for values that won't work)
# Create a matrix with each property in a row for each formula
all_act_props = [act_trg, act_gamma, act_omega]

for property in all_act_props:
	for i in range(0, len(act_form)):
		if math.isnan(property[i]):
			property[i] = -100
		else:
			pass

# Make a dictionary to hold all of the values later
values_dict = {}
# Zip together the lists we're trying to use as values in the dictionary
all_act_props = zip(act_trg, act_gamma, act_omega)
# Turn the zip object into a list because apparently zip objects can't do anything useful
all_act_props = list(all_act_props)

for i in range(len(act_form)):
    values_dict[act_form[i]] = all_act_props[i]


# Make arrays to hold the predicted values
pred_formulas = []
tg_vals = []
tl_vals = []
tx_vals = []
trg_vals = []
omega_vals = []
gamma_vals = []

# Extract the predicted value from the json holding the predictions
folder_out = "C:/Users/mvane/Documents/GitHub/better-glasses/predictions_output/"
for pred_json in list(os.listdir(folder_out)):
	print(pred_json)
	
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

temp_form = []
for f in pred_form:
	f_str = str(f)
	temp_form.append(f_str)
pred_form = temp_form	

tg_pred_err = np.asarray([tg[1] for tg in tg_vals])
tl_pred_err = np.asarray([tl[1] for tl in tl_vals])
tx_pred_err = np.asarray([tx[1] for tx in tx_vals])

# Check if the formulas are in the same order
for i in range(0, len(act_form)):
	if str(act_form[i]) == str(pred_form[i]):
		print("OK!")
	else:
		print("OH NOOOOOOOO!")
		print(act_form[i])
		print(pred_form[i])

# Calculate GFA metrics using the predicted values
trg_calc = tg_pred/tl_pred
gamma_calc = tg_pred/(tx_pred + tl_pred)
omega_calc = (tg_pred/tx_pred) - 2*(tg_pred/(tg_pred + tl_pred))
plt.figure()
plt.scatter(trg_pred, trg_calc, color = 'b')
#ax.scatter(trg_actual, trg_pred, color = 'r', marker = '^')

plt.title("Trg")
plt.xlabel("Actual Trg Value")
plt.ylabel("Calculated Trg Value")
plt.xlim([np.amin(trg_pred) + .1*(np.amax(trg_pred) - np.amin(trg_pred)), np.amax(trg_pred) + .1*(np.amax(trg_pred) - np.amin(trg_pred))])
plt.ylim([trg_calc.min(), trg_calc.max()])

plt.show()
		