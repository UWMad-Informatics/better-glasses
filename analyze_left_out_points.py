import pandas as pd
import os
import numpy as np

# Actual Data
act_data = pd.read_csv("/Users/vanessa/Documents/Skunkworks/BMG/Data/BMG_full_dataset_with_energies.csv")
act_form = act_data['formula'].tolist()
act_trg = act_data['PROPERTY: Trg'].tolist()
act_gamma = act_data['PROPERTY: $\\gamma$'].tolist()
act_omega = act_data['PROPERTY: $\\omega$'].tolist()

# Covert to dict with key as formula and a list with Trg, gamma, omega
act_dict = {}
for i in range(0, len(act_form)):
    act_dict[act_form[i]] = [act_trg[i], act_gamma[i], act_omega[i]]

avg_trg_err = np.zeros(6)
avg_gamma_err = np.zeros(6)
avg_omega_err = np.zeros(6)

# Predicted data folder
folder = "/Users/vanessa/Documents/Skunkworks/BMG/Data/Au Predictions"
for file in os.listdir(folder):
    predicted_data = pd.read_csv(os.path.join(folder, file))
    form = predicted_data['formula']
    tg = predicted_data['Property Tg'].values
    tl = predicted_data['Property Tl'].values
    tx = predicted_data['Property Tx'].values

    num_predicted = len(form)
    trg = tg/tl
    gamma = tx/(tg + tl)
    omega = (tg/tx) - 2*(tg/(tg + tl))

    trg_loss = np.empty(num_predicted)
    gamma_loss = np.empty(num_predicted)
    omega_loss = np.empty(num_predicted)

    # Calculate absolute
    for i in range(0, num_predicted):
        trg_loss = np.append(trg_loss, act_dict[form[i]][0] - trg[i])
        gamma_loss = np.append(gamma_loss, act_dict[form[i]][1] - gamma[i])
        omega_loss = np.append(omega_loss, act_dict[form[i]][2] - omega[i])

    for x in [trg_loss, gamma_loss, omega_loss]:
        x = x[~np.isnan(x)]

    temp_trg_err = np.mean(trg_loss)
    temp_gamma_err = np.mean(gamma_loss)
    temp_omega_err = np.mean(omega_loss)

    # Check to make sure there are already values at each position
    if avg_trg_err[num_predicted-1] != 0:
        avg_trg_err = np.put(avg_trg_err, num_predicted-1,np.mean([temp_trg_err, avg_trg_err[num_predicted-1]]))
        avg_gamma_err = np.put(avg_gamma_err, num_predicted-1,np.mean([temp_trg_err, avg_trg_err[num_predicted-1]]))
        avg_omega_err = np.put(avg_omega_err, num_predicted-1,np.mean([temp_trg_err, avg_trg_err[num_predicted-1]]))
    else:
        print(type(avg_trg_err))
        print(type(temp_trg_err))
        avg_trg_err = np.put(avg_trg_err, num_predicted-1,temp_trg_err)
        avg_gamma_err = np.put(avg_gamma_err, num_predicted-1,temp_gamma_err)
        avg_omega_err = np.put(avg_omega_err, num_predicted-1,temp_omega_err)
        print(avg_trg_err)

print("Trg Errors: " + str(avg_trg_err))
print("Gamma Errors: " + str(avg_gamma_err))
print("Omega Errors: " + str(avg_omega_err))
