import pandas as pd
import matplotlib.pyplot as plt
import load_data as ld



data = ld.load_data().load_data()
proba = pd.read_csv('proability.csv', )
for column in data.columns[0:17]:
    data[column] = data[column].replace(proba['index'].values, proba['value'].values)

# Marker size in units of points^2
volume = (150 * data['Deviation'] )

fig, ax = plt.subplots()
ax.scatter(data[0:17].mean(axis=0)[:-1],data[0:17].mean(axis=0)[1:],s=volume ,alpha=0.5)

ax.set_xlabel(r'$\Delta_i$', fontsize=15)
ax.set_ylabel(r'$\Delta_{i+1}$', fontsize=15)
ax.set_title('Volume and percent change')

ax.grid(True)
fig.tight_layout()

plt.show()