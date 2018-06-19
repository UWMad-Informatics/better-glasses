from citrination_client import CitrinationClient
from os import environ
import pandas as pd
import csv
import json
from pypif import pif
from pypif.obj import *
import time
import itertools
import numpy as np
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait

def main():
	start_time = time.time()
	# Create instance of the client
	client = CitrinationClient(environ["CITRINATION_API_KEY"], 'https://citrination.com')
	# dataset_id is the id of the dataset you want to upload new data to
	dataset_id = 161880
	# dataview_id is the DataView you want to update after file upload 
	dataview_id = 4743
	# url is the url of the dataview we'd like to click save on.
	url = 'https://citrination.com/data_views/' + str(dataview_id) + '/ml_config'
	# Read in new data. For test we are using just chemical formula, DFT energy, and only predicting Tg
	filename = "predict_data.csv"
	
	# Read in csv file using pandas to make df
	new_data = pd.read_csv(filename)
	# Pull out the desired properties
	form = new_data['formula']
	energy = new_data['PROPERTY: Nearest DFT Formation Energy (eV)']
	tg = new_data['PROPERTY: Tg (K)']
	
	# Use itertools to create combinations of the data set to leave out/use for training
	# Make a list of the indexes of the dataset
	train_indices = []
	for i in range(0, len(form)):
		train_indices.append(i)
	
	# Generate all combos of the indices of the extra data to use for training/testing
	combos = []
	for i in range(0, len(train_indices)-1):
		els = [list(x) for x in itertools.combinations(train_indices, i)]
		combos.extend(els)
		
	# Loop through each combo of the indices for training
	for c in combos:
		# Make copies of the lists of all indices so we can remove the training indices
		pred_form = form[:].tolist()
		pred_energy = energy[:].tolist()
		pred_tg = tg[:].tolist()
		for i in reversed(c):
			del pred_form[i]
			del pred_energy[i]
			del pred_tg[i]

		# for each index in the combination of training indices
		input = []
		if len(c) != 0:
			for i in c:
				# Convert to pif and store pif in JSON
				input.append([form[i], energy[i], tg[i]])
			# Write to CSV and pass the csv file path to make_pif
			with open("training_data.csv", 'w', newline='') as training_csv:
				writer = csv.writer(training_csv)
				writer.writerow(['formula', 'PROPERTY: Nearest DFT Formation Energy (eV)', 'PROPERTY: Tg (K)'])
				for i in range(0, len(input)):
					writer.writerow(input[i])
			training_csv.close()
			pif_output = make_pif("training_data.csv")
			# Upload data. Params are (dataset id, file path (local))
			client.data.upload(dataset_id, pif_output)
		else:
			pass
			
		# Click the save button in the ML config page
		click_save(url)
		
		# Wait for model to retrain
		# Make predictions and store them to a CSV
		# Write to CSV and pass the csv file path to make_pif
		predict_data_file = "testing_data.csv"
		with open(predict_data_file, 'w', newline='') as testing_csv:
			writer = csv.writer(testing_csv)
			writer.writerow(['formula', 'PROPERTY: Nearest DFT Formation Energy (eV)'])
			for i in range(0, len(pred_form)):
				writer.writerow([pred_form[i], pred_energy[i]])
		testing_csv.close()
		if len(pred_form) != 0:
			make_predictions(client, predict_data_file, str(dataview_id))
		# We don't need to delete the data file from the dataset if every file we're uploading has the same name.		
	print("Run time: " + str(time.time() - start_time))

def click_save(my_url):
	"""
	Method to click the save button in Data Views. Set up to login in using a UW email.
	
	:param my_url: URL of the DataView you'd like to click the save button for
	:type my_url: string
	"""
	driver = webdriver.Chrome('C:\Program Files\chromedriver')
	driver.get(my_url)
	# Select access type. This is open access xpath.
	open_access = driver.find_element_by_xpath('/html/body/div[2]/div[3]/div/div[2]/div/div[2]/span[1]').click()
	
	# Sign in with Google
	# Email
	google = driver.find_element_by_xpath('/html/body/div[2]/div[3]/div/div[2]/div[1]/a').click()
	email = driver.find_element_by_xpath('//*[@id="identifierId"]').send_keys('email')
	driver.find_element_by_xpath('//*[@id="identifierNext"]/content/span').click()
	# Password on MyUW login
	driver.implicitly_wait(10)
	password = driver.find_element_by_xpath('//*[@id="j_username"]').send_keys("username")
	password = driver.find_element_by_xpath('//*[@id="j_password"]').send_keys("password")
	driver.find_element_by_xpath('//*[@id="loginForm"]/div[3]/div/button').click()
	
	# Click the save button to trigger model retrain in data views
	driver.implicitly_wait(10)
	button = driver.find_element_by_xpath("/html/body/div/div[3]/div[2]/div[1]/div/div[3]/div/button").click()
	
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
	form = new_data['formula']
	energy = new_data['PROPERTY: Nearest DFT Formation Energy (eV)']
	tg = new_data['PROPERTY: Tg (K)']
	
	input = []
	
	# Make pifs
	for i in range(0, len(form)):
		chemical_system = ChemicalSystem()
		chemical_system.chemical_formula = form[i]
		dft_energy = Property(name = 'Nearest DFT Formation Energy', units = 'eV', scalars = float(energy[i]))
		tg_prop = Property(name = 'Tg', units = 'K', scalars = float(tg[i]))
		chemical_system.properties = [dft_energy, tg_prop]
		input.append(chemical_system)
	
	# Dictionary to PIF
	# Write the string that was dumped to a json
	outfile = "pif.json"
	with open(outfile, 'w') as fp:
		pif.dump(input, fp)
		
	return outfile

	
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
	# Set up client
	client = CitrinationClient(environ["CITRINATION_API_KEY"], 'https://citrination.com')
	
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
	predictions = client.predict(dataview_id, input)
	
	# Write all these predictions to json files with date and time to differentiate predictions.
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
		writer.writerow("")
	
# Run the script:
if __name__ == '__main__':
    main()

