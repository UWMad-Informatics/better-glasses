import os
import pandas as pd
import csv
import matplotlib.pyplot as plt

# Get to directory and loop through all folders in the results
for folder in os.listdir(os.getcwd())
    # Check for the leave one group out CV folder name IDer:
    if "LeaveOneGroupOut" in folder:
        # Get the predictions on the validation data file
        # Get formula and Trg prediction from file

        
