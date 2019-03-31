# A script to generate a range of compositions given a string

import pandas as pd
import csv
from pymatgen.core.composition import Composition
from pymatgen.core.periodic_table import Element

from matminer_design_module.matminer.design.composition import CompositionGenerator

original_comps_file = "./original_comps.csv"

def main():
    # Read in the csv and get the formulas
    orig_comps = pd.read_csv(original_comps_file).values
    orig_comps = orig_comps[:,0]

    # Convert the formulas to pymatgen objects
    for c in orig_comps:
        c = Composition(c)
        elements = []
        for key in c:
            elements.append(key)
        gen = CompositionGenerator(elements, min_elements=1,
                                    max_elements=len(elements), spacing=5)
        stoichs = list(gen._generate_stoichiometries(1, 4))

    # Generate the new compositions

    # Write the new compositions to a csv
    #with open("./generated_comps.csv", 'wb') as outfile:
    #    wr = csv.writer(outfile)
        #TODO fill with what I'm actually writing wr.writerow(comps)
    #outfile.close()

# Run the script:
if __name__ == '__main__':
    main()
