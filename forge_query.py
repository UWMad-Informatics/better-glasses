from mdf_forge.forge import Forge
from sklearn.neighbors import KNeighborsRegressor
import pandas

# Read in dataset
filepath = "C:\\Users\\mvane\\Documents\\Skunkworks\\BMG\\BMG_full_dataset.csv"
all_data = pandas.read_csv(filepath)
all_formulas = all_data["formula"]

# Set up forge
mdf = Forge()

# Add a field to match. We'd like to query OQMD, so we'll limit results to those from OQMD here.
mdf.match_sources("oqmd")
# Feed in the elements we'd like to search for. Starting w/ binaries so I can figure out if this is maybe working
mdf.match_elements(["Ca", "Mg", "Zn"])

# Search for entries with a specific element. Here, search for the largest element perhaps?
# Advanced args (match field or source) cleared when we call search(), so add reset_query = false to keep matches
# Use mdf.aggregate() if we need to retrieve > 10000 results from OQMD
results = mdf.search(reset_query=False)

# This doesn't work for me yet
# Download results. You need to have your computer set up to be an endpoint with globus and have it running 
# (See https://github.com/materials-data-facility/forge/blob/master/docs/tutorials/6%20-%20Data%20Retrieval%20Functions.ipynb)
#mdf.globus_download(results)