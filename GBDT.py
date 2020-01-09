import pandas as pd
import load_data as ld
import lightgbm as lgb
from sklearn.model_selection import train_test_split

data = ld.load_data().load_data()
data.loc[data.Deviation < 0.5, 'Deviation'] = 0
data.loc[data.Deviation >= 0.5, 'Deviation'] = 1
xdata = data[data.columns[0:17]]
ydata = data['Deviation'].astype('int')
train_data, test_data, train_targets, test_targets = train_test_split(xdata, ydata, random_state=0,test_size=0.25)
