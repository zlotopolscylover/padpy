#!/usr/bin/env python
# coding: utf-8

# In[1]:


import sklearn.ensemble
import sklearn.discriminant_analysis
from random import shuffle
import math
import knn
import numpy as np
import pandas as pd
import warnings
warnings.filterwarnings("ignore")


def parts(X):
    x = [i for i in range(len(X))]
    shuffle(x)
    indexes = [set(x[0:math.floor(len(x)/5)]),set(x[math.floor(len(x)/5):2*math.floor(len(x)/5)]), 
            set(x[2*math.floor(len(x)/5):3*math.floor(len(x)/5)]), set(x[3*math.floor(len(x)/5):4*math.floor(len(x)/5)]), 
            set(x[4*math.floor(len(x)/5):5*math.floor(len(x)/5)])]
    return indexes  

def zerolistmaker(n):
    listofzeros = [0] * n
    return listofzeros 

def crossvalidation(X, y, k):
    assert len(X) == len(y)
    indexes = parts(X)
    N = len(X)
    
    knn_Acc = zerolistmaker(5)
    RFC_Acc = zerolistmaker(5)
    LDA_Acc = zerolistmaker(5)
    Tree_Acc = zerolistmaker(5)
    for i in range(5):
        train_indexes = list(set(range(N)) - indexes[i])  
        test_indexes = list(indexes[i])
        X_train = [X[j] for j in train_indexes]
        y_train = [y[j] for j in train_indexes]
        X_test = [X[j] for j in test_indexes]
        y_test = [y[j] for j in test_indexes]
        
        knn_results = knn.knn(X_train, y_train, X_test, k)
        for l in range(len(y_test)):
            if y_test[l] == knn_results[l]:
                knn_Acc[i] += 1
        knn_Acc[i] = knn_Acc[i]/len(y_test)
        
        RFC = sklearn.ensemble.RandomForestClassifier()
        RFC.fit(X_train, y_train)
        RFC_Acc[i] = RFC.score(X_test, y_test)
        
        LDA = sklearn.discriminant_analysis.LinearDiscriminantAnalysis()
        LDA.fit(X_train, y_train)
        LDA_Acc[i] = LDA.score(X_test, y_test)
        
        Tree = sklearn.tree.DecisionTreeClassifier()
        Tree.fit(X_train, y_train)
        Tree_Acc[i] = Tree.score(X_test, y_test)
        
    return {"knn()": [np.mean(knn_Acc)], "Random Forests": [np.mean(RFC_Acc)], "LDA": [np.mean(LDA_Acc)], "Tree": [np.mean(Tree_Acc)]}

