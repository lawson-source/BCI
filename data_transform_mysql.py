

import os
import pandas as pd
import sqlalchemy
from sqlalchemy import create_engine

types={'Ident No.':sqlalchemy.types.VARCHAR(255),'X':sqlalchemy.types.Float,'∆X':sqlalchemy.types.Float,
'Y':sqlalchemy.types.Float,'∆Y':sqlalchemy.types.Float,'Deviation':sqlalchemy.types.Float,'PinCharacteristic':sqlalchemy.types.VARCHAR(255),
       'matDataBComponents[1].matID':sqlalchemy.types.VARCHAR(255), 'matDataBComponents[1].batch':sqlalchemy.types.VARCHAR(255),
      'matDataBComponents[1].typeNo':sqlalchemy.types.VARCHAR(255), 'matDataBComponents[1].vendor':sqlalchemy.types.VARCHAR(255),
      'toolData[1].toolID':sqlalchemy.types.VARCHAR(255), 'toolData[2].toolID':sqlalchemy.types.VARCHAR(255), 'toolData[12].toolID':sqlalchemy.types.VARCHAR(255),
      'toolData[13].toolID':sqlalchemy.types.VARCHAR(255), 'matDataBComponents[2].matID':sqlalchemy.types.VARCHAR(255),
      'matDataBComponents[2].batch':sqlalchemy.types.VARCHAR(255), 'matDataBComponents[2].typeNo':sqlalchemy.types.VARCHAR(255),
      'matDataBComponents[2].vendor':sqlalchemy.types.VARCHAR(255), 'matDataBComponents[3].matID':sqlalchemy.types.VARCHAR(255),
      'matDataBComponents[3].batch':sqlalchemy.types.VARCHAR(255), 'matDataBComponents[3].typeNo':sqlalchemy.types.VARCHAR(255),
      'matDataBComponents[3].vendor':sqlalchemy.types.VARCHAR(255), 'matDataBComponents[4].matID':sqlalchemy.types.VARCHAR(255),
      'matDataBComponents[4].batch':sqlalchemy.types.VARCHAR(255), 'matDataBComponents[4].typeNo':sqlalchemy.types.VARCHAR(255),
      'matDataBComponents[4].vendor':sqlalchemy.types.VARCHAR(255), 'Moulding.toolData[1].toolID':sqlalchemy.types.VARCHAR(255),
      'Moulding.toolData[2].toolID':sqlalchemy.types.VARCHAR(255), 'Moulding.toolData[3].toolID':sqlalchemy.types.VARCHAR(255),
      'Moulding.toolData[4].toolID':sqlalchemy.types.VARCHAR(255), 'Moulding.toolData[5].toolID':sqlalchemy.types.VARCHAR(255),
      'Moulding.toolData[6].toolID':sqlalchemy.types.VARCHAR(255), 'Moulding.toolData[7].toolID':sqlalchemy.types.VARCHAR(255),
      'Moulding.matData[1].matID':sqlalchemy.types.VARCHAR(255), 'MouldMachineNo':sqlalchemy.types.VARCHAR(255), 'MouldNestNo':sqlalchemy.types.VARCHAR(255),
      'TablePosition':sqlalchemy.types.VARCHAR(255),'Production Date':sqlalchemy.types.VARCHAR(255),'HV.Test.toolData[1].toolID':sqlalchemy.types.VARCHAR(255),
      'HV.Test.toolData[2].toolID':sqlalchemy.types.VARCHAR(255)}
engine=create_engine("mysql+pymysql://root:yuan20112@localhost/wujin?charset=utf8")
dirf=os.path.abspath(os.path.dirname(__file__)) # root directory
File_dir =dirf+'/data' # directory of data source
Filelist = os.listdir(File_dir) # all of file name of data source
for i in range(0, len(Filelist)):
        if Filelist[i] == ".DS_Store":
            continue
        print(i,Filelist[i]+'--start')
        data = pd.read_csv(File_dir + '/' + Filelist[i])
        data = data.dropna()
        data = data.sort_values('Deviation', ascending=False)
        data = data.drop_duplicates('Ident No.', keep='first')
        data.to_sql('dataunique',engine,schema='wujin',chunksize=100,if_exists='append',index=False,index_label=False,method='multi',dtype=types)
        print(i,  Filelist[i] + '--end')
