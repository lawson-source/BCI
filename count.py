import pandas as pd
import load_data as ld
import os
import itertools
import re


data = ld.load_data().load_data()
data=data[abs((data['Deviation']-data['Deviation'].mean())/data['Deviation'].std())<2.2]
data.loc[data.Deviation < 0.5, 'Deviation'] =0
data.loc[data.Deviation >= 0.5, 'Deviation'] =1
columns=data.columns[1:18]
for column in columns:
    data[column]=column+'__'+data[column]
dirf=os.path.abspath(os.path.dirname(__file__)) # root directory
data2=data.drop_duplicates(columns)

def count(item):
    result_item=data.groupby(item)['Deviation'].agg(['mean', 'count', 'sum'])
    result_item=pd.merge(result_item,data2.groupby(item)['Deviation'].agg([ 'count',]).rename(columns={'count':'ccount'}),left_index=True,right_index=True)
    return result_item

result=pd.DataFrame(columns=['mean','sum','count','ccount'])
for i in range(1,7):
    result_list=list(map(count, list(itertools.combinations(columns, i))))
    result_list=pd.concat(result_list)
    result_list=result_list[(result_list['ccount']/result_list['count']>0.5)&(result_list['count']>100)]
    result=result.append(result_list).sort_values('mean',ascending=False).head(20)
result.head(10).to_csv('result2.csv')



