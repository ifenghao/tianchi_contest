__author__ = 'zfh'
# coding:utf-8

import os
import cPickle
import warnings
import time

import matplotlib.pyplot as plt
import numpy as np

import utils
import erfModel, gbrtModel

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


def fout(embedDim, interval):
    artistObjectFile = os.path.join(utils.allResultPath, 'artistsObjectDict.pkl')
    artistsObjectDict = cPickle.load(open(artistObjectFile, 'r'))
    plt.figure(figsize=(6, 4))
    artistNum = 0
    for artistId, artist in artistsObjectDict.items():
        artistNum += 1
        print artistNum
        # # SVR模型
        # yPredict1 = genModel(artist, song, svrModel, embedDim, interval)
        # # 随机森林模型
        # yPredict2 = genModel(artist, song, rfModel, embedDim, interval, distance)
        # GBRT模型
        yPredict3 = gbrtModel.train(artist, embedDim, interval)
        # 完全随机森林模型
        yPredict4 = erfModel.train(artist, embedDim, interval)
        plotResult(yPredict3, yPredict4)
        plt.savefig(os.path.join(utils.resultPath, 'artist ' + artistId + ".png"))
        plt.clf()
        # finalResultFile1 = os.path.join(finalResultPath, 'svr.csv')
        # writecsv(finalResultFile1, artistId, yPredictSum1)
        # finalResultFile2 = os.path.join(finalResultPath, 'rf.csv')
        # writecsv(finalResultFile2, artistId, yPredictSum2)
        finalResultFile3 = os.path.join(finalResultPath, 'gbrt.csv')
        writecsv(finalResultFile3, artistId, yPredict3)
        finalResultFile4 = os.path.join(finalResultPath, 'erf.csv')
        writecsv(finalResultFile4, artistId, yPredict4)


if __name__ == '__main__':
    warnings.filterwarnings("ignore")
    if not os.path.exists(utils.resultPath):
        os.makedirs(utils.resultPath)
    if not os.path.exists(finalResultPath):
        os.makedirs(finalResultPath)
    embedDim = 7
    interval = 0
    fout(embedDim, interval)
    # for embedDim in range(1, 6):
    #     for interval in range(6):
    #         fout(embedDim, interval, testsize)
