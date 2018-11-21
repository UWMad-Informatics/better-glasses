import pandas as pd
import numpy as np
import csv

file = "BMG_ttemp_data.csv"
all_data = pd.read_csv(file)
formula = all_data['formula']
temp = all_data['PROPERTY: Tx (K)']
energy = all_data['PROPERTY: Nearest DFT Formation Energy (eV)']

for i in reversed(range(0, len(temp))):
    if np.isnan(temp[i]):
        del temp[i]
        del formula[i]
        del energy[i]

with open("removed_null_vals.csv", 'w', newline = '') as f:
    writer = csv.writer(f)
    header = ["formula", "PROPERTY: Tx (K)", "PROPERTY: Nearest DFT Formation Energy (eV)"]
    writer.writerow(header)
    rows = zip(formula, temp, energy)
    for row in rows:
        writer.writerow(row)
