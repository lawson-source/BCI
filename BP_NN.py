from sqlalchemy import create_engine
import pandas as pd
import load_data as ld
from imblearn.over_sampling import RandomOverSampler
from keras.models import Sequential
from keras import layers
from keras.layers.core import Dense
from sklearn.model_selection import GridSearchCV
from keras.wrappers import scikit_learn
from sklearn import preprocessing
from sklearn.model_selection import train_test_split
from keras import backend as K
from keras import regularizers
from hyperopt import hp, fmin, rand, tpe, space_eval,STATUS_OK
from hyperopt import Trials
import csv
import numpy as np

def mean_squared_error(y_true, y_pred):
    return K.mean(K.square(10*(y_pred - y_true)), axis=-1)
def metric(y_true, y_pred):
    def negative_score(y_true, y_pred):
        flase_nagetive = K.sum(y_true * y_pred)
        flase = K.sum(y_true)
        negative_score = flase_nagetive / (flase + K.epsilon())
        return negative_score

    def positive_score(y_true, y_pred):
        true_positive = K.sum((1-y_true) * (1-y_pred))
        true = K.sum(1-y_true)
        positive_score = true_positive / (true + K.epsilon())
        return positive_score
    positive_score = positive_score(y_true, y_pred)
    negative_score = negative_score(y_true, y_pred)
    return 2*((positive_score*negative_score)/(negative_score+positive_score+K.epsilon()))

def loss(y_true,y_pred):
    return K.mean(((y_true-1)*K.log(1-y_pred+K.epsilon())-y_true*50*K.log(y_pred+K.epsilon())),axis=-1)

def create_model(*args,**kwargs):
    num_neurons_1st=int(kwargs['num_neurons_1st'])
    num_neurons_2nd=int(kwargs['num_neurons_2nd'])
    num_neurons_3rd=int(kwargs['num_neurons_3rd'])
    drop_ratio_1st=kwargs['drop_ratio_1st']
    drop_ratio_2nd=kwargs['drop_ratio_2nd']
    model = Sequential()
    model.add(Dense(num_neurons_1st, activation='relu', kernel_initializer='he_normal', input_shape=(17,)))
    model.add(layers.Dropout(drop_ratio_1st))
    model.add(Dense(num_neurons_2nd, activation='relu', kernel_initializer='he_normal', ))
    model.add(layers.Dropout(drop_ratio_2nd))
    model.add(Dense(num_neurons_3rd, activation='relu', kernel_initializer='he_normal', ))
    model.add(Dense(1,))
    model.compile(loss='mse', optimizer='adam', metrics=['mae'])
    return model

def String2Num(data,column,label):
    proba=(data.groupby(column)[[label]].mean())[label]
    return proba
def model_find_hyperparm(data,targets):
    model = scikit_learn.KerasClassifier(batch_size=20, build_fn=create_model, epochs=5, verbose=0)
    param_grid = dict(num_neurons2=[300,200],num_neurons4=[100,50])
    grid = GridSearchCV(estimator=model, param_grid=param_grid, n_jobs=4, scoring='metric',cv=5)
    grid_result = grid.fit(data, targets)
    print('Best: {} using {}'.format(grid_result.best_score_, grid_result.best_params_))
    means = grid_result.cv_results_['mean_test_score']
    stds = grid_result.cv_results_['std_test_score']
    params = grid_result.cv_results_['params']

    for mean, std, param in zip(means, stds, params):
        print("%f (%f) with: %r" % (mean, std, param))

def model_find_hyperparm_Bayesian(xdata, ydata):
    train_data, test_data, train_targets, test_targets = train_test_split(xdata, ydata, random_state=0,
                                                                          test_size=0.25)
    def objective(params):
        batch_size = int(params['batch_size'])
        model=create_model(**params)
        model.fit(train_data, train_targets, epochs=10, batch_size=batch_size )
        loss, PN = model.evaluate(test_data, test_targets)
        PN=1-PN
        of_connection = open(out_file, 'a')
        writer = csv.writer(of_connection)
        writer.writerow([loss,PN, params,])
        of_connection.close()
        print("loss is %f SCORE—— is %f" % (loss,PN))
        return {'loss':loss,'PN':PN,'params': params,'status':STATUS_OK}

    bayes_trials = Trials()
    out_file = 'bp_trials.csv'
    of_connection = open(out_file, 'w')
    writer = csv.writer(of_connection)
    # Write the headers to the file
    writer.writerow(['loss', 'PN','params', ])
    of_connection.close()
    domain={'num_neurons_1st':hp.choice('num_neurons_1st',range(50,300,10)),'num_neurons_2nd':hp.quniform('num_neurons_2nd',20,200,10),'num_neurons_3rd':hp.quniform('num_neurons_3rd',20,100,10),
            'drop_ratio_1st':hp.uniform('drop_ratio_1st',0.1,0.9),'drop_ratio_2nd':hp.uniform('drop_ratio_2nd',0.1,0.9),'batch_size':hp.quniform('batch_size',20,200,10)}
    algo = tpe.suggest
    best=fmin(objective,domain,algo=algo,trials = bayes_trials,max_evals=30)

    print(space_eval(domain,best))


def model_train(xdata,ydata):
    train_data, test_data, train_targets, test_targets = train_test_split(xdata, ydata, random_state=0,
                                                                          test_size=0.25)
    model = create_model(**{'drop_ratio_1st': 0.1, 'drop_ratio_2nd': 0.1, 'num_neurons_1st': 130, 'num_neurons_2nd': 160, 'num_neurons_3rd': 70})
    model.fit(train_data, train_targets, epochs=500,batch_size=50 )
    loss, f1 = model.evaluate(test_data, test_targets)
    print("loss is %f f1—— is %f" % (loss, f1))
    print("Saving model to disk \n")
    mp = "BPNN_model2.h5"
    model.save(mp)

def data_processiug(data):
    data.loc[data.Deviation < 0.5, 'Deviation1'] = 0
    data.loc[data.Deviation >= 0.5, 'Deviation1'] = 1

    proability = pd.DataFrame()
    for column in data.columns[0:17]:
        data[column] = column + '__' + data[column]
        proba = String2Num(data, column, 'Deviation1')
        proability = pd.concat([proability, proba], axis=0)
        data[column] = data[column].replace(proba.index, proba)
        data[column] = data[column].transform(lambda x : (x-x.mean())/x.std())

    #
    xdata = data[data.columns[0:17]]
    ydata =data['Deviation']
    ydata = (ydata-ydata.mean())/ydata.std()


    # #Sampling by RandomUnderSample
    # model_RandomoverSample = RandomOverSampler(ratio=1)
    # xdata, ydata = model_RandomoverSample.fit_sample(xdata, ydata)
    return xdata,ydata

def main():
    data = ld.load_data().load_data().head(50000)
    xdata,ydata=data_processiug(data)
    model_train(xdata,ydata)
    # model_find_hyperparm_Bayesian(xdata,ydata)

main()









