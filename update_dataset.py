from citrination_client import CitrinationClient
from os import environ
import pandas as pd
import csv
import json
from pypif import pif
from pypif.obj import *
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

def main():
	# Create instance of the client
	client = CitrinationClient(environ["CITRINATION_API_KEY"], 'https://citrination.com')
	# dataset_id is the id of the dataset you want to upload new data to
	dataset_id = 161880
	# dataview_id is the DataView you want to update after file upload 
	dataview_id = 4743
	
	# Read in new data. For test we are using just chemical formula, DFT energy, and only predicting Tg
	new_files = ["test_10.csv"]
	for file in new_files:
		pif_output = make_pif(file)

		# Upload data. Params are (dataset id, file path (local))
		client.data.upload(dataset_id, 'pif.json')
		
		# Click the save button in the ML config page
		url = 'https://citrination.com/data_views/' + str(dataview_id) + '/ml_config'
		click_save(url)


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
	# Password
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
	
	:param: filename: Path to the CSV file you'd like to convert to PIF.
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

	# Convert CSV to use with PYPIF to go csv -> PIF
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
	# with open('pifs.txt', 'w') as outfile:
		# json.dump(input, outfile)
	outfile = filename + "pif.json"
	with open(outfile, 'w') as fp:
		pif.dump(input, fp)
		
	return outfile

	
# Run the script:
if __name__ == '__main__':
    main()

