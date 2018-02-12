import itertools

from mdf_forge.forge import Forge

from matminer.featurizers import composition as cf
from matplotlib import pyplot as plt
from matplotlib.colors import LogNorm
import numpy as np
import pandas as pd
from pymatgen import Composition
from pymatgen.core.periodic_table import Element
from sklearn import metrics
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import cross_val_score, cross_val_predict, GridSearchCV, ShuffleSplit

mdf = Forge()

query_string = 'mdf.source_name:oqmd AND (oqmd.configuration:static OR oqmd.configuration:standard) AND oqmd.converged:True'
result_records = mdf.aggregate(query_string)
print('Found %d compounds'%len(result_records))

print(result_records[0])
data = pd.DataFrame([x['mdf']['links']['landing_page'] for x in result_records], columns=['oqmd_url'])

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
		
		
data['composition'], data['delta_e'], data['energy'] = list(zip(*[get_data(x) for x in result_records]))
data['composition_pmg'] = data['composition'].apply(lambda x: Composition(x))
del result_records

for k in ['delta_e', 'energy']:
    data[k] = pd.to_numeric(data[k])
	
original_count = len(data)
data = data[~ np.logical_or(data['delta_e'].isnull(), data['energy'].isnull())]
print('Removed %d/%d entires'%(original_count - len(data), original_count))


original_count = len(data)
data['composition_str'] = data['composition_pmg'].apply(lambda x: x.reduced_formula)
data.sort_values('energy', ascending=True, inplace=True)
data.drop_duplicates('composition_str', keep='first', inplace=True)
print('Removed %d/%d entires'%(original_count - len(data), original_count))


original_size = len(data)
data.query('delta_e <= 5', inplace=True)
print('Removed %d/%d entires'%(original_count - len(data), original_count))