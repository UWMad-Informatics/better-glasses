# Use SKLearn's Nearest Neighbors function to find the closest values from the OQMD data base
from sklearn.neighbors import nearestneighbors
import pandas
import itertools
from mdf_forge.forge import Forgefrom matminer.featurizers 
import composition as cf
from matplotlib import pyplot as plt
from matplotlib.colors import LogNorm
import numpy as np
import pandas as pd
from pymatgen import Composition
from pymatgen.core.periodic_table import Element
from sklearn import metrics


# Read in the formulas we want to find
miracle_formulas = pandas.read_csv("C:\Users\mvane\Documents\Skunkworks\BMG\Miracle_Binary_Formulas.csv")

# Create a forge instance
mdf = Forge()

# Create the string we're going to query for
query_string = 'mdf.source_name:oqmd AND (oqmd.configuration:static OR oqmd.configuration:standard) AND oqmd.converged:True'
# Run a query through Forge
result_records = mdf.aggregate(query_string)

# Print how many records we found
print('Found %d compounds'%len(result_records))


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