from mdf_forge.forge import Forge
from matminer.featurizers import composition as cf
from matminer.utils.conversions import str_to_composition
from matplotlib import pyplot as plt
import numpy as np
import pandas as pd
import itertools
from pymatgen import Composition
from pymatgen.core.periodic_table import Element
from sklearn import metrics
from sklearn.neighbors import NearestNeighbors, KNeighborsRegressor
import time

def main():
	start = time.time()
	
	# Read in dataset
	filepath = "C:\\Users\\mvane\\Documents\\GitHub\\better-glasses\\formulas.csv"
	glass_data = pd.read_csv(filepath)
	glass_data = glass_data['composition']
	# Make the compositions of the glasses data into pymatgen objects to match the data from OQMD
	# Convert data into pandas dataframe
	glass_data = pd.DataFrame(data = glass_data, columns=['composition'])
	# Convert compositions to pymatgen objects.
	glass_data["composition_pmg"] = str_to_composition(glass_data["composition"])

	# Set up forge
	mdf = Forge()

	# Get all converged results from OQMD. Currently have "quick demo" set so searches don't take as long while testing code
	# Note: Advanced args (match field or source) cleared when we call search(), so add reset_query = false to keep matches
	# Note: Use mdf.aggregate() if we need to retrieve > 10000 results from OQMD
	result_records = mdf.aggregate('mdf.source_name:oqmd AND (oqmd.configuration:static OR oqmd.configuration:standard) ' + 
		'AND oqmd.converged:True') #AND mdf.scroll_id:<10000'
	print('Found %d compounds'%len(result_records))

	# Convert results into pandas dataframe and get lowest energy compound at each composition
	oqmd_data = pd.DataFrame([x['mdf']['links']['landing_page'] for x in result_records], columns=['oqmd_url'])

	# Get composition of alloys and enthalpy of formation
	oqmd_data['composition'], oqmd_data['delta_e'], oqmd_data['energy'] = list(zip(*[get_data(x) for x in result_records]))
	
	# Convert compositions to pymatgen objects
	oqmd_data["composition_pmg"] = str_to_composition(oqmd_data["composition"]) 
	
	# Remove results from memory
	#del result_records
	
	# Remove compounds without delta E
	for k in ['delta_e', 'energy']:
		oqmd_data[k] = pd.to_numeric(oqmd_data[k])
	oqmd_data = oqmd_data[~ np.logical_or(oqmd_data['delta_e'].isnull(), oqmd_data['energy'].isnull())]
		
	# Keep only the ground state of each composition
	oqmd_data['composition_str'] = oqmd_data['composition_pmg'].apply(lambda x: x.reduced_formula)
	oqmd_data.sort_values('energy', ascending=True, inplace=True)
	oqmd_data.drop_duplicates('composition_str', keep='first', inplace=True)
		
	# Feed in data as X,y, where X = training data and y = target values and fit the model. 
	# Use matminer to featurize the composition data. Returns a pandas array with element fraction of each element 
	# in a column, 0's in the rest. In this particular data frame, the matrix starts at column 6, so that's the chunk I take
	# a few lines down.
	oqmd_comp = cf.ElementFraction().featurize_dataframe(oqmd_data, "composition_pmg")
	oqmd_comp = oqmd_comp.as_matrix()
	oqmd_comp = oqmd_comp[:,6:]
	oqmd_energy = oqmd_data['energy'].values.reshape(-1, 1)
	
	# Featurize the glass data in the same way as the oqmd data. 
	glass_comp = cf.ElementFraction().featurize_dataframe(glass_data, "composition_pmg")
	glass_comp = glass_comp.as_matrix()
	glass_comp_str = glass_comp[:,:1]
	glass_comp_str = glass_comp_str.flatten
	glass_comp = glass_comp[:,2:]
	
	
	# SET UP SOME ML
	# Use 1 nearest neighbor to get closest energy
	num_neighbors = 1
	neigh = KNeighborsRegressor(n_neighbors=num_neighbors)
	
	# Fit the model with OQMD data, then predict the one nearest formation energy for comps in the glasses dataset
	model = neigh.fit(oqmd_comp, oqmd_energy) 
	kNearestEnergies = model.predict(glass_comp)
	kNearestEnergies = kNearestEnergies.flatten
	
	output = np.stack(glass_comp_str, kNearestEnergies)

	# Save the output of the model as a csv
	np.savetxt(str(num_neighbors) + "NearestEnergies and Compositions", output, header="Composition, Energy (eV)", delimiter=",", fmt="%s")

	end = time.time()
	print("Run Time: " + str(end - start))
	
	
	
def get_data(entry):
    """Get the composition, structure, band gap, and stability of an entry given its search result
    
    :param entry: dict, metadata for an entry as returned by Globus search
    :return: Several items
        - str, composition of the material
        - float, formation energy of material
        - float, Energy per atom (eV/atom)"""  
    
    # Get the metadata as a dict
    oqmd_data = entry['oqmd']
    
    # Return results
    return entry['mdf']['composition'], \
        oqmd_data.get('delta_e', {}).get('value'), \
        oqmd_data['total_energy'].get('value', np.nan)
		
		
		
# Run the script:
if __name__ == '__main__':
    main()