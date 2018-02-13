from mdf_forge.forge import Forge
from matminer.featurizers import composition as cf
from matplotlib import pyplot as plt
import numpy as np
import pandas as pd
import itertools
from pymatgen import Composition
from pymatgen.core.periodic_table import Element
from sklearn import metrics
from sklearn.neighbors import KNeighborsRegressor

def main():
	# Read in dataset
	filepath = "C:\\Users\\mvane\\Documents\\GitHub\\better-glasses\\formulas_subset.csv"
	glass_data = pd.read_csv(filepath)
	glass_data = glass_data['composition']
	# Make the compositions of the glasses data into pymatgen objects to match the data from OQMD
	# Convert data into pandas dataframe
	glass_data = pd.DataFrame(data = glass_data, columns=['composition'])
	# Convert compositions to pymatgen objects
	glass_data['composition'] = glass_data['composition'].apply(lambda x: Composition(x))

	# Set up forge
	mdf = Forge()

	# Get all converged results from OQMD. Currently have "quick demo" set so searches don't take as long while testing code
	# Note: Advanced args (match field or source) cleared when we call search(), so add reset_query = false to keep matches
	# Note: Use mdf.aggregate() if we need to retrieve > 10000 results from OQMD
	result_records = mdf.aggregate('mdf.source_name:oqmd AND (oqmd.configuration:static OR oqmd.configuration:standard) ' + 
		'AND oqmd.converged:True AND mdf.scroll_id:<10000')
	print('Found %d compounds'%len(result_records))

	# Convert results into pandas dataframe and get lowest energy compound at each composition
	oqmd_data = pd.DataFrame([x['mdf']['links']['landing_page'] for x in result_records], columns=['oqmd_url'])

	# Get composition of alloys and enthalpy of formation
	oqmd_data['composition'], oqmd_data['delta_e'], oqmd_data['energy'] = list(zip(*[get_data(x) for x in result_records]))
	
	# Convert compositions to pymatgen objects
	oqmd_data['composition_pmg'] = oqmd_data['composition'].apply(lambda x: Composition(x))
	
	# Remove results from memory for better efficiency
	del result_records
	
	# Remove compounds without delta E
	for k in ['delta_e', 'energy']:
		oqmd_data[k] = pd.to_numeric(oqmd_data[k])
		
	# Keep only the ground state of each composition
	oqmd_data['composition_str'] = oqmd_data['composition_pmg'].apply(lambda x: x.reduced_formula)
	oqmd_data.sort_values('energy', ascending=True, inplace=True)
	oqmd_data.drop_duplicates('composition_str', keep='first', inplace=True)
	
	print("We've made it this far")
	
	# Convert raw data into something usuable for the kNN method
	feature_calculators = [cf.Stoichiometry(), cf.ElementProperty.from_preset("magpie"), \
		cf.ValenceOrbital(props=['frac']), cf.IonProperty()]
		
	# Build that data as 'features'. 
	feature_labels = list(itertools.chain.from_iterable([x.feature_labels() for x in feature_calculators]))
	
	for fc in feature_calculators:
		oqmd_data = fc.featurize_dataframe(oqmd_data, col_id='composition_pmg')
		glass_data = fc.featurize_dataframe(glass_data, col_id='composition')
		
	print(oqmd_data)
	print()
	print(glass_data)
	
	# SET UP SOME ML
	num_neighbors = 10
	
	neigh = KNeighborsRegressor(n_neighbors=num_neighbors)
	# Feed in data as X,y, where X = training data and y = target values and fit the model
	neigh.fit(glass_data, oqmd_data) 
	
	
	
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