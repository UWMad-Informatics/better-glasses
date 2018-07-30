import os
import sys
import requests
import datetime
import pandas as pd
import numpy as np
from numpy import trapz
import csv
import matplotlib.pyplot as plt
from scipy.stats import norm
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
	
	tg_act = exp_data['PROPERTY: Tg (K)']
	tl_act = exp_data['PROPERTY: Tl (K)']
	tx_act = exp_data['PROPERTY: Tx (K)']
	# trg_act = exp_data['PROPERTY: Trg']
	# gamma_act = exp_data['PROPERTY: $\\gamma$']
	# omega_act = exp_data['PROPERTY: $\\omega$']
	
	tg_loss = predicted_vals['Property Tg Uncertainty'].tolist()
	tl_loss = predicted_vals['Property Tl Uncertainty'].tolist()
	tx_loss = predicted_vals['Property Tx Uncertainty'].tolist()
	trg_loss = predicted_vals['Property Trg Uncertainty'].tolist()
	gamma_loss = predicted_vals['Property $\\gamma$ Uncertainty'].tolist()
	omega_loss = predicted_vals['Property $\\omega$ Uncertainty'].tolist()
	
	tg_act_err = []
	tl_act_err = []
	tx_act_err = []
	tg_err_bar = []
	tl_err_bar = []
	tx_err_bar = []
	trg_err_bar = []
	gamma_err_bar = []
	omega_err_bar = []
	trg_act_err = []
	gamma_act_err = []
	omega_act_err = []
	trg_act_err = []
	gamma_act_err = []
	omega_act_err = []
	
	# GFA Metrics
	trg_calc = tg_pred/tl_pred
	gamma_calc = tx_pred/(tg_pred + tl_pred)
	omega_calc = (tg_pred/tx_pred) - ((2*tg_pred)/(tg_pred + tl_pred))
	
	trg_act = tg_act/tl_act
	gamma_act = tx_act/(tg_act + tl_act)
	omega_act = (tg_act/tx_act) - 2*(tg_act/(tg_act + tl_act))
	
	for i in reversed(range(0, len(formulas))):
		if not np.isnan(tg_act[i]) and not np.isnan(tl_act[i]) and not np.isnan(tx_act[i]):
			tg_err = abs(tg_pred[i] - tg_act[i])
			tg_act_err.append(tg_err)
			tg_err_bar.append(abs(tg_err - tg_loss[i]))
			
			tl_err = abs(tl_pred[i] - tl_act[i])
			tl_act_err.append(tl_err)
			tl_err_bar.append(abs(tl_err - tl_loss[i]))
		
			tx_err = abs(tx_pred[i] - tx_act[i])
			tx_act_err.append(tx_err)
			tx_err_bar.append(abs(tx_err - tx_loss[i]))
			
			trg_err = abs(trg_calc[i] - trg_act[i])
			trg_act_err.append(trg_err)
			trg_err_bar.append(abs(trg_err - trg_loss[i]))
			
			gamma_err = abs(gamma_calc[i] - gamma_act[i])
			gamma_act_err.append(gamma_err)
			gamma_err_bar.append(abs(gamma_err - gamma_loss[i]))
			
			omega_err = abs(omega_calc[i] - omega_act[i])
			omega_act_err.append(omega_err)
			omega_err_bar.append(abs(omega_err - omega_loss[i]))
	
	# Plotting Gaussian vs. standard deviations	
	metric = trg_err_bar
	mu = np.mean(metric)
	sigma = np.std(metric)
	n_bins = 100

	fig, ax = plt.subplots(figsize=(8, 4))

	# plot the cumulative histogram
	n, bins, patches = ax.hist(metric, n_bins, [min(metric), max(metric)], density=True, histtype='step', 
								cumulative=True, label='$\gamma$ Error', linewidth=3)

	# Add a line showing the expected distribution.
	y = norm.pdf(bins, mu, sigma).cumsum()
	y /= y[-1]
	ax.plot(bins, y, 'k--', linewidth=3, label='Gaussian')

	# tidy up the figure
	ax.grid(True)
	ax.legend(loc='right',fontsize=20)
	ax.set_title('Cumulative step histograms', fontsize=24)
	ax.set_xlabel('$\gamma$ Error (K)', fontsize=22)
	ax.set_ylabel('Likelihood of occurrence',fontsize=22)
	plt.tick_params(axis='both', labelsize=16)
	plt.tight_layout()
	plt.show()
	
	area_under_gaussian = trapz(y)
	area_under_err_curve = trapz(n)
	print(abs(area_under_gaussian - area_under_err_curve))
	
# Run the script:
if __name__ == '__main__':
	main()