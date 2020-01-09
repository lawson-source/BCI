import pandas as pd
import numpy as np
import load_data as ld
import pyfpgrowth as pyfg
import os
import time
import apriori
dirpath=os.path.abspath(os.path.dirname(__file__)) # root directory

def Find_reject_frendencyitem(data,minS):
    for column in data.columns:
        data[column] = column + '__' + data[column]
    order_records = np.array(data.astype('str')).tolist()
    L, suppData = apriori.apriori(order_records, minSupport=minS)  # find frequent itemsets
    return suppData




if __name__ == '__main__':
    data = ld.load_data().load_data()
    data.loc[data.Deviation < 0.5, 'Deviation'] = 0
    data.loc[data.Deviation >= 0.5, 'Deviation'] = 1
    print(time.asctime(time.localtime(time.time())))
    item = Find_reject_frendencyitem(data[data['Deviation'] == 1][data.columns[0:17]].astype('str'), minS=0.1)
    item1=pd.DataFrame({'item':list(item.keys()),'n':list(item.values())})
    print(time.asctime(time.localtime(time.time())))
    item = Find_reject_frendencyitem(data[data.columns[0:17]].astype('str'),minS=0.1)
    item2 = pd.DataFrame({'item':list(item.keys()),'N':list(item.values())})
    print(time.asctime(time.localtime(time.time())))
    items=pd.merge(item1,item2,on='item',how='left')
    items['confidence']=items['n']/items['N']
    items.to_csv(dirpath+'/result_data/combination_items2.csv')




