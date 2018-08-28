import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

folder = "./ChemCV"

for f in os.listdir(folder):
	print(f)
	data = pd.read_csv(os.path.join(folder, str(f)))
	elements = data['element']
	count = data['count']
	ndme = data['ndme']
	
	p = plt.figure()
	plt.scatter(count, ndme)
	for i, e in enumerate(elements):
		plt.annotate(e, (count[i], ndme[i]))
	plt.title("RMSE/$\sigma$ for " + str(f).split('.')[0])
	plt.xlabel("# for Testing")
	plt.ylabel("RMSE/$sigma$")
	plt.tight_layout()
	plt.savefig(str(f.split('.')[0]))