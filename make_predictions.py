import os
import sys
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
		
	# Make predictions of Tg, Tx, and Tl. These will also contain many of the Magpie descriptors used to train the model
	model_num = "4291"
	predictions = client.predict(model_num, inputs)
	
	# Write all these predictions to json file
	with open('predictions_' + str(model_num) + ".txt", 'w') as outfile:
		json.dump(predictions, outfile)

		
# Run the script:
if __name__ == '__main__':
    main()