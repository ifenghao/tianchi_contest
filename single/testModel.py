__author__ = 'zfh'
# coding:utf-8

import os
import cPickle
import time

from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt
import numpy as np

import utils
import preprocess as pp
import erfModel
import gbrtModel
from iterated import preprocess as iterpp
from iterated import gbrtModel as itergbrtModel
from iterated import erfModel as itererfModel


def plotResult(yPredict3, yPredict4, yTest):
    p3tag = plt.plot(yPredict3, 'bo', yPredict3, 'b-')
    p4tag = plt.plot(yPredict4, 'go', yPredict4, 'g-')
    # p5tag = plt.plot(yPredict5, 'ro', yPredict5, 'r-')
    ttag = plt.plot(yTest, 'ko', yTest, 'k-')
    plt.legend([p3tag[1], p4tag[1], ttag[1]],
               ['GBRT', 'erf', 'test'])
    plt.xlabel('test days')
    plt.ylabel('counts')


def genModel(artist, song, model, embedDim, interval, distance):
    XTrain, yTrain, XPredict, yTest, mean, var = pp.process(artist, song, embedDim, interval, distance)
    yPredict = model.train(XTrain, yTrain, XPredict)
    yTest = yTest * var + mean
    yPredict = yPredict * var + mean
    yPredict[yPredict < 0] = 0  # 预测值出现负数直接归零
    return yPredict, yTest


def itergenModel(artist, song, model, embedDim, interval, testsize):
    XTrain, yTrain, yTest, mean, var = iterpp.process(artist, song, embedDim, interval, testsize)
    yPredict = model.train(XTrain, yTrain, testsize)
    yTest = yTest * var + mean
    yPredict = yPredict * var + mean
    yPredict[yPredict < 0] = 0  # 预测值出现负数直接归零
    return yPredict, yTest


def test(embedDim, interval, distance):  # distance是预测长度，也是测试集长度
    artistObjectFile = os.path.join(utils.allResultPath, 'artistsObjectDict.pkl')
    artistsObjectDict = cPickle.load(open(artistObjectFile, 'r'))
    # artistF1Score1 = []
    # artistF1Score2 = []
    artistF1Score3 = []
    artistF1Score4 = []
    # artistF1Score5 = []
    plt.figure(figsize=(6, 6))
    artistNum = 0
    for artistId, artist in artistsObjectDict.items():
        artistNum += 1
        print artistNum
        savePath = os.path.join(utils.resultPath, str(embedDim) + ' ' + str(interval), artistId)
        if not os.path.exists(savePath):
            os.makedirs(savePath)
        yTestSum = np.zeros(distance)
        # yPredictSum1 = np.zeros(distance)
        # yPredictSum2 = np.zeros(distance)
        yPredictSum3 = np.zeros(distance)
        yPredictSum4 = np.zeros(distance)
        # yPredictSum5 = np.zeros(distance)
        for songId, song in artist.getSongsOwned().items():
            traceLength = np.array(song.getTrace()).shape[1]
            trainLength = pp.XTrainLength(traceLength, embedDim, interval, distance)
            if trainLength <= 8:  # 不测试预测天数之后发行的歌曲
                continue
            if trainLength < 8 + distance:  # 训练集长度不足3的歌曲跳过
                print 'iterated ' + str(traceLength) + ' ' + str(trainLength)
                # # SVR模型
                # yPredict1, yTest = genModel(artist, song, svrModel, embedDim, interval, distance)
                # rmse1 = np.sqrt(mean_squared_error(yTest, yPredict1))
                # nvar1 = utils.normalizedVariation(yTest, yPredict1)
                # # 随机森林模型
                # yPredict2, yTest = genModel(artist, song, rfModel, embedDim, interval, distance)
                # rmse2 = np.sqrt(mean_squared_error(yTest, yPredict2))
                # nvar2 = utils.normalizedVariation(yTest, yPredict2)
                # GBRT模型
                yPredict3, yTest = itergenModel(artist, song, itergbrtModel, embedDim, interval, distance)
                rmse3 = np.sqrt(mean_squared_error(yTest, yPredict3))
                nvar3 = utils.normalizedVariation(yTest, yPredict3)
                # 完全随机森林模型
                yPredict4, yTest = itergenModel(artist, song, itererfModel, embedDim, interval, distance)
                rmse4 = np.sqrt(mean_squared_error(yTest, yPredict4))
                nvar4 = utils.normalizedVariation(yTest, yPredict4)
                # xgboost模型
                # yPredict5, yTest = itergenModel(artist, song, iterxgbModel, embedDim, interval, distance)
                # rmse5 = np.sqrt(mean_squared_error(yTest, yPredict5))
                # nvar5 = utils.normalizedVariation(yTest, yPredict5)
            else:
                print 'single ' + str(traceLength) + ' ' + str(trainLength)
                # # SVR模型
                # yPredict1, yTest, best_params1 = genModel(artist, song, svrModel, embedDim, interval, distance)
                # rmse1 = np.sqrt(mean_squared_error(yTest, yPredict1))
                # nvar1 = utils.normalizedVariation(yTest, yPredict1)
                # modelList.append(best_params1)
                # # 随机森林模型
                # yPredict2, yTest, best_params2 = genModel(artist, song, rfModel, embedDim, interval, distance)
                # rmse2 = np.sqrt(mean_squared_error(yTest, yPredict2))
                # nvar2 = utils.normalizedVariation(yTest, yPredict2)
                # modelList.append(best_params2)
                # GBRT模型
                yPredict3, yTest = genModel(artist, song, gbrtModel, embedDim, interval, distance)
                rmse3 = np.sqrt(mean_squared_error(yTest, yPredict3))
                nvar3 = utils.normalizedVariation(yTest, yPredict3)
                # 完全随机森林模型
                yPredict4, yTest = genModel(artist, song, erfModel, embedDim, interval, distance)
                rmse4 = np.sqrt(mean_squared_error(yTest, yPredict4))
                nvar4 = utils.normalizedVariation(yTest, yPredict4)
                # xgboost模型
                # yPredict5, yTest = genModel(artist, song, xgbModel, embedDim, interval, distance)
                # rmse5 = np.sqrt(mean_squared_error(yTest, yPredict5))
                # nvar5 = utils.normalizedVariation(yTest, yPredict5)
            plotResult(yPredict3, yPredict4, yTest)
            plt.title(
                # 'SVR=RMSE:' + str(rmse1) + '-nvar:' + str(nvar1) + '\n' + \
                # 'RF=RMSE:' + str(rmse2) + '-nvar:' + str(nvar2) + '\n' + \
                'GBRT=RMSE:' + str(rmse3) + '-nvar:' + str(nvar3) + '\n' + \
                'erf=RMSE:' + str(rmse4) + '-nvar:' + str(nvar4)
                # 'bag=RMSE:' + str(rmse5) + '-nvar:' + str(nvar5)
            )
            plt.savefig(os.path.join(savePath, 'song ' + songId + ".png"))
            plt.clf()
            yTestSum += yTest
            # yPredictSum1 += yPredict1
            # yPredictSum2 += yPredict2
            yPredictSum3 += yPredict3
            yPredictSum4 += yPredict4
            # yPredictSum5 += yPredict5
        # rmseSum1 = np.sqrt(mean_squared_error(yTestSum, yPredictSum1))
        # nvarSum1 = utils.normalizedVariation(yTestSum, yPredictSum1)
        # rmseSum2 = np.sqrt(mean_squared_error(yTestSum, yPredictSum2))
        # nvarSum2 = utils.normalizedVariation(yTestSum, yPredictSum2)
        rmseSum3 = np.sqrt(mean_squared_error(yTestSum, yPredictSum3))
        nvarSum3 = utils.normalizedVariation(yTestSum, yPredictSum3)
        rmseSum4 = np.sqrt(mean_squared_error(yTestSum, yPredictSum4))
        nvarSum4 = utils.normalizedVariation(yTestSum, yPredictSum4)
        # rmseSum5 = np.sqrt(mean_squared_error(yTestSum, yPredictSum5))
        # nvarSum5 = utils.normalizedVariation(yTestSum, yPredictSum5)
        plotResult(yPredictSum3, yPredictSum4, yTestSum)
        plt.title(
            # 'SVR=RMSE:' + str(rmseSum1) + '-nvar:' + str(nvarSum1) + '\n' + \
            # 'RF=RMSE:' + str(rmseSum2) + '-nvar:' + str(nvarSum2) + '\n' + \
            'GBRT=RMSE:' + str(rmseSum3) + '-nvar:' + str(nvarSum3) + '\n' + \
            'erf=RMSE:' + str(rmseSum4) + '-nvar:' + str(nvarSum4)
            # 'xgb=RMSE:' + str(rmseSum5) + '-nvar:' + str(nvarSum5)
        )
        plt.savefig(os.path.join(savePath, 'artist ' + artistId + ".png"))
        plt.clf()
        artistWeight = np.sqrt(np.sum(artist.getTotalTrace()[0, -distance:]))
        # artistF1Score1.append(artistWeight * (1 - nvarSum1))
        # artistF1Score2.append(artistWeight * (1 - nvarSum2))
        artistF1Score3.append(artistWeight * (1 - nvarSum3))
        artistF1Score4.append(artistWeight * (1 - nvarSum4))
        # artistF1Score5.append(artistWeight * (1 - nvarSum5))
    f1ScoreFile = os.path.join(utils.allResultPath, 'F1Score')
    with open(f1ScoreFile, 'a') as file:
        file.write(time.asctime())
        file.write('embedDim=' + str(embedDim) + ', interval=' + str(interval) + ', distance=' + str(distance))
        file.write('\n')
        # file.write('SVR:' + str(np.sum(artistF1Score1)) + '\n' + str(artistF1Score1) + '\n')
        # file.write('-RF:' + str(np.sum(artistF1Score2)) + '\n' + str(artistF1Score2) + '\n')
        file.write('-GBRT:' + str(np.sum(artistF1Score3)) + '\n' + str(artistF1Score3) + '\n')
        file.write('-erf:' + str(np.sum(artistF1Score4)) + '\n' + str(artistF1Score4) + '\n')
        # file.write('-xgb:' + str(np.sum(artistF1Score5)) + '\n' + str(artistF1Score5) + '\n')
        file.write('\n')


if __name__ == '__main__':
    if not os.path.exists(utils.resultPath):
        os.makedirs(utils.resultPath)
    distance = 60
    # embedDim = 3
    interval = 0
    # test(embedDim, interval, distance)
    for embedDim in range(6, 10):
        test(embedDim, interval, distance)
