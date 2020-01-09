from sqlalchemy import create_engine
import pandas as pd
from imblearn.over_sampling import RandomOverSampler


columns =[
          'Deviation','matDataBComponents[1].vendor','matDataBComponents[2].vendor', 'matDataBComponents[3].vendor',
          'matDataBComponents[4].vendor', 'toolData[1].toolID','toolData[12].toolID', 'toolData[2].toolID',
          'MouldMachineNo','MouldNestNo', 'TablePosition', 'Moulding.toolData[1].toolID','Moulding.toolData[2].toolID',
          'Moulding.toolData[3].toolID','Moulding.toolData[4].toolID', 'Moulding.toolData[5].toolID',
          'Moulding.toolData[6].toolID', 'Moulding.toolData[7].toolID'
          ]
columns2= ['matDataBComponents[1].vendor','matDataBComponents[2].vendor', 'matDataBComponents[3].vendor',
             'matDataBComponents[4].vendor', 'toolData[1].toolID','toolData[12].toolID', 'toolData[2].toolID',
             'MouldMachineNo','MouldNestNo', 'TablePosition', 'Moulding.toolData[1].toolID','Moulding.toolData[2].toolID',
             'Moulding.toolData[3].toolID','Moulding.toolData[4].toolID', 'Moulding.toolData[5].toolID',
             'Moulding.toolData[6].toolID', 'Moulding.toolData[7].toolID'
            ]
def String2Num(data,column,label):
    proba=(data.groupby(column)[[label]].sum())[label]/data.groupby(column)[[column]].size()
    return proba

# load data from MySQL
sql='SELECT * FROM data WHERE `Production Date`>\'2019-03-01\' AND `Production Date`<\'2019-09-31\' '
engine=create_engine("mysql+pymysql://root:yuan20112@localhost/wujin?charset=UTF8MB4")
data=pd.read_sql(sql,engine)
data=data[columns].dropna()

# transform Deviation to label
data.loc[data.Deviation<0.5,'Deviation']=0
data.loc[data.Deviation>=0.5,'Deviation']=1

proability=pd.DataFrame()
for column in columns2:
    proba=String2Num(data,column,'Deviation')
    proability=pd.concat([proability,proba],axis=0)
    data[column]=data[column].replace(proba.index,proba)
proability.to_csv('proability.csv')
#
xdata=data[columns2]
ydata=data['Deviation'].astype('int')

from sklearn.model_selection import train_test_split
partial_train_data, val_data,partial_train_targets, val_targets = train_test_split(xdata, ydata, random_state=0,test_size=0.2)

from sklearn.ensemble import GradientBoostingClassifier
clf=RF(class_weight='balanced')
clf.fit(partial_train_data,partial_train_targets)
print('Training Score:%.2f'%clf.score(partial_train_data,partial_train_targets))
print('Testing Score:%.2f'%clf.score(val_data,val_targets))
y_predict=clf.predict(val_data)
from sklearn.metrics import confusion_matrix
print(confusion_matrix(val_targets, y_predict))