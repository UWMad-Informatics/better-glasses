from matminer.featurizers import composition as cf
from matminer.utils.conversions import str_to_composition
import numpy as np
import pandas as pd
import csv
import itertools
from matminer.featurizers import composition as cf
from matminer.utils.conversions import str_to_composition
from pymatgen import Composition
from pymatgen.core.periodic_table import Element

# Read in dataset
filepath = "C:\\Users\\mvane\\Documents\\GitHub\\MAST-ML\\tests\\csv\\rfe_20_logrc.csv"
glass_data = pd.read_csv(filepath)
glass_data = glass_data['formula']
# Convert compositions to pymatgen objects.
comps = str_to_composition(glass_data)

# Loop through all elements and list the ones that come up.
# Also keep track fo how many elements there are of each.
all_elements = []
for c in comps:
	comp_contains = c.as_dict().keys()
	for e in comp_contains:
		if e not in all_elements:
			all_elements.append(e)
		
with open('element_analysis.csv', 'w', newline='') as csv_file:
	writer = csv.writer(csv_file)	
	writer.writerow(all_elements)

	for c in comps:
		comp_contains = c.as_dict().keys()
		contains = []
		for a in all_elements:
			if a in comp_contains:
				contains.append(1)
			else:
				contains.append(0)
		writer.writerow(contains)