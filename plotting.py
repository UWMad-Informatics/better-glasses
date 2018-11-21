import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt

data = pd.read_csv('element_count.csv')
element = np.flip(data['Element'].values, axis=0)
count = np.flip(data['Count'].values, axis=0)

matplotlib.rc('xtick', labelsize=14)
matplotlib.rc('ytick', labelsize=14)
p = plt.figure(figsize=(6.9,14.3))
plt.barh(np.arange(len(element)), count, height=3, color='b', tick_label=element, fill=True)
#for i, e in enumerate(elements):
#	plt.annotate(e, (count[i], ndme[i]))
plt.title("Elemental Representation in Thermophysical Dataset", fontsize=16)
plt.ylabel("Element", fontsize=16)
plt.xlabel("Count", fontsize=16)
plt.tight_layout()
plt.savefig("element_analysis.png", bbox_inches="tight")
plt.show()

print(len(element))
