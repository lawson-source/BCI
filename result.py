import os
import process_data
import  pandas as pd
# sort data in descend order by the value of Deviation, then keep first record  and delete the duplicate data of Ident_NO

columns =['Deviation',
                'matDataBComponents[1].batch',
                'matDataBComponents[1].vendor', 'matDataBComponents[2].batch',
                'matDataBComponents[2].vendor', 'matDataBComponents[3].batch',
                'matDataBComponents[3].vendor', 'matDataBComponents[4].batch',
                'matDataBComponents[4].vendor', 'toolData[1].toolID',
                'toolData[12].toolID', 'toolData[2].toolID',
               'MouldMachineNo',
                'MouldNestNo', 'TablePosition', 'Moulding.toolData[1].toolID',
                'Moulding.toolData[2].toolID', 'Moulding.toolData[3].toolID',
                'Moulding.toolData[4].toolID', 'Moulding.toolData[5].toolID',
                'Moulding.toolData[6].toolID', 'Moulding.toolData[7].toolID',] # analysis dimension
dirf=os.path.abspath(os.path.dirname(__file__)) # root directory
File_dir =dirf+'/data' # directory of data source
Filelist = os.listdir(File_dir) # all of file name of data source
data = pd.read_csv(File_dir + '/' + Filelist[0]) # read first data source
data=data[columns]

#read data and sort data in descend order by the value of Deviation, then keep first record  and delete the duplicate data of Ident_NO
for i in range(1, len(Filelist)):
        print(Filelist[i])
        if Filelist[i] == ".DS_Store":
            continue
        df = pd.read_csv(File_dir + '/' + Filelist[i])
        df=df[columns]
        data = data.append(df, ignore_index=True)
        data = data.dropna()
        data=data.sort_values('Deviation',ascending=False)
        data = data.drop_duplicates('Ident No.',keep='first')
        print(data.shape)
print(data.shape)
data = data.sort_values('Deviation', ascending=False)
data = data.drop_duplicates('Ident No.', keep='first')

# filter data, the deciation of good data is less than 0.5, the deciation of bad data is  not less than 0.5
good_data=data[data['Deviation']<0.5]
good_data=good_data.sample(n=5000)
good_data['Deviation']=0
bad_data=data[data['Deviation']>=0.5]
bad_data['Deviation']=1

# find frequent itemset and  Generate association rules
data=bad_data.append(good_data, ignore_index=True)
data = data[columns].astype('str')
for column in columns:
        data[column] = column + '__' + data[column]  #Appends the column name to the value
mat_columns=['Deviation',
          'matDataBComponents[1].batch',
          'matDataBComponents[1].vendor', 'matDataBComponents[2].batch',
          'matDataBComponents[2].vendor', 'matDataBComponents[3].batch',
          'matDataBComponents[3].vendor', 'matDataBComponents[4].batch',
          'matDataBComponents[4].vendor']
mould_cloumns=columns =['Deviation',
                 'MouldMachineNo',
                'MouldNestNo', 'Moulding.toolData[1].toolID',
                'Moulding.toolData[2].toolID', 'Moulding.toolData[3].toolID',
                'Moulding.toolData[4].toolID', 'Moulding.toolData[5].toolID',
                'Moulding.toolData[6].toolID', 'Moulding.toolData[7].toolID',]
tool_columns=['Deviation',
          'toolData[1].toolID',
                'toolData[12].toolID', 'toolData[2].toolID',]
mins=(0.1*bad_data.shape[0]/data.shape[0])  # Minimum support for find frequent itemsets
mat_result=process_data.Apriori(data[mat_columns],minS=mins,minC=0.3).sort_values(['lift'], ascending=False) # invoke Apriori algorithm to find frequent and generate assciation rules
mat_result=mat_result[ mat_result['item2']==frozenset({'Deviation__1'})].head(10) # filter the result related to 'Deviation__1'
mould_result=process_data.Apriori(data[mould_cloumns],minS=mins,minC=0.3).sort_values(['lift'], ascending=False)
mould_result=mould_result[ mould_result['item2']==frozenset({'Deviation__1'})].head(10)
tool_result=process_data.Apriori(data[tool_columns],minS=mins,minC=0.3).sort_values(['lift'], ascending=False)
tool_result=tool_result[tool_result['item2']==frozenset({'Deviation__1'})].head(10)

#out the result
mat_result.to_csv(dirf+'/result_data/mat_result.csv',index=False)
mould_result.to_csv(dirf+'/result_data/mould_result.csv',index=False)
tool_result.to_csv(dirf+'/result_data/tool_result.csv',index=False)