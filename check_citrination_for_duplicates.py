# import statements
import os
import sys
import json
import pandas
import requests
from citrination_client.client import CitrinationClient
from citrination_client.util.quote_finder import quote

# You have a citrination API key that can be found under account settings on Citrination. I made it an environment variable.
api_key = os.environ['CITRINATION_API_KEY']
client = CitrinationClient(api_key)
# Make the URL to go to
api_url = 'https://citrination.com/api'
headers = {'X-API-Key': quote(api_key), 'Content-Type': 'application/json'}
# Create an array to hold the results of what we've found
my_pif_results = []

# Change path for csv locally (I'll upload the CSV used here).
my_csv = pandas.read_csv("C:\\Users\\mvane\\Documents\\Citrine\\Data\\Better Glasses\\Trimmed Data\\Formulas exported from Citrination.csv")
# Get the formulas from the CSV
formula = my_csv["formula"]

for chem in formula:
	# Search the pifs on Citrination for a data set (will need to change dataset number to be relevant for 
	# The dataset you want it to work on)
	pif_result = client.simple_chemical_search(chemical_formula=chem, include_datasets = 153278)
	my_pif_results.append(pif_result.total_num_hits)
	
# Prints the results when checking for duplicates, can be removed
for i in range(0, len(my_pif_results)):
	if my_pif_results[i] != 1:
		print(formula[i]+ " " + str(my_pif_results[i]))
