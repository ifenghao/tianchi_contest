__author__ = 'zfh'
# coding:utf-8
from sklearn.ensemble import GradientBoostingRegressor
from sklearn import cross_validation, grid_search
from sklearn import cluster
from scipy.stats import randint, uniform
import numpy as np
from copy import copy
import preprocess as pp
from iterated import gbrtModel as itergbrtModel
import utils


def train(artist, embedDim, interval):
    embedDimInit = embedDim
    intervalInit = interval
    distance = 7
    playArray = []
    songsList = []
    shortSongsList = []
    for song in artist.getSongsOwned().values():
        playTrace = song.getTrace()[0]
        traceLength = len(playTrace)
        trainLength = pp.XTrainLength(traceLength, embedDim, interval, distance)  # 训练集长度
        if trainLength < 10:  # 短歌曲不参与聚类训练
            shortSongsList.append(song)
            continue
        if traceLength < utils.days:
            playTrace = np.hstack((np.zeros(utils.days - traceLength), playTrace))
        playArray.append(playTrace)
        songsList.append(song)
    apc = cluster.AffinityPropagation(damping=0.5, max_iter=500, convergence_iter=20, preference=None,
                                      affinity='euclidean')
    clusterIndex = apc.fit_predict(playArray)
    clusterDict = {}
    for index, song in zip(clusterIndex, songsList):  # 将歌曲聚类
        if index not in clusterDict:
            clusterDict[index] = []
        songList = clusterDict.get(index)
        songList.append(song)

    yPredictSum = np.zeros(60)
    for index, songList in clusterDict.items():
        print 'cluster' + str(index)
        embedDim = embedDimInit
        interval = intervalInit
        tracelist, meanList, varList = makeTraceList(songList)
        XTrainCluster, yTrainCluster = foldTrain(tracelist, embedDim, interval, distance)
        kfold = cross_validation.KFold(len(XTrainCluster), n_folds=5, shuffle=False)
        params = {'n_estimators': randint(20, 200),
                  'loss': ['ls', 'lad', 'huber'],
                  'learning_rate': uniform(0.01, 0.19),
                  'subsample': uniform(0.5, 0.5),
                  'max_depth': randint(1, 5),
                  'min_samples_split': randint(1, 3),
                  'min_samples_leaf': randint(1, 3),
                  'max_features': randint(1, len(XTrainCluster[0]))}
        bestModels = []
        for i in range(len(yTrainCluster[0])):
            gbrt = GradientBoostingRegressor()
            clf = grid_search.RandomizedSearchCV(gbrt, param_distributions=params, n_iter=30,
                                                 scoring='mean_squared_error', cv=kfold, n_jobs=-1)
            clf.fit(XTrainCluster, yTrainCluster[:, i])
            bestModels.append(clf.best_estimator_)

        for i in range(9):
            XTrainCluster, yTrainCluster = foldTrain(tracelist, embedDim, interval, distance)
            XPredictCluster = foldPredict(tracelist, embedDim, interval, distance)
            for k in range(len(songList)):  # 对每首歌曲用同一个类别模型做预测
                XPredict = XPredictCluster[k]
                subyPredict = []
                for j in range(len(yTrainCluster[0])):
                    bestModels[j].fit(XTrainCluster, yTrainCluster[:, j])
                    subyPredict.append(bestModels[j].predict(XPredict))
                tracelist[k] = np.hstack((tracelist[k], np.array(copy(subyPredict))))  # 将一个模型的预测值作为已知数据，训练下一个模型
            embedDim += distance
        yPredictSum += clusterSum(tracelist, meanList, varList)
    yPredictSum += shortSongsPredict(shortSongsList, embedDimInit, interval)
    return yPredictSum


def makeTraceList(clusterSongList):  # 提取歌曲的trace
    tracelist = []
    meanList = []
    varList = []
    for song in clusterSongList:
        array, mean, var = pp.fprocess(song)
        tracelist.append(copy(array))
        meanList.append(copy(mean))
        varList.append(copy(var))
    return tracelist, meanList, varList


def foldTrain(tracelist, embedDim, interval, distance):  # 将同一类的歌曲的输入空间合并
    clusterXTrain = np.array([])
    clusteryTrain = np.array([])
    for i in range(len(tracelist)):
        array = tracelist[i]
        XTrain, yTrain = pp.makeTrainset(array, embedDim, interval, distance)
        if i == 0:
            clusterXTrain = copy(XTrain)
            clusteryTrain = copy(yTrain)
        else:
            clusterXTrain = np.vstack((clusterXTrain, copy(XTrain)))
            clusteryTrain = np.vstack((clusteryTrain, copy(yTrain)))
    return clusterXTrain, clusteryTrain


def foldPredict(tracelist, embedDim, interval, distance):
    clusterXPredict = []
    for array in tracelist:
        XPredict = pp.makeXPredict(array, embedDim, interval, distance)
        clusterXPredict.append(copy(XPredict))
    return clusterXPredict


def clusterSum(tracelist, meanList, varList):
    yPredictCluster = np.zeros(60)
    for array, mean, var in zip(tracelist, meanList, varList):
        yPredictCluster += array[0, -62:-2] * var + mean
    return yPredictCluster


def shortSongsPredict(shortSongsList, embedDim, interval):
    yPredictSum = np.zeros(60)
    for song in shortSongsList:
        array, mean, var = pp.fprocess(song)
        yPredict = itergbrtModel.train(array, embedDim, interval)
        yPredict = yPredict * var + mean
        yPredict[yPredict < 0] = 0  # 预测值出现负数直接归零
        yPredictSum += yPredict
    return yPredictSum
