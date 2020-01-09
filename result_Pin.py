import  pandas as pd
import os
import numpy as np
import apriori
import pyfpgrowth as pyfg
import process_data

columns = ['Deviation', 'PinCharacteristic']
dirf=os.path.abspath(os.path.dirname(__file__))
good_data=pd.read_csv(dirf+'/result_data/good_data_threshold_default.csv')
bad_data=pd.read_csv(dirf+'/result_data/bad_data_threshold_default.csv')
data=bad_data.append(good_data, ignore_index=True)
data = data[columns].astype('str')
bad_data=bad_data[columns].astype('str')
for column in columns:
        data[column] = column+'__' + data[column]
        bad_data[column]= column+'__' + bad_data[column]

order_records = np.array(data).tolist()
order_records_bad= np.array(bad_data).tolist()
L, suppData = apriori.apriori(order_records_bad, minSupport=0.01)  # 计算得到满足最小支持度的规则
rules = apriori.generateRules(order_records, L, suppData, minConf=0.5)
rules=pd.DataFrame(rules, columns=['item1', 'item2', 'instance', 'support', 'confidence','lift'])
data_result = rules
rules_sort = data_result.sort_values(['lift'], ascending=False)
print(rules_sort.head(10))
rules_sort .to_csv(dirf+'/result_data/result_PinCharateristic2.csv',index=False)
