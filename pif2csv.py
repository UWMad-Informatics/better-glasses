from pypif import pif
from pypif.obj import *
import csv
import json

# Open the json file that contains the pifs
json_file = open("pifs.json")

# Load json with pif
pifs = pif.load(json_file)
# Find all the CSV headers
headers = []
for p in pifs:
    props = p.properties
    names = []
    for i in props:
        names.append(i.name)
    if len(names) > len(headers):
        headers = names

# Possible attributes associated with a pif:
pif_common_objs = []
header = []

# CSV outfile
csv_out = "pifs.csv"
with open(csv_out, 'w', newline='') as outfile:
    csvwriter = csv.writer(outfile)
    csvwriter.writerow(headers)

    # Loop through each pif
    for p in pifs:
        # Make a list of a row to write each time
        row = []
        # Add chemical_formula
        row.append(p.chemical_formula)
        #Add all the value of the properties
        props = p.properties
        for j in props:
            row.append(j.scalars)
        csvwriter.writerow(row)

outfile.close()
