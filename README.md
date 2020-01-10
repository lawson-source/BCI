# BCI
code in BCI
## Repositories URL 
BOSCH Python Repositories: https://anu9rng:AP6eY5xuhS1MqAdy5jedftw3ndQq7MHjXL8Rpb@rb-artifactory.bosch.com/artifactory/api/pypi/python-virtual/simple/  

BOSCH Angular NPM Repositories:https://rb-artifactory.bosch.com/artifactory/webapp/#/artifacts/browse/tree/General/bci-npm-virtual  
 
## Naive Bayesian Model
Naive presents factors are independence for each other

![](http://latex.codecogs.com/gif.latex?P(Y|X)=\frac{P(X|Y)*P(Y)}{P(X)})

where Y represents labels, X represents factor.

![](http://latex.codecogs.com/gif.latex?P(Y|X_1,X_2,...,X_n)=\frac{P(X_1,X_2,...,X_n|Y)*P(Y)}{P(X_1,X_2,...,X_n)}=\frac{P(X_1|Y)*P(X_2|Y)*...*P(X_n|Y)*P(Y)}{P(X_1)*P(X_2)*...*P(X_n)})

where X1, X2, ... , Xn represent varies of factors values.

the probability of prediction:

![](http://latex.codecogs.com/gif.latex?P(Y_1)=\frac{P(Y_1|X_1,X_2,...,X_n)}{P(Y_1|X_1,X_2,...,X_n)+P(Y_0|X_1,X_2,...,X_n)})

or

we can also set the max(p(Y1|X1,X2,.......,Xn), p(Y2X1,X2,.......,Xn)) value as the probability.
## Development of Program
Hyperparams:
num_neurons:the number of neuons
Dropout:A Simple Way to Prevent Neural Networks from Overfitting.
Activations: Relu was choosen as activaions.
Softmoid: It can transIform continuous-valued to between 0 and 1,but the gradient may be missed with  iteration increase. Hence, it  is seldom used.
Hyperbolic Tangent (tanh): Its put value is zero-centered, but the problem of gradient missing is still exist.
Relu: It is a Maximum function and the most popular activation.
Elu: It is similar with the Relu, but speend more computational cost.
loss:
 mean_squared_error：
 
![](http://latex.codecogs.com/gif.latex?Erro=\frac{\sum_{k=1}^N(y_{pred}-y_{true})^2}{N}) 

mean_absolute_error:

![](http://latex.codecogs.com/gif.latex?Erro=\frac{\sum_{k=1}^N\left|(y_{pred}-y_{true})\right|}{N})

 mean_absolute_percentage_error  

binary_crossentropy: binary cross entropy loss function  

categorical_crossentropy  

User-defined: binary_crossentropy (unbalanced data)  

the loss function increase weight of less sample to the gradient of loss function incline less sample under the situation of unbalanced samples between positive and negative.   

```
def loss(y_true,y_pred):
   return K.mean(((y_true-1)*K.log(1-y_pred+K.epsilon())-y_true*500*K.log(y_pred+K.epsilon())),axis=-1)
```
optimizer:
adam

metric:


Positive	Negative 

True	TP	FN
Flase	FP	TN

Positive_Score=TP/（FP+TN）Negtive_Score=TN/(TN+FP)

Metric_Score=2*Negtive_Score*Positive_Score/（Negtive_Score+Positive_Score）
