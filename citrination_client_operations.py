# This file contains methods to perform basic operation on Citrination using the Python client.
# I'm assuming you've set your Citrination API key (which can be found in your profile) as an
# environment variable called CITRINATION_API_KEY.
# This isn't entirely ready to run on its own. You'll need to update the paths to the files 
# you'd like and use pandas to pull out the values of the csv you're reading, but that should
# be fairly copy and paste.
# Packages that should be installed are below in the imports

from citrination_client import CitrinationClient
from os import environ
import pandas as pd
import csv
import json
from pypif import pif
from pypif.obj import *
import numpy as np

def main():
	# Create an instance of the client
	client = CitrinationClient(os.environ["CITRINATION_API_KEY"], 'https://citrination.com')
	
	# Name of the file storing the data you would like to upload or predict:
	filename = "filename"
	# Number of the Dataset you would like to upload to (found in URL):
	dataset_id = 0000
	# Number of the DataView you would like to upload to (found in URL):
	dataview_id = 0000
	
	
	# Upload data
	upload(client, filename, dataset_id)	
	
	# Retrieve predictions
	predict(client, filename, dataview_id)
	

def upload(client, filename, dataset_id):
	"""
	Method to upload data to a given Dataset in Citrination
	:param client: An instance of the CitrinationClient
	:type client: CitrinationClient
	:param filename: CSV file of the data we'd like to predict
	:type filename: str
	:param dataset_id: ID of the Dataset to make predictions in
	:type dataset_id: str
	"""
	# Turn the csv file (with headers) to pif and store on your computer.
	pif_output = make_pif(fileaname)
	
	# Upload data to Citrination
	client.data.upload(dataset_id, pif_output)

	
	
def make_predictions(client, filename, dataview_id):
	"""
	Method to generate predictions in a DataView and store the results to a csv
	:param client: An instance of the CitrinationClient
	:type client: CitrinationClient
	:param filename: CSV file of the data we'd like to predict
	:type filename: str
	:param dataview_id: ID of the DataView to make predictions in
	:type dataview_id: str
	"""
	# read in csv and convert to pandas df
	# input should be whatever property you used as input to your model (if any). This does not include
	# the automatically generated inputs Citrination will create.
	# For example, if you were predicting glass transition temperature for alloys using the formula (required) and
	# DFT formation energy as input, this would be what your input would look like.
	exp_data = pd.read_csv(filename)
	formula = exp_data['formula'].as_matrix()
	energy = exp_data['PROPERTY: Nearest DFT Formation Energy (eV)'].as_matrix()
	
	# Define the keys for the dictionary used to predict
	# If you have more than one input, you will need to make adjustments here and add the
	# name of your input as a string and use that string as a dictionary key
	form = "formula"
	property = "Property Nearest DFT Formation Energy"
	
	# Convert formulas & input (energy, in this example) to dictionary. Make a list of dictionaries.
	input = []
	for i in range(0, len(formula)):
		input.append({form: formula[i], property: energy[i]})
	
	# Make predictions. These will also contain many of the Magpie descriptors used to train the model.
	predictions = client.predict(dataview_id, input)
	
	# Write all these predictions to json files with date and time to differentiate predictions.
	# Note: not the most efficient, but it works.
	# Folder path:
	folder_out = time.strftime("%H%M").replace(":","") + "_predictions_output.csv"
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


def make_pif(filename):
	"""
	Method to turn a CSV file to PIF for this BMG-based dataset. Can edit it to pull out whatever properties needed.
	
	:param filename: Path to the CSV file you'd like to convert to PIF.
	:type filename: str
	:return: Path to the JSON output from converting to PIF
	:rtype: str
	"""
	# Read in csv file using pandas to make df
	new_data = pd.read_csv(filename)
	
	# Pull out the desired properties and turn them to lists.
	# Edit this to include each of the properties you would like to upload for 
	# small numbers of columns in your csv or use the commented out block of code below to get all properties you
	# would like to upload for a larger number of files. Requires some lists to be made for storing the values associated
	# with said properties that's not written here.
	form = new_data['formula']
	energy = new_data['PROPERTY: Nearest DFT Formation Energy (eV)']
	tg = new_data['PROPERTY: Tg (K)']
	
	# headers = []
	# with open(filename, "rb") as f:
    # reader = csv.reader(f, delimiter=",")
    # for i in enumerate(reader):
        # headers.append(i)
	# headers = headers[0]
	
	input = []
	
	# Make pifs
	for i in range(0, len(form)):
		# Create a new chemical system (from the pypif package)
		chemical_system = ChemicalSystem()
		# Set the formula
		chemical_system.chemical_formula = form[i]
		# Create some properties to add
		# If you have conditions, the format is slightly different and the appropriate info can 
		# be found the on the Citrination knowledgebase
		dft_energy = Property(name = 'Nearest DFT Formation Energy', units = 'eV', scalars = float(energy[i]))
		tg_prop = Property(name = 'Tg', units = 'K', scalars = float(tg[i]))
		# add the properties to the chemical system
		chemical_system.properties = [dft_energy, tg_prop]
		# add the system to the list
		input.append(chemical_system)
	
	# Dictionary to PIF
	# Write the string that was dumped to a json using pif.dump from pypif
	outfile = "pif.json"
	with open(outfile, 'w') as fp:
		pif.dump(input, fp)
		
	# Return the name of the file you wrote the pif to
	return outfile


# Run the script:
if __name__ == '__main__':
    main()