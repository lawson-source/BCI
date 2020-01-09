import  pandas as pd
import process_data
import os

dirf=os.path.abspath(os.path.dirname(__file__))

columns =['Deviation',
          'toolData[1].toolID',
                'toolData[12].toolID', 'toolData[2].toolID',]
data=pd.read_csv(dirf+'/result_data/Ident_No.csv')
good_data=data[data['Deviation']<0.5]
good_data=good_data.sample(n=5000)
good_data['Deviation']=0
bad_data=pd.read_csv(dirf+'/result_data/bad_data.csv')
data=bad_data.append(good_data, ignore_index=True)
data = data[columns].astype('str')
for column in columns:
        data[column] = column + '__' + data[column]
mins=(0.05*bad_data.shape[0]/data.shape[0])
rules=process_data.Apriori(data[columns],minS=mins,minC=0.3)
data_result = rules
rules_sort = data_result.sort_values(['lift'], ascending=False)
print(rules_sort.head(10))
rules_sort .to_csv(dirf+'/result_data/result_toolData_random2.csv',index=False)
