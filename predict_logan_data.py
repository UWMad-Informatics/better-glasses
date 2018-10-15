# This file is a method that takes in a csv with formula and formation energy for some BMG's
# and make predictions on a given data view on citrination.
# Predictions are written to a csv called predictions_output.csv
import csv
import pandas as pd
import numpy as np
import os
from sklearn.metrics import f1_score, roc_curve, auc
import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt

# Define cutoff value to check against than for GFA
TRG_CUTOFF = .67
GAMMA_CUTOFF_MIN = .35
GAMMA_CUTOFF_MAX = .5
OMEGA_CUTOFF = .3
LOG_RC_CUTOFF = 6

def main():
	# Read in experimental data
	exp_file = "pifs.csv"
	exp_data = pd.read_csv(exp_file)
	actual_gfa = exp_data['Glass forming ability'].values

	# Loop through MASTML results and read them in
	root_dir = os.getcwd()
	cv_method = "RepeatedKFold"
	property = "PROPERTY: $/gamma$"

	pred_gfa = collect_mastml_results(root_dir, cv_method, property)

	# Check prediction of GFA against actual GFA. Write 1 if predictions match, 0 else
	# Calc F1 Score
	f1 = f1_score(actual_gfa, pred_gfa)
	fpr, tpr, thresholds = roc_curve(actual_gfa, pred_gfa)
	roc_auc = auc(fpr, tpr)

	# Plot ROC
	plt.plot(fpr, tpr, label=r'Mean ROC (AUC = %0.2f)' % (roc_auc), lw=2, alpha=.8)
	plt.xlabel('False Positive Rate')
	plt.ylabel('True Positive Rate')
	plt.title('Receiver operating characteristic example')
	plt.legend(loc="lower right")
	plt.savefig("roc_curve.png")

	# Write all GFA comparison to CSV files with date and time
	# Folder path:
	folder_out = os.path.join(os.getcwd(), "gfa_predictions.csv")
	with open(folder_out, 'w', newline='') as csvfile:
		wr = csv.writer(csvfile)
		wr.writerow(["GFA Predictions"])
		wr.writerow(["F1 Score: " + str(f1)])
		wr.writerow("")
		wr.writerow(["Actual GFA", "Predicted GFA"])
		rows = zip(actual_gfa, pred_gfa)
		for row in rows:
			wr.writerow(row)
	csvfile.close()

def collect_mastml_results(root_dir, cv_method, property):
	'''
	Method to collect results from MASTML and compare predicted
	'''
	# Get to the directory that has all the splits from the CV method
	cv_dir = "StandardScaler/DoNothing/RandomForestRegressor/" + cv_method
	#cv_dir = cv_method
	cv_dir = os.path.join(root_dir, cv_dir)

	predicted_vals = []

	# Loop through every file and collect the "clean_predictions". Add them to a list
	for f in os.listdir(cv_dir):
		if "split_" in f:
			split_folder = os.path.join(cv_dir, f)
			predictions = pd.read_csv(os.path.join(split_folder, "predictions_Logan_Data.csv"))
			property_prediction = predictions['clean_predictions']
			predicted_vals.append(property_prediction)

	# Convert to np array
	predicted_vals = np.array(predicted_vals)

	# Check predicted value of GFA metric and convert to did/did not form glass classification
	gfa_yes_count = 0
	gfa_no_count = 0
	for p in predicted_vals:
		if p >= GAMMA_CUTOFF_MIN and p <= GAMMA_CUTOFF_MAX:
			pred_gfa.append(1)
			gfa_yes_count+=1
		else:
			pred_gfa.append(0)
			gfa_no_count+=1

	# Calculate probability the material would form a glass given the metric (count
	# number predicted true/total number)
	prob_gfa = gfa_yes_count/(gfa_yes_count + gfa_no_count)

	# Convert GFA categorical prediction array to np array and dump data to CSV
	all_pred_gfa = np.array(pred_gfa)
	np.savetxt("all_predictions.csv", all_pred_gfa, delimiter=",")
	# return the average of the predictions
	return prob_gfa


# Run the script:
if __name__ == '__main__':
    main()
