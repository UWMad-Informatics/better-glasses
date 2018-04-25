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
	client = CitrinationClient(os.environ["CITRINATION_API_KEY"], 'https://citrination.com')
	
	# Read in experimental data
	filename = "C:/Users/mvane/Documents/Skunkworks/BMG/Data/BMG_full_dataset_with_energies.csv"
	exp_data = pd.read_csv(filename)
	formula = exp_data['formula'].as_matrix()
	energy = exp_data['PROPERTY: Nearest DFT Formation Energy (eV)'].as_matrix()
	form = "formula"
	property = "Property Nearest DFT Formation Energy"
	# Convert formulas to dictionary one at a time and make predictions. Export each to their own json.	
	for i in range(0, len(formula)):
		input = {form: formula[i], property: energy[i]}
		# Make predictions of Tg, Tx, and Tl. (These will also contain many of the Magpie descriptors used to train the model)
		model_num = "4416"
		predictions = client.predict(model_num, input)
	
		# Write all these predictions to json files
		# Folder path:
		folder_out = "C:/Users/mvane/Documents/GitHub/better-glasses/predictions_output/"
		with open(folder_out + str(formula[i]) + ".txt", 'w') as outfile:
			json.dump(predictions, outfile)
		outfile.close()	
		
# Run the script:
if __name__ == '__main__':
    main()