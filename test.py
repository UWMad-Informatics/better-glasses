import os
import sys
import csv
import json
import requests
import datetime
import pandas as pd
from citrination_client.client import CitrinationClient
from citrination_client.util.quote_finder import quote

def main():
	# Set up client
	api_key = os.environ['CITRINATION_API_KEY']
	client = CitrinationClient(api_key)
	api_url = 'https://citrination.com/api'
	headers = {'X-API-Key': quote(api_key), 'Content-Type': 'application/json'}

	# Read in experimental data
	filename = "C:/Users/mvane/Documents/Skunkworks/BMG/Data/BMG_full_dataset_with_energies.csv"
	exp_data = pd.read_csv(filename)
	formula = exp_data['formula'].as_matrix()
	energy = exp_data['PROPERTY: Nearest DFT Formation Energy (eV)'].as_matrix()
	form = "formula"
	property = "Nearest DFT Formation Energy (eV)"
	# Convert formulas to dictionary
	inputs = []
	for i in range(0, len(formula)):
		inputs.append({form: formula[i], property: energy[i]})
	print(inputs)
		
	# Make predictions of Tg, Tx, and Tl
	model_num = "4291"
	predictions = client.predict(model_num, inputs)
	
	# Write all predictions to json file
	with open('full_predictions_' + str(model_num) + ".txt", 'w') as outfile:
		json.dump(predictions, outfile)
		
	# Write what we care about to a csv
	formula_p = predictions['candidates'][0]['formula']
	tg_p = predictions['candidates'][0]['Property Tg']
	tl_p = predictions['candidates'][0]['Property Tl']
	tx_p = predictions['candidates'][0]['Property Tx']
	values = zip(formula_p, tg_p, tl_p, tx_p)
	
	with open('predictions_' + str(model_num) + ".csv", 'wb') as csvout:
		wr = csv.writer(csvout)
		for row in values:
			wr.writerow(row)

		
# Run the script:
if __name__ == '__main__':
    main()