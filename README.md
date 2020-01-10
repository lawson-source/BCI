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
