import matplotlib.pyplot as plt
import numpy as np

properties = np.array(["Tg", "Tl", "Tx", "Trg", "gamma", "omega", "log(Rc)"])

kbest_3fold = [.2, .266, .223, .744, .728, .685, .575]
citrination = [.18, .24, .19, .6, .63, .55, .55]

width = .2
x = np.arange(len(properties))

fig, ax = plt.subplots()
plt.tick_params(axis='both', which='major', labelsize=18)

kbest_3fold = ax.bar(x, kbest_3fold, width, tick_label = properties, label="MASTML")
citrination = ax.bar(x+width, citrination, width, tick_label = properties, label="Citrination")

ax.set_ylabel('RMSE/$\sigma$', fontsize=32)
ax.set_xlabel('Property', fontsize=32)
ax.set_title('RMSE/$\sigma$ for Feature Selection', fontsize=40)
x_ticks = [float(i + width) for i in x]
ax.tick_params(axis='both', which='major', labelsize=24)
ax.set_xticks(x_ticks)

plt.tight_layout()
ax.legend((kbest_3fold[0], citrination[0]),("MASTML", "Citrination"), prop={'size': 20})

plt.show()
