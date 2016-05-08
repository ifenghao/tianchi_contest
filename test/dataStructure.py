__author__ = 'zfh'

import cPickle
import numpy as np
from sklearn import svm,covariance
import matplotlib.pyplot as plt
import pandas as pd
import random


def makeDataset(array, embedDim,interval,distance):
    array = np.array(array)
    subXSpan=(embedDim-1)*(interval+1)+1
    datasetLength=array.shape[1]-(subXSpan+distance)+1
    print datasetLength
    X = []
    y = []
    for i in range(datasetLength):
        subX=[]
        for j in range(i,i+subXSpan,interval+1):
            subX.extend(array[:,j])
        X.append(subX)
        y.append(array[0,i+subXSpan+distance-1])
    return np.array(X), np.array(y)


def makePredictset(array, embedDim, interval, distance):
    array = np.array(array)
    subXSpan = (embedDim - 1) * (interval + 1) + 1
    predictStart = array.shape[1] - (subXSpan + distance) + 1
    predictX = []
    for i in range(predictStart,predictStart+distance):
        subX = []
        for j in range(i, i + subXSpan, interval + 1):
            subX.extend(array[:, j])
        predictX.append(subX)
    return np.array(predictX)

x=np.arange(135)
z=np.vstack((x,x+100,x+200))
print makeDataset(z,3,1,48)
print makePredictset(z,3,1,48)