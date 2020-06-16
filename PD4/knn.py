#!/usr/bin/env python
# coding: utf-8

# In[2]:


import numpy as np
from collections import Counter
import random

def knn(X, y, Z, k):
    assert len(X) == len(y)
    result = []
    yX = list(zip(y, X))
    for i in range(len(Z)):
        merged = sorted(yX, key = lambda x: np.linalg.norm(np.array(x[1]) - np.array(Z[i]))) 
        labels = Counter([j[0] for j in merged[:k]]).most_common() 
        values = [j[0] for j in labels if j[1] == max([j[1] for j in labels]) ] 
        random.shuffle(values) 
        result.append(values[0])
    return result

