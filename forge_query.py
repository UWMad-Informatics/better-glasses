from mdf_forge.forge import Forge
from matminer.featurizers import composition as cf
from matplotlib import pyplot as plt
import numpy as np
import pandas as pd
from pymatgen import Composition
from pymatgen.core.periodic_table import Element
from sklearn import metrics
from sklearn.neighbors import NearestNeighbors

def main():
	# Read in dataset
	filepath = "C:\\Users\\mvane\\Documents\\GitHub\\better-glasses\\formulas_subset.csv"
	glass_data = pd.read_csv(filepath)
	glass_data = glass_data['composition']

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
	oqmd_data['composition'], oqmd_data['delta_e'], oqmd_data['enerprint(oqmd_data['composition'])

	
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
	
	# SET UP SOME ML
	
	# Find the nearest compositions and create cluster
	
	# Find average formation energy for the cluster and set this value to the glasses data's formation energy

	
	
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