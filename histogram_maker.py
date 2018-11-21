import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt

# Read in data
property = "trg"
filename = "2018_11_05_gfa_predictions_" + property + ".csv"
all_data = pd.read_csv(filename)
gfa_ability = all_data['Actual GFA'].values
predicted_gfa_metric = all_data['Predicted GFA'].values

gformers = []
non_gformers = []

# Check for predicted GF/nonGF
for i in range(0, len(gfa_ability)):
    if gfa_ability[i] == 1:
        gformers.append(predicted_gfa_metric[i])
    else:
        non_gformers.append(predicted_gfa_metric[i])

# Convert from array to NumPy array
gformers = np.asarray(gformers)
non_gformers = np.asarray(non_gformers)

property = "Trg"

# Make hist of GF, nonGF, & together
transparency = 0.5
plt.figure(0)
gf_hist = plt.hist(gformers, bins="auto")
plt.title(property + " Glass Formers Histogram")
plt.xlabel(property)
plt.ylabel('Count')
plt.savefig("gf_hist_" + property + ".png")

plt.figure(1)
nongf_hist = plt.hist(non_gformers, bins="auto")
plt.title(property + " Non-Glass Formers Histogram")
plt.xlabel(property)
plt.ylabel('Count')
plt.savefig("nongf_hist_" + property + ".png")

num_bins = 20
width = 0.1
plt.figure(2)
_, bins, _ = plt.hist(gformers, color="b", alpha = transparency, label="Glass formers")
plt.hist(non_gformers, bins = bins, color="r", alpha = transparency, label="Non-Glass Formers")
plt.title("Histogram of Experimental Classification Data")
plt.xlabel("Trg Predictions")
plt.ylabel('Count')
plt.legend()
plt.savefig("both_hist_" + property + ".png")
