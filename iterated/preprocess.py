__author__ = 'zfh'
# coding:utf-8

import os, utils
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def makeTrainset(array, embedDim, interval):  # 嵌入维度 间隔 预测距离=1
    distance = 1
    array = np.array(array)
    subXSpan = (embedDim - 1) * (interval + 1) + 1
    datasetLength = array.shape[1] - (subXSpan + distance) + 1
    X = []
    y = []
    for i in range(datasetLength):
        subX = []
        for j in range(i, i + subXSpan, interval + 1):
            subX.append(array[:, j])
        X.append(subX)
        y.append(array[:, i + subXSpan + distance - 1])
    return X, y


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


def split(array, testsize):
    train = array[:, :-testsize]
    test = array[:, -testsize:]
    return train, test


def makeDataArray(artist, song):
    songTrace = song.getTrace()
    songEA = song.getCumulateEA()
    songPercent = song.getPercentInSongs()
    artistEA = artist.getTotalCumulateEA()[song.getEmptyDays():]
    artistPercent = artist.getPercentInArtists()[:, song.getEmptyDays():]
    return np.vstack((songTrace, songEA, songPercent, artistEA, artistPercent))


def process(artist, song, embedDim, interval, testsize):
    array = makeDataArray(artist, song)
    array = movingAverage(array, 3)
    array, mean, var = uniform(array)  # 归一化
    # plotArray(array, song.getId())
    train, test = split(array, testsize)
    XTrain, yTrain = makeTrainset(train, embedDim, interval)
    yTest = test[0, :]
    return XTrain, yTrain, yTest, mean, var


def fprocess(artist, song, embedDim, interval):
    array = makeDataArray(artist, song)
    array = movingAverage(array, 3)
    array, mean, var = uniform(array)  # 归一化
    # plotArray(array, song.getId())
    XTrain, yTrain = makeTrainset(array, embedDim, interval)
    return XTrain, yTrain, mean, var


def plotArray(array, songId):
    savePath = os.path.join(utils.resultPath, 'song array')
    if not os.path.exists(savePath):
        os.makedirs(savePath)
    plt.figure(figsize=(8, 8))
    for i in range(array.shape[0]):
        plt.plot(array[i], label=str(i))
    plt.legend()
    plt.xlabel('days')
    plt.ylabel('counts')
    plt.savefig(os.path.join(savePath, songId + ".png"))
    plt.close()