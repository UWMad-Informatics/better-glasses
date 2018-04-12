import json
import numpy as np
import math

# Read in json file from obtained using citrination_retrieve_predicted_vals
filename = "/Users/vanessa/Documents/GitHub/better-glasses/PredictedValuesFromCitrination.txt"
with open(filename) as file:
    all_data = json.load(file)

Tg_x = []
print(type(Tg_x))
Tg_y = []
Tg_y_err = []
Tl_x = []
Tl_y = []
Tl_y_err = []
Tx_x = []
Tx_y = []
Tx_y_err = []

for property in range(0, len(all_data['reports'][0])):
    # Retrieve the x value (actual property value), y value (predicted property value), and the error in the prediction
    # Current file is in order Tx, log(Rc), gamma, omega, Tg, Tl, Trg
    model = all_data['reports'][property]['modelName']
    x = (all_data['reports'][property]['performancePlots'][0]['data'][0]['x'])
    y = (all_data['reports'][property]['performancePlots'][0]['data'][0]['y'])
    err_y = (all_data['reports'][property]['performancePlots'][0]['data'][0]['error_y'])

    # Save each x, y, and y_err value for the materials properties
    if model == "Tg":
        Tg_x = x
        Tg_y = y
        Tg_y_err = y_err
    elif model == "Tl":
        Tl_x = x
        Tl_y = y
        Tl_y_err = y_err
    elif model == "Tx":
        Tx_x = x
        Tx_y = y
        Tx_y_err = y_err
    else:
        pass

# Convert the lists of materials properties to np arrays
Tg_x = np.asarray(Tg_x)
Tg_y = np.asarray(Tg_y)
Tg_y_err = np.asarray(Tg_y_err)
Tl_x = np.asarray(Tl_x)
Tl_y = np.asarray(Tl_y)
Tl_y_err = np.asanyarray(Tl_y_err)
Tx_x = np.asarray(Tx_x)
Tx_y = np.asarray(Tx_y)
Tx_y_err = np.asarray(Tx_y_err)

# Calculate Trg (=Tg/Tl) and the standard deviation & mean of Tg and Tl
calc_Trg = Tg_y/Tl_y
calc_Trg_err = 0
stdev_Tg = np.std(Tg_y)
stdev_Tl = np.std(Tl_y)
mean_Tg = np.mean(Tg_y)
mean_Tl = np.mean(Tl_y)
covar_Tg_Tl = 0

#for val in range(0, len(calc_Trg)):
#    error_calc = calc_Trg[val]*math.sqrt(math.pow(Tg_y_err[val]/Tg_y[val], 2) + math.pow(Tl_y_err[val]/Tl_y[val], 2)
#                                         - (2*covar_Tg_Tl)/(Tg_y[val]*Tl_y[val]))
#    print(error_calc)
#    calc_Trg_err.extend(error_calc)
