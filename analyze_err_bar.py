import os
import sys
import requests
import datetime
import pandas as pd
import numpy as np
import csv
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
import math
from citrination_client.client import CitrinationClient

def main():
	# This method assumes you've already made predictions and they're stored in a CSV.
	# Can use make_predictions.py in this repo to make predictions
	# Set up client
	client = CitrinationClient(os.environ["CITRINATION_API_KEY"], 'https://citrination.com')
	
	# Analyze the outputs
	# Read in the predicted values from the CSV just created (pred_file) and the actual values (exp_file)
	# Both files should be sorted alphabetically by formula.
	pred_file = "predictions_output.csv" 
	exp_file = "C:\\Users\\mvane\\Documents\\Skunkworks\\BMG\\Data\\BMG_full_dataset_with_energies - Copy.csv"
	predicted_vals = pd.read_csv(pred_file)
	exp_data = pd.read_csv(exp_file)
	
	formulas = predicted_vals['Formula']
	tg_pred = predicted_vals['Property Tg']
	tl_pred = predicted_vals['Property Tl']
	tx_pred = predicted_vals['Property Tx']
	tg_act = exp_data['PROPERTY: Tg (K)'].tolist()
	tl_act = exp_data['PROPERTY: Tl (K)'].tolist()
	tx_act = exp_data['PROPERTY: Tx (K)'].tolist()
	trg_act = exp_data['PROPERTY: Trg']
	gamma_act = exp_data['PROPERTY: $\\gamma$']
	omega_act = exp_data['PROPERTY: $\\omega$']
	tg_loss = predicted_vals['Property Tg Uncertainty'].tolist()
	tl_loss = predicted_vals['Property Tl Uncertainty'].tolist()
	tx_loss = predicted_vals['Property Tx Uncertainty'].tolist()
	
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
	
	for i in range(0, len(formulas)):
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