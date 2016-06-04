__author__ = 'zfh'

import cPickle
import numpy as np
from sklearn import svm, covariance
import matplotlib.pyplot as plt
import pandas as pd
import random
import utils
from mix1 import preprocess as pp
from copy import copy
from scipy.stats import uniform


def makeDataset(array, embedDim, interval, distance):
    array = np.array(array)
    subXSpan = (embedDim - 1) * (interval + 1) + 1
    datasetLength = array.shape[1] - (subXSpan + distance) + 1
    print datasetLength
    X = []
    y = []
    for i in range(datasetLength):
        subX = []
        for j in range(i, i + subXSpan, interval + 1):
            subX.extend(array[:, j])
        X.append(subX)
        y.append(array[:, i + subXSpan + distance - 1])
    # return np.array(X), np.array(y)
    return X, y


def makePredictset(array, embedDim, interval, distance):
    array = np.array(array)
    subXSpan = (embedDim - 1) * (interval + 1) + 1
    predictStart = array.shape[1] - (subXSpan + distance) + 1
    predictX = []
    for i in range(predictStart, predictStart + distance):
        subX = []
        for j in range(i, i + subXSpan, interval + 1):
            subX.extend(array[:, j])
        predictX.append(subX)
    return np.array(predictX)


def transform(array):
    result=[]
    for row in array:
        catRow=[]
        for item in row:
            catRow.extend(item)
        result.append(catRow)
    return result


def makeTrainset(array, embedDim, interval, distance):
    array = np.array(array)
    subXSpan = (embedDim - 1) * (interval + 1) + 1
    datasetLength = array.shape[1] - (subXSpan + distance) + 1
    X = []
    y = []
    for i in range(datasetLength):
        subX = []
        for j in range(i, i + subXSpan, interval + 1):
            subX.extend(array[:, j])
        X.append(subX)
        y.append(array[0, i + subXSpan:i + subXSpan + distance])
    return X, y


def makeXPredict(array, embedDim, interval):
    array = np.array(array)
    subXSpan = (embedDim - 1) * (interval + 1) + 1
    predictStart = array.shape[1] - subXSpan
    XPredict = []
    for i in range(predictStart, predictStart + subXSpan, interval+1):
        XPredict.extend(array[:, i])
    return XPredict

x = np.arange(183)
array = np.vstack((x, x + 100, x + 200))
# X,y= makeDataset(z, 7, 0, 2)
# Xpred=makePredictset(z,7,0,2)
# print np.array(X),np.array(y)
# print Xpred

# embedDim = 7
# interval = 0
# for i in range(1, 12):
#     XTrain, yTrain = pp.makeTrainset(z, embedDim, interval, i)
#     XPredict = pp.makeXPredict(z, embedDim, interval, i)
#     subyPredict = []
#     for j in range(len(yTrain[0])):
#         clf = svm.SVR()
#         clf.fit(XTrain, yTrain[:, j])
#         subyPredict.append(clf.predict(XPredict))
#     z=np.hstack((z, np.array(copy(subyPredict))))
# print z

# embedDim = 7
# interval = 0
# distance = 7
# for i in range(9):
#     XTrain, yTrain = pp.makeTrainset(array, embedDim, interval, distance)
#     XPredict = pp.makeXPredict(array, embedDim, interval, distance)
#     subyPredict = []
#     for j in range(len(yTrain[0])):
#         svr = svm.SVR()
#         svr.fit(XTrain, yTrain[:, j])
#         subyPredict.append(svr.predict(XPredict))
#     array = np.hstack((array, np.array(copy(subyPredict))))
# print array