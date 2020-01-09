import  pandas as pd
import os
import process_data
dirf=os.path.abspath(os.path.dirname(__file__))
columns =['Deviation',
                 'MouldMachineNo',
                'MouldNestNo', 'Moulding.toolData[1].toolID',
                'Moulding.toolData[2].toolID', 'Moulding.toolData[3].toolID',
                'Moulding.toolData[4].toolID', 'Moulding.toolData[5].toolID',
                'Moulding.toolData[6].toolID', 'Moulding.toolData[7].toolID',] # the name of columns to analyze
data=pd.read_csv(dirf+'/result_data/Ident_No.csv')
good_data=data[data['Deviation']<0.5] # Filter the good data
good_data=good_data.sample(n=5000)    # simmple random sampling
good_data['Deviation']=0              # transform to labe
bad_data=pd.read_csv(dirf+'/result_data/bad_data.csv')
data=bad_data.append(good_data, ignore_index=True) # concat data
data = data[columns].astype('str')    # transform type of data to string
for column in columns:                # add name of column to value
        data[column] = column + '__' + data[column]
mins=(0.05*bad_data.shape[0]/data.shape[0])
rules=process_data.Apriori(data[column],minS=mins,minC=0.2)   # asssociation Analysis
data_result = rules
rules_sort = data_result.sort_values(['confidence'], ascending=False)  # sort data by value of confidence
print(rules_sort.head(10))
rules_sort .to_csv(dirf+'/result_data/result_Mould_random1.csv',index=False) #save data

