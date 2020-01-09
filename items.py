import  pandas as pd
import os
# count unique value
dirf=os.path.abspath(os.path.dirname(__file__))
columns =[
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
File_dir = dirf+'/data'
Filelist = os.listdir(File_dir)
data = pd.read_csv(File_dir + '/' + Filelist[0],dtype=object)
data=data[columns]
data=data.drop_duplicates()

for i in range(1, len(Filelist)):
        print(Filelist[i])
        if Filelist[i] == ".DS_Store":
            continue
        df = pd.read_csv(File_dir + '/' + Filelist[i],dtype=object)
        df=df[columns]
        data = data.append(df, ignore_index=True)
        data = data.dropna()
        data = data.drop_duplicates()

data=data.drop_duplicates()
data.to_csv(dirf+'/result_data/items.csv',index=False)
