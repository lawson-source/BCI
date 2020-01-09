import  pandas as pd
import os


data=pd.read_csv('./result_data/Ident_No.csv')
good_data=data[data['Deviation']<0.3]
good_data['Deviation']=0
good_data.to_csv('./result_data/good_data.csv')
print(good_data.shape)
bad_data=data[data['Deviation']>=0.5]
bad_data['Deviation']=1
bad_data.to_csv('./result_data/bad_data.csv')
print(bad_data.shape)