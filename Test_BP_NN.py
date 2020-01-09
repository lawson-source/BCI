from sqlalchemy import create_engine
import matplotlib.pyplot as plt
import pandas as pd
import load_data as ld
from imblearn.over_sampling import RandomOverSampler
from sklearn import preprocessing
from keras.models import load_model
from sklearn.metrics import confusion_matrix
from sklearn.metrics import f1_score
import numpy as np
from keras import backend as K
def metric(y_true, y_pred):
    def negative_score(y_true, y_pred):

        flase_nagetive = K.sum(K.round(K.clip((1-y_true) * (1-y_pred), 0, 1)))
        flase = K.sum(K.round(K.clip(1-y_true, 0, 1)))
        negative_score = flase_nagetive / (flase + K.epsilon())
        return negative_score

    def positive_score(y_true, y_pred):

        true_positive = K.sum(K.round(K.clip(y_true * y_pred, 0, 1)))
        true = K.sum(K.round(K.clip(y_true, 0, 1)))
        positive_score = true_positive / (true + K.epsilon())
        return positive_score
    positive_score = positive_score(y_true, y_pred)
    negative_score = negative_score(y_true, y_pred)
    return 2*((positive_score*negative_score)/(negative_score+positive_score+K.epsilon()))

def String2Num(data,column,label):
    proba=(data.groupby(column)[[label]].sum())[label]/data.groupby(column)[[column]].size()
    return proba
def data_processiug(data):
    # data.loc[data.Deviation < 0.5, 'Deviation'] = 0
    # data.loc[data.Deviation >= 0.5, 'Deviation'] = 1
    proba = pd.read_csv('proability.csv', )
    for column in data.columns[0:17]:
        data[column] = column + '__' + data[column]
        data[column] = data[column].replace(proba['index'].values, proba['value'].values)
        data[column] = data[column].transform(lambda x : (x-x.mean())/(x.std()+K.epsilon()))

    #
    xdata = data[data.columns[0:17]]
    ydata = data['Deviation']
    xdata = preprocessing.scale(xdata)
    return xdata,ydata

def loss(y_true,y_pred):
    return K.mean(((y_true-1)*K.log(1-y_pred+K.epsilon())-y_true*1000*K.log(y_pred+K.epsilon())),axis=-1)

def model_load(xdata,ydata):
    model = load_model('BPNN_model2.h5' )
    yp = model.predict(xdata).reshape(len(ydata))
    yp=yp*(0.052++K.epsilon())+0.039
    return yp



def main():
    data = ld.load_data().load_data().sample(n=10000,axis=0)
    xdata, ydata = data_processiug(data)
    yp=model_load(xdata,ydata)
    yp=(yp>0.5).astype('int')
    # fig = plt.figure()
    # ax = fig.add_subplot(1, 1, 1)
    # ax.plot(range(0,yp.size), yp-ydata, color='tab:blue')
    # plt.show()
    matrix=confusion_matrix(((ydata>0.5).astype('int')), yp)
    print(matrix)
    pre_score=matrix[1,1]/(matrix[1,1]+matrix[1,0])
    ture_score=matrix[0,0]/(matrix[0,1]+matrix[0,0])
    score=2*pre_score*ture_score/(pre_score+ture_score)
    print(score)
    print(f1_score((ydata>0.5).astype('int'), yp, pos_label=0))

main()