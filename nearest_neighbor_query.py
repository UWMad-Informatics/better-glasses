# Use SKLearn's Nearest Neighbors function to find the closest values from the OQMD data base
from sklearn.neighbors import nearestneighbors
import pandas

# Read in the formulas we want to find
miracle_formulas = pandas.read_csv("C:\Users\mvane\Documents\Skunkworks\BMG\Miracle_Binary_Formulas.csv")
