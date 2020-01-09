from sklearn.naive_bayes import BernoulliNB
from sklearn.model_selection import train_test_split
from sklearn.externals import joblib
import numpy as np
import load_data as ld


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

# transform Deviation to label
def processing_data(data):
    data.loc[data.Deviation < 0.5, 'Deviation'] = 0
    data.loc[data.Deviation >= 0.5, 'Deviation'] = 1
    xdata = data.ix[:, 1:19]
    ydata = data['Deviation'].astype('int')
    for column in xdata.column:
        xdata[column] = column + '__' + xdata[column]
        return xdata,ydata
def main():
    data = ld.load_data().load_data()
    xdata, ydata = process_data(data)
    wordlist = createlist(xdata.values)  # find uniques from data
    xdata = changeword2vec(xdata.values, wordlist)  # transform xdata to vector quantity

    # # Sampling by RandomUnderSample
    # model_RandomoverSample = RandomOverSampler(ratio=0.02)
    # xdata,ydata=model_RandomoverSample.fit_sample(xdata, ydata)

    Xtrain, Xtest, ytrain, ytest = train_test_split(xdata, ydata, test_size=0.25)  # split data to train and test

    cls = BernoulliNB()  # instantiate  Bayesian model
    cls.fit(Xtrain, ytrain, sample_weight=[10])  # train model
    # save model
    joblib.dump(cls, "Bayesian_train_model3.m")
    wordlist = dict({'wordlist': wordlist})
    np.save('wordlist3.npy', wordlist)
    print('Training Score:%.2f' % cls.score(Xtrain, ytrain))
    print('Testing Score:%.2f' % cls.score(Xtest, ytest))
    y_predict = cls.predict(Xtest)
    from sklearn.metrics import confusion_matrix
    print(confusion_matrix(ytest, y_predict))
if __name__ == '__main__':
    main()


