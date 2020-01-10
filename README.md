# BCI
code in BCI
##Repositories URL 
BOSCH Python Repositories: https://anu9rng:AP6eY5xuhS1MqAdy5jedftw3ndQq7MHjXL8Rpb@rb-artifactory.bosch.com/artifactory/api/pypi/python-virtual/simple/  

BOSCH Angular NPM Repositories:https://rb-artifactory.bosch.com/artifactory/webapp/#/artifacts/browse/tree/General/bci-npm-virtual  
 
##Naive Bayesian Model
Naive presents factors are independence for each other

P(Y|X)=P(X|Y)∗P(Y)P(X)

where Y represents labels, X represents factor.

P(Y|X1,X2,...,Xn)=P(X1,X2,...,Xn|Y)∗P(Y)P(X1,X2,...,Xn)=P(X1|Y)∗P(X2|Y)∗...∗P(Xn|Y)∗P(Y)P(X1)∗P(X2)∗...∗P(Xn)

where X1, X2, ... , Xn represent varies of factors values.

the probability of prediction:

P(Y1)=P(Y1|X1,X2,...,Xn)P(Y1|X1,X2,...,Xn)+P(Y0|X1,X2,...,Xn)

or

we can also set the max(p(Y1|X1,X2,.......,Xn), p(Y2X1,X2,.......,Xn)) value as the probability.
