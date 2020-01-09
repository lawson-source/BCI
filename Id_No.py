import  pandas as pd
import os
# sort data in descend order by the value of Deviation, then keep first record  and delete the duplicate data of Ident_NO
columns =['Ident No.','Deviation',
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
                'Moulding.toolData[6].toolID', 'Moulding.toolData[7].toolID',]
File_dir = './data'
Filelist = os.listdir(File_dir)
data = pd.read_csv(File_dir + '/' + Filelist[0])
data=data[columns]
data=data.drop_duplicates()

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
print(data.shape)
data.to_csv('./result_data/Ident_No.csv')
print(data.shape)
