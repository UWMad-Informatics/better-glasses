from mdf_forge.forge import Forge
from matminer.featurizers import composition as cf
from matminer.featurizers.conversions import StrToComposition
import numpy as np
import pandas as pd
import csv
import os
import itertools
from pymatgen import Composition
from pymatgen.core.periodic_table import Element

# Read in dataset
filepath = "pifs.csv"
glass_data = pd.read_csv(filepath)
# Make the compositions of the glasses data into pymatgen objects to match the data from OQMD
# Convert compositions to pymatgen objects.
comps = StrToComposition().featurize_dataframe(glass_data, "formula", ignore_errors=True)["composition"]

# Loop through all elements and list the ones that come up.
# Also keep track fo how many elements there are of each.
majority = []
for c in comps:
	print(c)
	max_comp = -1
	main_element = ""
	elements = c.items()
	for e in elements:
		if e[1] > max_comp:
			max_comp = e[1]
			main_element = e[0]
	majority.append(str(main_element))

with open('main_element.csv', 'w', newline='') as csv_file:
    writer = csv.writer(csv_file)
    for row in majority:
       writer.writerow([row])
