import pandas as pd
import numpy as np
import csv

# Read in actual values collected from extracting data.
actual_values = "C:/Users/mvane/Documents/Skunkworks/BMG/Data/BMG_full_dataset_with_energies.csv"	

# Make dictionaries of the actual values of the GFA metrics
# Read in values and make into numpy arrays
actual_vals = pd.read_csv(actual_values)
all_form = actual_vals['formula'].as_matrix()
all_dft = actual_vals['PROPERTY: Nearest DFT Formation Energy (eV)'].as_matrix()
all_tg = actual_vals['PROPERTY: Tg (K)'].as_matrix()
all_tl = actual_vals['PROPERTY: Tl (K)'].as_matrix()
all_tx = actual_vals['PROPERTY: Tx (K)'].as_matrix()
all_trg = actual_vals['PROPERTY: Trg'].as_matrix()
all_gamma = actual_vals['PROPERTY: $\gamma$'].as_matrix()
all_omega = actual_vals['PROPERTY: $\omega$'].as_matrix()


# Al
al_forms = []
al_tg = []
al_tl = []
al_tx = []
al_trg =[]
al_gamma = []
al_omega = []
without_al_tg = all_tg
without_al_tl = all_tl
without_al_tx = all_tx
without_al_trg = all_trg
without_al_gamma = all_gamma
without_al_omega = all_omega
without_al_forms = all_form
al_energies = []
without_al_energies = all_dft
al_remove = []
for i in range(0, len(all_form)):
	if "Al" in str(all_form[i]):
		al_forms.append(all_form[i])
		al_energies.append(all_dft[i])
		al_tg.append(all_tg[i])
		al_tl.append(all_tl[i])
		al_tx.append(all_tx[i])
		al_trg.append(all_trg[i])
		al_gamma.append(all_gamma[i])
		al_omega.append(all_omega[i])
		al_remove.append(i)
		
without_al_forms = np.delete(without_al_forms, al_remove).tolist()
without_al_energies = np.delete(without_al_energies, al_remove).tolist()
without_al_tg = np.delete(without_al_tg, al_remove).tolist()
without_al_tl = np.delete(without_al_tl, al_remove).tolist()
without_al_tx = np.delete(without_al_tx, al_remove).tolist()
without_al_trg =np.delete(without_al_trg, al_remove).tolist()
without_al_gamma = np.delete(without_al_gamma, al_remove).tolist()
without_al_omega = np.delete(without_al_omega, al_remove).tolist()
rows = zip(without_al_forms, without_al_energies, without_al_tg, without_al_tl, without_al_tx, without_al_trg, without_al_gamma, without_al_omega)
with open('bmg_no_al.csv', "w", newline='') as f:
    writer = csv.writer(f)
    for row in rows:
        writer.writerow(row)
		
rows = zip(al_forms, al_energies, al_tg, al_tl, al_tx, al_trg, al_gamma, al_omega)
with open('bmg_only_al.csv', "w", newline='') as f:
    writer = csv.writer(f)
    for row in rows:
        writer.writerow(row)
		
# Mg
mg_forms = []
mg_tg = []
mg_tl = []
mg_tx = []
mg_trg =[]
mg_gamma = []
mg_omega = []
without_mg_tg = all_tg
without_mg_tl = all_tl
without_mg_tx = all_tx
without_mg_trg = all_trg
without_mg_gamma = all_gamma
without_mg_omega = all_omega
without_mg_forms = all_form
mg_energies = []
without_mg_energies = all_dft
mg_remove = []
for i in range(0, len(all_form)):
	if "Mg" in str(all_form[i]):
		mg_forms.append(all_form[i])
		mg_energies.append(all_dft[i])
		mg_tg.append(all_tg[i])
		mg_tl.append(all_tl[i])
		mg_tx.append(all_tx[i])
		mg_trg.append(all_trg[i])
		mg_gamma.append(all_gamma[i])
		mg_omega.append(all_omega[i])
		mg_remove.append(i)
		
without_mg_forms = np.delete(without_mg_forms, mg_remove).tolist()
without_mg_energies = np.delete(without_mg_energies, mg_remove).tolist()
without_mg_tg = np.delete(without_mg_tg, mg_remove).tolist()
without_mg_tl = np.delete(without_mg_tl, mg_remove).tolist()
without_mg_tx = np.delete(without_mg_tx, mg_remove).tolist()
without_mg_trg =np.delete(without_mg_trg, mg_remove).tolist()
without_mg_gamma = np.delete(without_mg_gamma, mg_remove).tolist()
without_mg_omega = np.delete(without_mg_omega, mg_remove).tolist()
rows = zip(without_mg_forms, without_mg_energies, without_mg_tg, without_mg_tl, without_mg_tx, without_mg_trg, without_mg_gamma, without_mg_omega)
with open('bmg_no_mg.csv', "w", newline='') as f:
    writer = csv.writer(f)
    for row in rows:
        writer.writerow(row)
		
rows = zip(mg_forms, mg_energies, mg_tg, mg_tl, mg_tx, mg_trg, mg_gamma, mg_omega)
with open('bmg_only_mg.csv', "w", newline='') as f:
    writer = csv.writer(f)
    for row in rows:
        writer.writerow(row)

# Cu
cu_forms = []
cu_tg = []
cu_tl = []
cu_tx = []
cu_trg =[]
cu_gamma = []
cu_omega = []
without_cu_tg = all_tg
without_cu_tl = all_tl
without_cu_tx = all_tx
without_cu_trg = all_trg
without_cu_gamma = all_gamma
without_cu_omega = all_omega
without_cu_forms = all_form
cu_energies = []
without_cu_energies = all_dft
cu_remove = []
for i in range(0, len(all_form)):
	if "Cu" in str(all_form[i]):
		cu_forms.append(all_form[i])
		cu_energies.append(all_dft[i])
		cu_tg.append(all_tg[i])
		cu_tl.append(all_tl[i])
		cu_tx.append(all_tx[i])
		cu_trg.append(all_trg[i])
		cu_gamma.append(all_gamma[i])
		cu_omega.append(all_omega[i])
		cu_remove.append(i)
		
without_cu_forms = np.delete(without_cu_forms, cu_remove).tolist()
without_cu_energies = np.delete(without_cu_energies, cu_remove).tolist()
without_cu_tg = np.delete(without_cu_tg, cu_remove).tolist()
without_cu_tl = np.delete(without_cu_tl, cu_remove).tolist()
without_cu_tx = np.delete(without_cu_tx, cu_remove).tolist()
without_cu_trg =np.delete(without_cu_trg, cu_remove).tolist()
without_cu_gamma = np.delete(without_cu_gamma, cu_remove).tolist()
without_cu_omega = np.delete(without_cu_omega, cu_remove).tolist()
rows = zip(without_cu_forms, without_cu_energies, without_cu_tg, without_cu_tl, without_cu_tx, without_cu_trg, without_cu_gamma, without_cu_omega)
with open('bmg_no_cu.csv', "w", newline='') as f:
    writer = csv.writer(f)
    for row in rows:
        writer.writerow(row)
		
rows = zip(cu_forms, cu_energies, cu_tg, cu_tl, cu_tx, cu_trg, cu_gamma, cu_omega)
with open('bmg_only_cu.csv', "w", newline='') as f:
    writer = csv.writer(f)
    for row in rows:
        writer.writerow(row)

# Zr
zr_forms = []
zr_tg = []
zr_tl = []
zr_tx = []
zr_trg =[]
zr_gamma = []
zr_omega = []
without_zr_tg = all_tg
without_zr_tl = all_tl
without_zr_tx = all_tx
without_zr_trg = all_trg
without_zr_gamma = all_gamma
without_zr_omega = all_omega
without_zr_forms = all_form
zr_energies = []
without_zr_energies = all_dft
zr_remove = []
for i in range(0, len(all_form)):
	if "Zr" in str(all_form[i]):
		zr_forms.append(all_form[i])
		zr_energies.append(all_dft[i])
		zr_tg.append(all_tg[i])
		zr_tl.append(all_tl[i])
		zr_tx.append(all_tx[i])
		zr_trg.append(all_trg[i])
		zr_gamma.append(all_gamma[i])
		zr_omega.append(all_omega[i])
		zr_remove.append(i)
		
without_zr_forms = np.delete(without_zr_forms, zr_remove).tolist()
without_zr_energies = np.delete(without_zr_energies, zr_remove).tolist()
without_zr_tg = np.delete(without_zr_tg, zr_remove).tolist()
without_zr_tl = np.delete(without_zr_tl, zr_remove).tolist()
without_zr_tx = np.delete(without_zr_tx, zr_remove).tolist()
without_zr_trg =np.delete(without_zr_trg, zr_remove).tolist()
without_zr_gamma = np.delete(without_zr_gamma, zr_remove).tolist()
without_zr_omega = np.delete(without_zr_omega, zr_remove).tolist()
rows = zip(without_zr_forms, without_zr_energies, without_zr_tg, without_zr_tl, without_zr_tx, without_zr_trg, without_zr_gamma, without_zr_omega)
with open('bmg_no_zr.csv', "w", newline='') as f:
    writer = csv.writer(f)
    for row in rows:
        writer.writerow(row)
		
rows = zip(zr_forms, zr_energies, zr_tg, zr_tl, zr_tx, zr_trg, zr_gamma, zr_omega)
with open('bmg_only_zr.csv', "w", newline='') as f:
    writer = csv.writer(f)
    for row in rows:
        writer.writerow(row)