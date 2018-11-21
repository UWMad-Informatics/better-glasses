import os
import numpy as np
import math
import pandas as pd
import csv
import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt
from sklearn.metrics import mean_squared_error

folders = ['Trg_Predict_Logan_withFeatureGen', 'Tg_with_FeatureGen', 'Tl_with_FeatureGen', 'Tx_with_FeatureGen']
properties = ['PROPERTY: Trg', 'PROPERTY: Tg (K)','PROPERTY: Tl (K)', 'PROPERTY: Tx (K)']
labels = ['Trg']#, 'Tg', 'Tl', 'Tx']
prop_counter = 0

# Make some plots
plt.rc('font', size=20)
plt.rc('axes', titlesize=20)
plt.rc('axes', labelsize=20)
plt.rc('xtick', labelsize=20)
plt.rc('ytick', labelsize=20)
plt.rc('figure', titlesize=20)
plt.figure()

for f in folders:
	root_dir = os.path.join(os.getcwd(), f)
	path_to_cv = os.path.join(root_dir, 'StandardScaler/DoNothing/RandomForestRegressor')
	logocv_data = {}
	kfoldcv_data = {}

	ndme = []
	training_size = []

	# For each cv folder in the results directory
	for cv_folder in os.listdir(path_to_cv):
		if "LeaveOneGroupOut" in cv_folder:
			cv_folder = os.path.join(path_to_cv, cv_folder)
			for split in os.listdir(cv_folder):
				# Add formula and prediction to a list
					test_csv = pd.read_csv(os.path.join(cv_folder, "split_0/test.csv"))
					formula = test_csv['formula']
					prediction = test_csv['test_pred']
					actual = test_csv[properties[prop_counter]]
					train_csv = pd.read_csv(os.path.join(cv_folder, "split_0/train.csv"))
					training_size.append(len(train_csv['formula']))
					std = np.std(train_csv[properties[prop_counter]])
					ndme.append(math.sqrt(mean_squared_error(actual, prediction))/std)

					# Add the collected formula and prediction from the current folder in the loop to the all_data dict
					for i in range(0, len(formula)):
						if formula[i] not in logocv_data:
							logocv_data[formula[i]] = [prediction[i], actual[i]]
						else:
							# Average the prediction, keep the actual value the same
							logocv_data[formula[i]][0] = np.mean([logocv_data[formula[i]][0], prediction[i]])

		elif "RepeatedKFold" in cv_folder:
			cv_folder = os.path.join(path_to_cv, cv_folder)
			for split in os.listdir(cv_folder):
				# Add formula and prediction to a list
				if "split_" in split:
					test_csv = pd.read_csv(os.path.join(os.path.join(cv_folder, split), "test.csv"))
					formula = test_csv['formula']
					prediction = test_csv['test_pred']
					actual = test_csv[properties[prop_counter]]
					train_csv = pd.read_csv(os.path.join(os.path.join(cv_folder, split), "train.csv"))
					if len(train_csv['formula']) > 100:
						training_size.append(len(train_csv['formula']))
						std = np.std(train_csv[properties[prop_counter]])
						ndme.append(math.sqrt(mean_squared_error(actual, prediction))/std)

					# Add the collected formula and prediction from the current folder in the loop to the all_data dict
					for i in range(0, len(formula)):
						if formula[i] not in kfoldcv_data:
							kfoldcv_data[formula[i]] = [prediction[i], actual[i]]
						else:
							# Average the prediction, keep the actual value the same
							kfoldcv_data[formula[i]][0] = np.mean([kfoldcv_data[formula[i]][0], prediction[i]])

	predicted = []
	actual = []
	for key in kfoldcv_data.keys():
		predicted.append(kfoldcv_data[key][0])
		actual.append(kfoldcv_data[key][1])
	plt.scatter(actual, predicted, c='r', marker = '^', edgecolor = 'k', label = "3 Fold CV")
	plt.plot(actual, actual, 'k--')

	predicted = []
	actual = []
	for key in logocv_data.keys():
		predicted.append(logocv_data[key][0])
		actual.append(logocv_data[key][1])
	plt.scatter(actual, predicted, c='b', marker = 'o', edgecolor = 'k', label = "LOChemO CV")
	plt.legend(loc=2, prop={'size': 14})
	plt.xlabel("Actual " + str(labels[prop_counter]) + " Value")
	plt.ylabel("Predicted " + str(labels[prop_counter]) + " Value")
	plt.tight_layout()
	plt.savefig(str(labels[prop_counter]) + "_Parity.png")
	plt.clf()

	plt.scatter(ndme, training_size, marker = 'o', edgecolor = 'k', label = labels[prop_counter])
	plt.xlabel("# Points Used for Training")
	plt.ylabel("RMSE/$\sigma$")
	plt.tight_layout()
	plt.savefig(str(labels[prop_counter]) + "_NDME.png")
	plt.clf()

	prop_counter += 1
