__author__ = 'zfh'
# coding:utf-8

from sklearn.metrics import mean_squared_error
import os
import cPickle

import matplotlib.pyplot as plt
import numpy as np

import utils
import svrModel
import preprocess as pp


def plotResult(yPredict, yTest):
    yptag = plt.plot(yPredict, 'bo', yPredict, 'b-')
    yttag = plt.plot(yTest, 'ro', yTest, 'r-')
    plt.legend([yptag[1], yttag[1]], ['predict', 'test'])
    plt.xlabel('test days')
    plt.ylabel('counts')


embedDim = 3
interval = 0
distance = 48
trainLen = 135
artistObjectFile = os.path.join(utils.allResultPath, 'result0506', 'artistsObjectDict.pkl')
artistsObjectDict = cPickle.load(open(artistObjectFile, 'r'))
artistF = []
plt.figure(figsize=(6, 4))
for artistId, artist in artistsObjectDict.items():
    savePath = os.path.join(utils.resultPath, artistId)
    if not os.path.exists(savePath):
        os.makedirs(savePath)
    yTestSum = [0 for __ in range(utils.days - trainLen)]
    yPredictSum = [0 for __ in range(utils.days - trainLen)]
    for songId, song in artist.getSongsOwned().items():
        XTrain, yTrain, XPredict, yTest, mean, var = pp.process(artist, song, trainLen, embedDim, interval, distance)
        yPredict = svrModel.trainSVR(XTrain, yTrain, XPredict)
        yTest = [i * var + mean for i in yTest]
        yPredict = [i * var + mean for i in yPredict]
        rmse = np.sqrt(mean_squared_error(yTest, yPredict))
        nvar = utils.normalizedVariation(yTest, yPredict)
        plotResult(yPredict, yTest)
        plt.title('song id:' + songId + '\n' + 'RMSE:' + str(rmse) + '-nvar:' + str(nvar))
        plt.savefig(os.path.join(savePath, 'song' + songId + ".png"))
        plt.clf()
        yTestSum = [i + j for i, j in zip(yTestSum, yTest)]
        yPredictSum = [i + j for i, j in zip(yPredictSum, yPredict)]
    rmseSum = np.sqrt(mean_squared_error(yTestSum, yPredictSum))
    nvarSum = utils.normalizedVariation(yTestSum, yPredictSum)
    plotResult(yPredictSum, yTestSum)
    plt.title('artist sum:' + artistId + '\n' + 'RMSE:' + str(rmseSum) + '-nvarSum:' + str(nvarSum))
    plt.savefig(os.path.join(savePath, 'artist' + artistId + ".png"))
    plt.clf()
    artistWeight = np.sqrt(np.sum(artist.getTotalTrace()[0, :]))
    artistF.append(artistWeight * (1 - nvarSum))

f1ScoreFile = os.path.join(utils.allResultPath, 'F1Score')
with open(f1ScoreFile, 'a') as file:
    file.write(str(artistF))
    file.write('\n')
    file.write(str(np.sum(artistF)))
    file.write('\n')
