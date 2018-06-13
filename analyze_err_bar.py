import os
import sys
import json
import requests
import datetime
import pandas as pd
import numpy as np
import csv
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
import math
from citrination_client.client import CitrinationClient
from citrination_client.util.quote_finder import quote

def main():
	# Set up client
	client = CitrinationClient(os.environ["CITRINATION_API_KEY"], 'https://citrination.com')
	
	# Read in experimental data. Values to be predicted should be in list form.
	filename = "C:/Users/mvane/Documents/Skunkworks/BMG/Data/BMG_full_dataset_with_energies.csv"
	exp_data = pd.read_csv(filename)
	formula = exp_data['formula'].values.tolist()
	energy = exp_data['PROPERTY: Nearest DFT Formation Energy (eV)'].tolist()
	
	# Create a list of dictionaries containing the key-value pairs corresponding to what you need to run your model.
	# This example has model inputs of chemical formula and DFT formation energy, so each entry of this list will 
	# contain a dictionary of {"formula":chemical formula & "Energy":value}
	form = "formula"
	property = "Property Nearest DFT Formation Energy"
	input = []
	for i in range(0, len(formula)):
		input.append({form: formula[i], property: energy[i]})
	
	# # Make predictions of Tg, Tx, and Tl. (These will also contain many of the Magpie descriptors used to train the model)
	# model_num = "4416"
	# predictions = client.models.predict(model_num, input)
	
	# # Make a CSV to write predictions to. We'll save formula, Tg, Tl, Tx, and their uncertainties (loss)
	# # CSV arg newline = '' prevents CSV from saving with lines between each row.
	outfile = "C:/Users/mvane/Documents/Skunkworks/BMG/Data/retrieved_predictions.csv"
	# with open(outfile, 'w', newline='') as csvfile:
		# writer = csv.writer(csvfile)
		# # Headers just for remembering which column is which.
		# headers = ['FORMULA', 'Tg (K)', 'Tg Err', 'Tl (K)', 'Tl Err', 'Tx (K)', 'Tx Err']
		# writer.writerow(headers)
		# for p in predictions:
			# f = p.get_value('formula').value
			# tg = p.get_value('Property Tg').value
			# tg_loss = p.get_value('Property Tg').loss
			# tl = p.get_value('Property Tl').value
			# tl_loss = p.get_value('Property Tl').loss
			# tx = p.get_value('Property Tx').value
			# tx_loss = p.get_value('Property Tx').loss
			# row = []
			# for i in [f, tg, tg_loss, tl, tl_loss, tx, tx_loss]:
				# row.append(str(i))
			# writer.writerow(row)
	# csvfile.close()
	
	# Analyze the outputs
	# Read in the predicted values from the CSV just created
	predicted_vals = pd.read_csv(outfile)
	tg_pred = predicted_vals['Tg (K)']
	tl_pred = predicted_vals['Tl (K)']
	tx_pred = predicted_vals['Tx (K)']
	tg_act = exp_data['PROPERTY: Tg (K)'].tolist()
	tl_act = exp_data['PROPERTY: Tl (K)'].tolist()
	tx_act = exp_data['PROPERTY: Tx (K)'].tolist()
	trg_act = exp_data['PROPERTY: Trg']
	gamma_act = exp_data['PROPERTY: $\\gamma$']
	omega_act = exp_data['PROPERTY: $\\omega$']
	tg_loss = predicted_vals['Tg Err'].tolist()
	tl_loss = predicted_vals['Tl Err'].tolist()
	tx_loss = predicted_vals['Tx Err'].tolist()
	
	tg_act_err = []
	tl_act_err = []
	tx_act_err = []
	tg_err_bar = []
	tl_err_bar = []
	tx_err_bar = []
	
	# GFA Metrics
	trg_calc = tg_pred/tl_pred
	gamma_calc = tx_pred/(tg_pred + tl_pred)
	omega_calc = (tg_pred/tx_pred) - 2*(tg_pred/(tg_pred + tl_pred))
	
	for i in range(0, len(formula)):
		tg_err = abs(tg_pred[i] - tg_act[i])
		tg_act_err.append(tg_err)
		tg_err_bar.append(abs(tg_err - tg_loss[i]))
		
		tl_err = abs(tl_pred[i] - tl_act[i])
		tl_act_err.append(tl_err)
		tl_err_bar.append(abs(tl_err - tl_loss[i]))
	
		tx_err = abs(tx_pred[i] - tx_act[i])
		tx_act_err.append(tx_err)
		tx_err_bar.append(abs(tx_err - tx_loss[i]))
	
	# Plotting Gaussian vs. standard deviations	
	mu = np.mean(tg_loss)
	sigma = np.std(tg_loss)
	n_bins = 100
	x = tg_loss
	ra = [min(tg_loss), max(tg_loss)]

	fig, ax = plt.subplots(figsize=(8, 4))

	# plot the cumulative histogram
	n, bins, patches = ax.hist(tg_loss, n_bins, [min(tg_loss), max(tg_loss)], normed=1, histtype='step', 
								cumulative=True, label='Tg Error', linewidth=3)

	# Add a line showing the expected distribution.
	y = mlab.normpdf(bins, mu, sigma).cumsum()
	y /= y[-1]
	ax.plot(bins, y, 'k--', linewidth=3, label='Gaussian')

	# tidy up the figure
	ax.grid(True)
	ax.legend(loc='right',fontsize=20)
	ax.set_title('Cumulative step histograms', fontsize=24)
	ax.set_xlabel('Tg Error (K)', fontsize=22)
	ax.set_ylabel('Likelihood of occurrence',fontsize=22)
	plt.tick_params(axis='both', labelsize=16)
	plt.tight_layout()
	plt.show()

	
# Run the script:
if __name__ == '__main__':
	main()