__author__ = 'zfh'
# coding:utf-8

from multiprocessing import Pool

import os
import cPickle
import warnings
import time
from copy import copy

import matplotlib.pyplot as plt
import numpy as np

import utils
import preprocess as pp
import erfModel, gbrtModel, svrModel
from iterated import preprocess as iterpp
from iterated import gbrtModel as itergbrtModel
from iterated import erfModel as itererfModel

now = time.strftime('%Y%m%d', time.localtime(time.time()))
finalResultPath = os.path.join(utils.allResultPath, 'finalout' + now)


def plotResult(yPredict3, yPredict4):
    # p1tag = plt.plot(yPredict1, 'bo', yPredict1, 'b-')
    # p2tag = plt.plot(yPredict2, 'go', yPredict2, 'g-')
    p3tag = plt.plot(yPredict3, 'co', yPredict3, 'c-')
    p4tag = plt.plot(yPredict4, 'yo', yPredict4, 'y-')
    plt.legend([p3tag[1], p4tag[1]],
               ['gbrt', 'erf'])
    plt.xlabel('test days')
    plt.ylabel('counts')


def writecsv(finalResultFile, artistId, yPredictSum):
    with open(finalResultFile, 'a') as file:
        for num in range(len(yPredictSum)):
            file.write(','.join([artistId, str(int(round(yPredictSum[num]))), utils.num2date(num)]) + '\n')


def genModel(artist, song, model, embedDim, interval):
    array, mean, var = pp.fprocess(artist, song)
    yPredict = model.train(array, embedDim, interval)
    yPredict = yPredict * var + mean
    yPredict[yPredict < 0] = 0  # 预测值出现负数直接归零
    return yPredict


def itergenModel(artist, song, model, embedDim, interval, testsize):
    XTrain, yTrain, mean, var = iterpp.fprocess(artist, song, embedDim, interval)
    yPredict = model.train(XTrain, yTrain, testsize)
    yPredict = yPredict * var + mean
    yPredict[yPredict < 0] = 0  # 预测值出现负数直接归零
    return yPredict


def fout(dict, embedDim, interval, distance):
    print 'Run task %s...' % (os.getpid(),)
    plt.figure(figsize=(6, 4))
    artistNum = 0
    for artistId, artist in dict.items():
        artistNum += 1
        print artistNum
        savePath = os.path.join(utils.resultPath, artistId)
        if not os.path.exists(savePath):
            os.makedirs(savePath)
        # yPredictSum1 = np.zeros(testsize)
        # yPredictSum2 = np.zeros(distance)
        yPredictSum3 = np.zeros(distance)
        yPredictSum4 = np.zeros(distance)
        for songId, song in artist.getSongsOwned().items():
            traceLength = np.array(song.getTrace()).shape[1]
            trainLength = pp.XTrainLength(traceLength, embedDim, interval, 7)  # 训练集长度
            if trainLength < 10:  # 训练集长度不足10的歌曲
                print 'iterated ' + str(traceLength) + ' ' + str(trainLength)
                # # SVR模型
                # yPredict1 = genModel(artist, song, svrModel, embedDim, interval)
                # # 随机森林模型
                # yPredict2 = genModel(artist, song, rfModel, embedDim, interval, distance)
                # GBRT模型
                yPredict3 = itergenModel(artist, song, itergbrtModel, embedDim, interval, distance)
                # 完全随机森林模型
                yPredict4 = itergenModel(artist, song, itererfModel, embedDim, interval, distance)
            else:
                print 'mix2 ' + str(traceLength) + ' ' + str(trainLength)
                # # SVR模型
                # yPredict1 = genModel(artist, song, svrModel, embedDim, interval)
                # # 随机森林模型
                # yPredict2 = genModel(artist, song, rfModel, embedDim, interval, distance)
                # GBRT模型
                yPredict3 = genModel(artist, song, gbrtModel, embedDim, interval)
                # 完全随机森林模型
                yPredict4 = genModel(artist, song, erfModel, embedDim, interval)
            plotResult(yPredict3, yPredict4)
            plt.savefig(os.path.join(savePath, 'song ' + songId + ".png"))
            plt.clf()
            # yPredictSum1 += yPredict1
            # yPredictSum2 += yPredict2
            yPredictSum3 += yPredict3
            yPredictSum4 += yPredict4
        plotResult(yPredictSum3, yPredictSum4)
        plt.savefig(os.path.join(savePath, 'artist ' + artistId + ".png"))
        plt.clf()
        # finalResultFile1 = os.path.join(finalResultPath, 'svr.csv')
        # writecsv(finalResultFile1, artistId, yPredictSum1)
        # finalResultFile2 = os.path.join(finalResultPath, 'rf.csv')
        # writecsv(finalResultFile2, artistId, yPredictSum2)
        finalResultFile3 = os.path.join(finalResultPath, 'gbrt.csv')
        writecsv(finalResultFile3, artistId, yPredictSum3)
        finalResultFile4 = os.path.join(finalResultPath, 'erf.csv')
        writecsv(finalResultFile4, artistId, yPredictSum4)


if __name__ == '__main__':
    print 'Parent process %s.' % os.getpid()
    artistObjectFile = os.path.join(utils.allResultPath, 'artistsObjectDict.pkl')
    artistsObjectDict = cPickle.load(open(artistObjectFile, 'r'))
    list = []
    dict = {}
    for artistId, artist in artistsObjectDict.items():
        if len(dict) < 13:
            dict[artistId] = artist
        else:
            list.append(copy(dict))
            dict = {}
            dict[artistId] = artist
    list.append(dict)
    warnings.filterwarnings("ignore")
    if not os.path.exists(utils.resultPath):
        os.makedirs(utils.resultPath)
    if not os.path.exists(finalResultPath):
        os.makedirs(finalResultPath)
    distance = 60
    embedDim = 7
    interval = 0
    p = Pool()
    for dict in list:
        p.apply_async(fout, args=(dict, embedDim, interval, distance))
    print 'Waiting for all subprocesses done...'
    p.close()
    p.join()
    print 'All subprocesses done.'
