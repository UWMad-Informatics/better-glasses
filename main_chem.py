from mdf_forge.forge import Forge
from matminer.featurizers import composition as cf
from matminer.utils.conversions import str_to_composition
from matplotlib import pyplot as plt
import numpy as np
import pandas as pd
import csv
import os
import itertools
from pymatgen import Composition
from pymatgen.core.periodic_table import Element

# Read in dataset
filepath = "formulas.csv"
glass_data = pd.read_csv(filepath)
glass_data = glass_data['FORMULA']
# Make the compositions of the glasses data into pymatgen objects to match the data from OQMD
# Convert data into pandas dataframe
#glass_data = pd.DataFrame(data = glass_data, columns=['FORMULA'])
# Convert compositions to pymatgen objects.
comps = str_to_composition(glass_data)

# Loop through all elements and list the ones that come up.
# Also keep track fo how many elements there are of each.
majority = []
for c in comps:
	max_comp = -1
	main_element = ""
	for element, amount in c.items():
		if amount > max_comp:
			max_comp = amount
			main_element = element
	majority.append(str(main_element))		
			
with open('main_element.csv', 'w', newline='') as csv_file:
    writer = csv.writer(csv_file)
    for row in majority:
       writer.writerow([row])