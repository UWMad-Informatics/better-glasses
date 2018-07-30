# This file is a method that takes in a csv with formula and formation energy for some BMG's
# and make predictions on a given data view on citrination.
# Predictions are written to a csv called predictions_output.csv
import os
import sys
import datetime
import csv
import requests
import pandas as pd
from citrination_client import CitrinationClient

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
	# Convert formulas & energies to dictionary. Make a list of dictionaries.
	input = []
	for i in range(0, len(formula)):
		input.append({form: formula[i], property: energy[i]})
	
	# Make predictions of Tg, Tx, and Tl. (These will also contain many of the Magpie descriptors used to train the model)
	model_num = "4416"
	predictions = client.predict(model_num, input)
	
	# Write all these predictions to json files with date and time to differentiate predictions.
	# Folder path:
	folder_out = "C:/Users/mvane/Documents/GitHub/better-glasses/predictions_output.csv"
	first = True
	# Make CSV writer. 
	with open(folder_out, 'w', newline='') as csvfile:
		writer = csv.writer(csvfile)
		# Go through every prediction that we made from the chemical formula
		for p in predictions:
			keys = p.all_keys()
			# Make a header row with all of the keys listed
			if first:
				row = []
				row.append('Formula')
				for k in keys:
					row.append(k)
					row.append(str(k) + ' Uncertainty')
				writer.writerow(row)
				first = False
			row = []
			# Write the formula in the first column of the CSV. Formula will also show up in a later column.
			row.append(p.get_value('formula').value)
			# Write the value and uncertainty of each key to the CSV
			for k in keys:
				val = p.get_value(k).value
				loss = p.get_value(k).loss
				row.append(str(val))
				row.append(str(loss))
			writer.writerow(row)

	csvfile.close()
		
		
# Run the script:
if __name__ == '__main__':
    main()