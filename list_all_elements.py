from mdf_forge.forge import Forge
from matminer.featurizers import composition as cf
from matminer.utils.conversions import str_to_composition
from matplotlib import pyplot as plt
import numpy as np
import pandas as pd
import csv
import itertools
from pymatgen import Composition
from pymatgen.core.periodic_table import Element

# Read in dataset
filepath = "C:\\Users\\mvane\\Documents\\GitHub\\better-glasses\\formulas.csv"
glass_data = pd.read_csv(filepath)
glass_data = glass_data['FORMULA']
# Make the compositions of the glasses data into pymatgen objects to match the data from OQMD
# Convert data into pandas dataframe
glass_data = pd.DataFrame(data = glass_data, columns=['FORMULA'])
# Convert compositions to pymatgen objects.
comps = str_to_composition(glass_data["FORMULA"])

# Loop through all elements and list the ones that come up.
# Also keep track fo how many elements there are of each.
count = {}
for c in comps:
	for key, value in c.items():
		if key in count:
			count[key] += 1
		else:
			count[key] = 1
			
with open('element_analysis.csv', 'w', newline='') as csv_file:
    writer = csv.writer(csv_file)
    for key, value in count.items():
       writer.writerow([key, value])		