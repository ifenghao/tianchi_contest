__author__ = 'zfh'
# coding:utf-8

import numpy as np
import pandas as pd


def makeTrainset(array, embedDim, interval, distance):  # 嵌入维度 间隔 预测距离
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
        y.append(array[0, i + subXSpan + distance - 1])
    return X, y


def makeXPredict(array, embedDim, interval, distance):
    array = np.array(array)
    subXSpan = (embedDim - 1) * (interval + 1) + 1
    predictStart = array.shape[1] - (subXSpan + distance) + 1
    XPredict = []
    for i in range(predictStart, predictStart + distance):
        subX = []
        for j in range(i, i + subXSpan, interval + 1):
            subX.extend(array[:, j])
        XPredict.append(subX)
    return XPredict


def movingAverage(array, span):
    array = np.array(array, dtype=float)
    result = []
    for row in array:
        row = pd.Series(row)
        row = pd.ewma(row, span=span)
        row = np.array(row)
        rowmean = np.mean(row)
        rowvar = np.var(row)
        prob = 1 / (np.sqrt(2 * np.pi * rowvar)) * np.exp(-(row - rowmean) ** 2 / (2 * rowvar))
        outliers = np.where(prob < 1e-18)
        smoothOutliers(row, outliers, 3)
        result.append(row)
    return np.array(result)


def smoothOutliers(rowdata, outliers, winsize):
    halfsize = winsize // 2
    length = len(rowdata)
    for i in outliers[0]:
        window = []
        if i < halfsize:
            for j in range(-i, halfsize + 1):
                window.append(rowdata[i + j])
        elif i > length - 1 - halfsize:
            for j in range(-halfsize, length - i):
                window.append(rowdata[i + j])
        else:
            for j in range(-halfsize, halfsize + 1):
                window.append(rowdata[i + j])
        windowmean = np.mean(window)
        rowdata[i] = windowmean


def uniform(array):
    array = np.array(array, dtype=float)
    mean = np.mean(array, axis=1)
    std = np.std(array, axis=1)
    result = []
    for row, rowmean, rowstd in zip(array, mean, std):
        result.append((row - rowmean) / rowstd)
    result = np.array(result)
    result[np.isnan(result)] = 0
    result[np.isinf(result)] = 0
    return result, mean[0], std[0]


def split(array, trainLength):
    train = array[:, :trainLength]
    test = array[:, trainLength:]
    return train, test


def makeDataArray(artist, song):
    songTrace = song.getTrace()
    songPercent = song.getPercentInSongs()
    artistPercent = artist.getPercentInArtists()
    return np.vstack((songTrace, songPercent, artistPercent))


def process(artist, song, trainLen, embedDim, interval, distance):
    array = makeDataArray(artist, song)
    array = movingAverage(array, 3)
    array, mean, var = uniform(array)  # 归一化
    train, test = split(array, trainLen)
    XTrain, yTrain = makeTrainset(train, embedDim, interval, distance)
    XPredict = makeXPredict(train, embedDim, interval, distance)
    yTest = test[0, :]
    return XTrain, yTrain, XPredict, yTest, mean, var
