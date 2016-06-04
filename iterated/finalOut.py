__author__ = 'zfh'
# coding:utf-8

import os
import cPickle

import matplotlib.pyplot as plt
import numpy as np

import utils
import preprocess as pp
import erfModel, gbrtModel

finalResultPath = os.path.join(utils.allResultPath, 'finalout0518')


def plotResult(yPredict3, yPredict4):
    # p1tag = plt.plot(yPredict1, 'bo', yPredict1, 'b-')
    # p2tag = plt.plot(yPredict2, 'go', yPredict2, 'g-')
    p3tag = plt.plot(yPredict3, 'co', yPredict3, 'c-')
    p4tag = plt.plot(yPredict4, 'ro', yPredict4, 'r-')
    plt.legend([p3tag[1], p4tag[1]],
               ['GBRT', 'erf'])
    plt.xlabel('test days')
    plt.ylabel('counts')


def writecsv(finalResultFile, artistId, yPredictSum):
    with open(finalResultFile, 'a') as file:
        for num in range(len(yPredictSum)):
            file.write(','.join([artistId, str(int(round(yPredictSum[num]))), utils.num2date(num)]) + '\n')


def genModel(artist, song, model, embedDim, interval, testsize):
    XTrain, yTrain, mean, var = pp.fprocess(artist, song, embedDim, interval)
    yPredict = model.train(XTrain, yTrain, testsize)
    yPredict = yPredict * var + mean
    yPredict[yPredict < 0] = 0  # 预测值出现负数直接归零
    return yPredict


def fout(embedDim, interval, testsize):
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
        # yPredictSum2 = np.zeros(testsize)
        yPredictSum3 = np.zeros(testsize)
        yPredictSum4 = np.zeros(testsize)
        # yPredictSum5 = np.zeros(testsize)
        for songId, song in artist.getSongsOwned().items():
            print songId
            # SVR模型
            # yPredict1 = genModel(artist, song, svrModel, embedDim, interval, testsize)
            # 随机森林模型
            # yPredict2 = genModel(artist, song, rfModel, embedDim, interval, testsize)
            # GBRT模型
            yPredict3 = genModel(artist, song, gbrtModel, embedDim, interval, testsize)
            # 完全随机森林模型
            yPredict4 = genModel(artist, song, erfModel, embedDim, interval, testsize)
            # xgboost模型
            # yPredict5 = genModel(artist, song, xgbModel, embedDim, interval, testsize)
            plotResult(yPredict3, yPredict4)
            plt.savefig(os.path.join(savePath, 'song ' + songId + ".png"))
            plt.clf()
            # yPredictSum1 += yPredict1
            # yPredictSum2 += yPredict2
            yPredictSum3 += yPredict3
            yPredictSum4 += yPredict4
            # yPredictSum5 += yPredict5
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
        # finalResultFile5 = os.path.join(finalResultPath, 'xgb.csv')
        # writecsv(finalResultFile5, artistId, yPredictSum5)


if __name__ == '__main__':
    if not os.path.exists(utils.resultPath):
        os.makedirs(utils.resultPath)
    if not os.path.exists(finalResultPath):
        os.makedirs(finalResultPath)
    testsize = 60
    embedDim = 7
    interval = 0
    fout(embedDim, interval, testsize)
    # for embedDim in range(1, 6):
    #     for interval in range(6):
    #         fout(embedDim, interval, testsize)
