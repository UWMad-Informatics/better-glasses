import pandas as pd
import os
import numpy as np
import math
from sklearn.metrics import mean_squared_error
from formula_prediction import FormulaPrediction

# Actual Data
#act_data = pd.read_csv("/Users/vanessa/Documents/Skunkworks/BMG/Data/BMG_full_dataset_with_energies.csv")
act_data = pd.read_csv("C:\\Users\\mvane\\Documents\\Skunkworks\\BMG\\Data\\BMG_full_dataset_with_energies - Copy.csv")
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

# Make a dictionary to hold predicted values for each formula
predict_junk = pd.read_csv("Au_predict_data.csv")
pred_form = predict_junk["formula"]
predictions_by_formula = []
for f in pred_form:
	predictions_by_formula.append(FormulaPrediction(f))
	
# Predicted data folder
#folder = "/Users/vanessa/Documents/Skunkworks/BMG/Data/Au Predictions"
folder = "C:\\Users\\mvane\\Documents\\Skunkworks\\BMG\\Data\\Tb Predictions"
for file in os.listdir(folder):
	predicted_data = pd.read_csv(os.path.join(folder, file))
	form = predicted_data['Formula']
	tg = predicted_data['Property Tg'].values
	tl = predicted_data['Property Tl'].values
	tx = predicted_data['Property Tx'].values
	
	num_predicted = len(form)
	trg = tg/tl
	gamma = tx/(tg + tl)
	omega = (tg/tx) - 2*(tg/(tg + tl))

	# Calculate absolute error
	# Loop through all the predictions in the file
	for i in range(0, num_predicted):
		formula = form[i]
		# Loop through all the possibl formulas in predictions_by_formula
		for p in predictions_by_formula:
			if p.formula == formula:
				if "Trg" in p.list_predicted_props():
					# Don't add nan values from original data
					if not math.isnan(act_dict[form[i]][trg_index]):
						p.update_prediction("Trg", math.sqrt(mean_squared_error([act_dict[form[i]][trg_index]],[trg[i]])))
					if not math.isnan(act_dict[form[i]][gamma_index]):
						p.update_prediction("gamma", math.sqrt(mean_squared_error([act_dict[form[i]][gamma_index]],[gamma[i]])))
					if not math.isnan(act_dict[form[i]][omega_index]):
						p.update_prediction("omega", math.sqrt(mean_squared_error([act_dict[form[i]][omega_index]],[omega[i]])))
				else:
					# Don't add nan values from original data
					if not math.isnan(act_dict[form[i]][trg_index]):
						p.add_prediction("Trg", math.sqrt(mean_squared_error([act_dict[form[i]][trg_index]],[trg[i]])))
					if not math.isnan(act_dict[form[i]][gamma_index]):
						p.add_prediction("gamma", math.sqrt(mean_squared_error([act_dict[form[i]][gamma_index]],[gamma[i]])))
					if not math.isnan(act_dict[form[i]][omega_index]):
						p.add_prediction("omega", math.sqrt(mean_squared_error([act_dict[form[i]][omega_index]],[omega[i]])))

# Calculate the error on each metric for each formula
for k in predictions_by_formula:
	print(k.formula)
	for j in k.list_predicted_props():
		print(str(j) + ": " + str(np.mean(k.retrieve_predictions(j))))