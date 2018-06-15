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
	# Read in new data. For test we are using just chemical formula, DFT energy, and only predicting Tg
	new_data = pd.read_csv("test_10.csv")
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
	filename = "pif.json"
	with open(filename, 'w') as fp:
		pif.dump(input, fp)

	# Upload new data
	# Do I need to upload, update, create new version...? Does uploading a csv work?
	# Create instance of the client
	client = CitrinationClient(environ["CITRINATION_API_KEY"], 'https://citrination.com')

	# # Upload data. Params are (dataset id, file path (local))
	dataset_id = 161880
	# dataview_id = 4743
	client.data.upload(dataset_id, 'pif.json')
	
	# Click the save button in the ML config page
	url = 'https://citrination.com/data_views/4743/ml_config'
	click_save(url)

		
# Save button clicker
def click_save(my_url):
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
	
# Run the script:
if __name__ == '__main__':
    main()

