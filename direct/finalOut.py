__author__ = 'zfh'
# coding:utf-8

import os
import cPickle
import warnings

import matplotlib.pyplot as plt
import numpy as np

import utils
import preprocess as pp
import erfModel, gbrtModel, xgbModel
from iterated import preprocess as iterpp
from iterated import xgbModel as iterxgbModel
from iterated import gbrtModel as itergbrtModel
from iterated import erfModel as itererfModel

finalResultPath = os.path.join(utils.allResultPath, 'finalout0522')


def plotResult(yPredict3, yPredict4, yPredict5):
    # p1tag = plt.plot(yPredict1, 'bo', yPredict1, 'b-')
    # p2tag = plt.plot(yPredict2, 'go', yPredict2, 'g-')
    p3tag = plt.plot(yPredict3, 'co', yPredict3, 'c-')
    p4tag = plt.plot(yPredict4, 'yo', yPredict4, 'y-')
    p5tag = plt.plot(yPredict5, 'ro', yPredict5, 'r-')
    plt.legend([p3tag[1], p4tag[1], p5tag[1]],
               ['gbrt', 'erf', 'xgb'])
    plt.xlabel('test days')
    plt.ylabel('counts')


def writecsv(finalResultFile, artistId, yPredictSum):
    with open(finalResultFile, 'a') as file:
        for num in range(len(yPredictSum)):
            file.write(','.join([artistId, str(int(round(yPredictSum[num]))), utils.num2date(num)]) + '\n')


def genModel(artist, song, model, embedDim, interval, distance):
    XTrain, yTrain, XPredict, mean, var = pp.fprocess(artist, song, embedDim, interval, distance)
    yPredict = model.train(XTrain, yTrain, XPredict)
    yPredict = yPredict * var + mean
    yPredict[yPredict < 0] = 0  # 预测值出现负数直接归零
    return yPredict


def itergenModel(artist, song, model, embedDim, interval, testsize):
    XTrain, yTrain, mean, var = iterpp.fprocess(artist, song, embedDim, interval)
    yPredict = model.train(XTrain, yTrain, testsize)
    yPredict = yPredict * var + mean
    yPredict[yPredict < 0] = 0  # 预测值出现负数直接归零
    return yPredict


def fout(embedDim, interval, distance):
    artistObjectFile = os.path.join(utils.allResultPath, 'artistsObjectDict.pkl')
    artistsObjectDict = cPickle.load(open(artistObjectFile, 'r'))
    modelParamsDict = {}
    plt.figure(figsize=(6, 4))
    artistNum = 0
    for artistId, artist in artistsObjectDict.items():
        artistNum += 1
        print artistNum
        modelParamsDict[artistId] = {}
        savePath = os.path.join(utils.resultPath, artistId)
        if not os.path.exists(savePath):
            os.makedirs(savePath)
        # yPredictSum1 = np.zeros(testsize)
        # yPredictSum2 = np.zeros(distance)
        yPredictSum3 = np.zeros(distance)
        yPredictSum4 = np.zeros(distance)
        yPredictSum5 = np.zeros(distance)
        for songId, song in artist.getSongsOwned().items():
            traceLength = np.array(song.getTrace()).shape[1]
            trainLength = pp.XTrainLength(traceLength, embedDim, interval, distance)
            if trainLength < 8:  # 训练集长度不足8的歌曲跳过
                print 'iterated ' + str(traceLength) + ' ' + str(trainLength)
                # # SVR模型
                # yPredict1 = genModel(artist, song, svrModel, embedDim, interval, testsize)
                # # 随机森林模型
                # yPredict2 = genModel(artist, song, rfModel, embedDim, interval, distance)
                # GBRT模型
                yPredict3 = itergenModel(artist, song, itergbrtModel, embedDim, interval, distance)
                # 完全随机森林模型
                yPredict4 = itergenModel(artist, song, itererfModel, embedDim, interval, distance)
                # xgboost模型
                yPredict5 = itergenModel(artist, song, iterxgbModel, embedDim, interval, distance)
            else:
                print 'direct ' + str(traceLength) + ' ' + str(trainLength)
                # # SVR模型
                # yPredict1 = genModel(artist, song, svrModel, embedDim, interval, testsize)
                # # 随机森林模型
                # yPredict2 = genModel(artist, song, rfModel, embedDim, interval, distance)
                # GBRT模型
                yPredict3 = genModel(artist, song, gbrtModel, embedDim, interval, distance)
                # 完全随机森林模型
                yPredict4 = genModel(artist, song, erfModel, embedDim, interval, distance)
                # xgboost模型
                yPredict5 = genModel(artist, song, xgbModel, embedDim, interval, distance)
            plotResult(yPredict3, yPredict4, yPredict5)
            plt.savefig(os.path.join(savePath, 'song ' + songId + ".png"))
            plt.clf()
            # yPredictSum1 += yPredict1
            # yPredictSum2 += yPredict2
            yPredictSum3 += yPredict3
            yPredictSum4 += yPredict4
            yPredictSum5 += yPredict5
        plotResult(yPredictSum3, yPredictSum4, yPredictSum5)
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
        finalResultFile5 = os.path.join(finalResultPath, 'xgb.csv')
        writecsv(finalResultFile5, artistId, yPredictSum5)


if __name__ == '__main__':
    warnings.filterwarnings("ignore")
    if not os.path.exists(utils.resultPath):
        os.makedirs(utils.resultPath)
    if not os.path.exists(finalResultPath):
        os.makedirs(finalResultPath)
    distance = 60
    embedDim = 1
    interval = 0
    fout(embedDim, interval, distance)
    # for embedDim in range(1, 6):
    #     for interval in range(6):
    #         fout(embedDim, interval, testsize)
