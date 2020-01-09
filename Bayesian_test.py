from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split
from sqlalchemy import create_engine
from imblearn.under_sampling import RandomUnderSampler
import pandas as pd
from sklearn.externals import joblib
import numpy as np

# find uniques in data source
def createlist (dataset) :
    vocabSet = set([])
    for document in dataset:
        vocabSet = vocabSet | set(document)
    return list(vocabSet)

# transform data to vector quantity
def changeword2vec (inputdata, wordlist) :
    returnVecs=[]
    for words in inputdata :
        returnVec = [0] * len(wordlist)
        for word in words:
         if word in wordlist :
            returnVec[wordlist.index(word)] = 1
        returnVecs.append(returnVec)
    return returnVecs

# columns for analysis
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

# load data from MySQL
sql='SELECT * FROM dataunique WHERE `Production Date`>\'2019-08-01\' AND `Production Date`<\'2019-09-31\''
engine=create_engine("mysql+pymysql://root:yuan20112@localhost/wujin?charset=UTF8MB4")
data=pd.read_sql(sql,engine)
data=data[columns].dropna()
data=data.groupby(columns2).mean().reset_index()


# transform Deviation to label
data.loc[data.Deviation<0.5,'Deviation']=0
data.loc[data.Deviation>=0.5,'Deviation']=1

#
xdata=data[columns2]
for column in columns2:
    xdata[column] = column + '__' + xdata[column]
ydata=data['Deviation'].astype('int')
wordlist=np.load('wordlist3.npy', allow_pickle=True).item()
wordlist=wordlist['wordlist']
xdata=changeword2vec(xdata.values,wordlist) # transform xdata to vector quantity

RF=joblib.load('Bayesian_train_model3.m')
y_predict=RF.predict(xdata)
y_pro=RF.predict_proba(xdata)
print(RF.score(xdata,ydata))
from sklearn.metrics import confusion_matrix
print(confusion_matrix(ydata, y_predict))
a=(ydata==1 )&(y_predict==0)

print()
