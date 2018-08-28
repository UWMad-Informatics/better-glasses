import os
import numpy as np
import math
import pandas as pd
import csv
import matplotlib.pyplot as plt
import matplotlib
from sklearn.metrics import mean_squared_error

results_dir = "C:\\Users\\mvane\\Documents\\GitHub\\MAST-ML\\results\\LeaveOutEntireChem"

property = ""
all_data = {}

# For each folder in the results directory

results = []

for folder in os.listdir(results_dir):
	elements = []
	num_elements = []

	# For each split result in the split directory
	property = folder.split("_")[-1]
	f = os.path.join(results_dir, folder)
	split_dir = "StandardScaler\\DoNothing\\RandomForestRegressor"
	g = os.path.join(f, split_dir)	
	# formula = np.array([])
	# prediction = np.array([])
	ndme1 = []
	
	for file in os.listdir(g):
		if file != "RepeatedKFold":
			elements.append(file.split("_")[-1])
			
			ndme_data = pd.read_csv(os.path.join(g, os.path.join(file, "rmse_over_stdev_vs_group.csv"))).values
			ndme1_temp = ndme_data[1][0]
			if not np.isnan(ndme1_temp) and not np.isinf(ndme1_temp):
				ndme1.append(ndme1_temp)
			
			test_data = pd.read_csv(os.path.join(g, os.path.join(file, "split_1\\test.csv")))
			test_formulas = test_data['formula']
			num_elements.append(len(test_formulas))
			
	with open(str(property) + "_chemcv.csv", 'w', newline = '') as f:
		writer = csv.writer(f)
		header = ["element", "count", "ndme"]
		writer.writerow(header)
		rows = zip(elements, num_elements, ndme1)
		for row in rows:
			writer.writerow(row)
			
		
		for test in os.listdir(file):
			if "split_" in file:
				test_csv = pd.read_csv(os.path.join(os.path.join(g, file), "test.csv"))
				formula = np.append(formula, test_csv['formula'])
				prediction = np.append(prediction, test_csv['test_pred'])
			
	for i in range(0, len(formula)):
		if formula[i] not in all_data:
			all_data[formula[i]] = [{}]
			all_data[formula[i]][0][property] = prediction[i]			
		else:
			#all_data[formula[i]].append({})
			all_data[formula[i]][0][property] = prediction[i]

			

# Read in actual values collected from extracting data.
actual_values = "C:\\Users\\mvane\\Documents\\Skunkworks\\BMG\\Data\\BMG_full_dataset_with_energies.csv"	

# Read in values of actual data and make into numpy arrays
actual_vals = pd.read_csv(actual_values)
formulas = actual_vals['formula'].values
act_trg = actual_vals['PROPERTY: Trg'].values
act_gamma = actual_vals['PROPERTY: $\gamma$'].values
act_omega = actual_vals['PROPERTY: $\omega$'].values

act_tg = actual_vals['PROPERTY: Tg (K)'].values
act_tl = actual_vals['PROPERTY: Tl (K)'].values
act_tx = actual_vals['PROPERTY: Tx (K)'].values

# Read in csv file from obtained using citrination_retrieve_predicted_vals (predictions_output.csv)
predicted_csv = "summary_data.csv" #"predictions_output.csv"
predicted_data = pd.read_csv(predicted_csv)
tg_pred = predicted_data['Predicted Tg'].values
tl_pred = predicted_data['Predicted Tl'].values
tx_pred = predicted_data['Predicted Tx'].values

trg_pred = np.empty(0)
gamma_pred = np.empty(0)
omega_pred = np.empty(0)

pred_formula = list(all_data.keys())
pred_formula.sort()
for f in pred_formula:
	entry = all_data[f][0]
	if 'tg' in entry and 'tl' in entry:
		trg_pred = np.append(trg_pred, entry['tg']/entry['tl'])
		if 'tx' in entry:
			gamma_pred = np.append(gamma_pred, entry['tx']/(entry['tg'] + entry['tl']))
			omega_pred = np.append(omega_pred, (entry['tg']/entry['tx']) - 2*(entry['tg']/(entry['tg'] + entry['tl'])))
		else:
			gamma_pred = np.append(gamma_pred, np.nan)
			omega_pred = np.append(omega_pred, np.nan) 
	else:
		trg_pred = np.append(trg_pred, np.nan)
		gamma_pred = np.append(gamma_pred, np.nan)
		omega_pred = np.append(omega_pred, np.nan)

# Reformat np strings to plain old strings so they can be checked for equality later.
temp_form = []
for f in formulas:
	f_str = str(f)
	temp_form.append(f_str)
pred_form = temp_form	

# Check if the formulas are in the same order. Add formulas that are not to lists to remove.
remove_indices = []
counter = 0
for i in range(0, len(formulas)):
	if str(formulas[i]) != str(pred_form[i]):
		remove_indices.append(i)
		counter+=1
		print("bad formulas: " + str(pred_form[i]) + ", " + str(act_form[i]))
		
if len(remove_indices) != 0:
	for x in all_act_props:
		x = np.delete(x, remove_indices)
	print('Removed %d alloys from set due to mismatched formula orders.'%counter)
	
# Calculate stats for every property 
all_act_props = [act_trg, act_gamma, act_omega] #, act_tg, act_tl, act_tx]
all_pred_props = [trg_pred, gamma_pred, omega_pred] #, tg_pred, tl_pred, tx_pred]
names = ["Trg", "gamma", "omega"] #, "Tg", "Tl", "Tx"]
all_rmse = []
all_ndme = []
for x in range(0, len(all_act_props)):
	print(names[x])
	# Remove nan
	remove_indices = []
	copy_form = formulas
	print(len(all_act_props[x]))
	for i in range(0, len(all_act_props[x])):
		if np.isnan(all_act_props[x][i]) or np.isnan(all_pred_props[x][i]):
			remove_indices.append(i)
	all_pred_props[x] = np.delete(all_pred_props[x], remove_indices)
	all_act_props[x] = np.delete(all_act_props[x], remove_indices)
	copy_form = np.delete(copy_form, remove_indices)
	
	std = np.std(all_act_props[x])
	rmse = math.sqrt(mean_squared_error(all_act_props[x], all_pred_props[x]))
	ndme = rmse/std
	
	all_rmse.append(rmse)
	all_ndme.append(ndme)

	# Make some Parity plots
	plt.rc('font', size=20)          
	plt.rc('axes', titlesize=20)     
	plt.rc('axes', labelsize=20)
	plt.rc('xtick', labelsize=20)
	plt.rc('ytick', labelsize=20)
	plt.rc('figure', titlesize=20)
	f = plt.figure()
	ax = f.add_subplot(111)
	plt.scatter(all_act_props[x], all_pred_props[x], color='r', edgecolor='k')
	# Adds y = x line to scatter
	plt.plot(all_act_props[x], all_act_props[x], 'k')
	plt.title(names[x]) 
	plt.xlabel("Actual " + str(names[x]) + " Value")
	plt.ylabel("Predicted " + str(names[x]) + " Value")
	plt.text(.65,.05,"NDME: %.2f"%ndme, transform = ax.transAxes, fontsize=18)
	#plt.text(np.amin(all_act_props[x]) + .65*(np.amax(all_act_props[x]) - np.amin(all_act_props[x])), 
	#		np.amin(all_pred_props[x]) + .05*(np.amax(all_pred_props[x]) - np.amin(all_pred_props[x])), "NDME: %.2f"%ndme, fontsize=16)
	plt.tight_layout()
	plt.savefig(str(names[x]) + "_Parity.png")
	
	# Save data used to make plots to CSV
	with open(str(names[x]) + "_predictions.csv", 'w', newline = '') as outfile:
		wr = csv.writer(outfile)
		header = ["Formula", "Actual " + str(names[x]), "Predicted " + str(names[x])]
		wr.writerow(header)
		rows = zip(copy_form, all_act_props[x], all_pred_props[x])
		for row in rows:
			wr.writerow(row)
	outfile.close()
			
	with open(str(folder) + " RMSE and NDME.csv", 'w', newline = '') as fp:
		writer = csv.writer(fp)
		header = [""]
		#for x in names:
		#	header.append(x)
		writer.writerow(header)
		rmse = ["RMSE"]
		#for r in all_rmse:
		#	rmse.append(r)
		ndme = ["NDME"]
		for n in all_ndme:
			ndme.append(n)
		#writer.writerow(rmse)
		writer.writerow(ndme)	
	fp.close()
