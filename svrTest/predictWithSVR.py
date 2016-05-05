__author__ = 'zfh'
# coding:utf-8

from sklearn import svm, grid_search
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt
import numpy as np
import utils, os
import cPickle


def makePlayCount(array, index):
    array = np.array(array)
    return array[0, index]


def makeFeature(array, embedDim, offset):
    array = np.array(array)
    feature = []
    for i in range(embedDim):
        feature.extend(array[:, offset - embedDim + i])
    return feature


def makeDataset(array, embedDim):
    array = np.array(array)
    X = []
    y = []
    for i in range(embedDim, array.shape[1]):
        X.append(makeFeature(array, embedDim, i))
        y.append(makePlayCount(array, i))
    return X, y


def uniform(array):
    array = np.array(array, dtype=float)
    factor = np.max(array, axis=1)
    for i in range(array.shape[0]):
        array[i, :] /= factor[i]
    array[array == np.nan] = 0
    array[array == np.inf] = 0
    return array, factor[0]  # 播放量的比例因子


def split(array, trainLength):
    train = array[:, :trainLength]
    test = array[:, trainLength:]
    return train, test


def makeDataArray(artist, song):
    songTrace = song.getTrace()
    songPercent = song.getPercentInSongs()
    artistPercent = artist.getPercentInArtists()
    return np.vstack((songTrace, songPercent, artistPercent))


def normalizedVariation(yTrue, yPredict):
    normSquare = [((p - t) / t) ** 2 for t, p in zip(yTrue, yPredict)]
    return np.sqrt(np.mean(normSquare))


dim = 3
trainLength = 100
artistObjectFile = os.path.join(utils.allResultPath, 'result0505', 'artistsObjectDict.pkl')
artistsObjectDict = cPickle.load(open(artistObjectFile, 'r'))
artistF = []
plt.figure(figsize=(6, 4))
for artistId, artist in artistsObjectDict.items():
    savePath = os.path.join(utils.resultPath, artistId)
    if not os.path.exists(savePath):
        os.makedirs(savePath)
    yTestSum = [0 for __ in range(utils.days - trainLength)]
    yPredictSum = [0 for __ in range(utils.days - trainLength)]
    for songId, song in artist.getSongsOwned().items():
        array = makeDataArray(artist, song)
        array, factor = uniform(array)  # 归一化
        train, test = split(array, trainLength)
        XTrain, yTrain = makeDataset(array=train, embedDim=dim)
        XTest, yTest = makeDataset(array=test, embedDim=dim)
        svr = svm.SVR()
        para = {'C': [1, 10, 30]}
        clf = grid_search.GridSearchCV(svr, para)
        # clf.fit(XTrain, yTrain)
        yPredict = []
        for XSub, ySub in zip(XTest, yTest):
            clf.fit(XTrain, yTrain)  # 使用更新后的训练集重新生成模型
            yPredict.extend(clf.predict([XSub]))
            XTrain.pop(0)
            XTrain.append(XSub)
            yTrain.pop(0)
            yTrain.append(ySub)
        yTest = [i * factor for i in yTest]
        yPredict = [i * factor for i in yPredict]
        rmse = np.sqrt(mean_squared_error(yTest, yPredict))
        yptag = plt.plot(yPredict, 'bo', yPredict, 'b-')
        yttag = plt.plot(yTest, 'ro', yTest, 'r-')
        plt.legend([yptag[1], yttag[1]], ['predict', 'test'])
        plt.xlabel('test days')
        plt.ylabel('counts')
        plt.title('song id:' + songId + '\n' + 'RMSE:' + str(rmse))
        plt.savefig(os.path.join(savePath, 'song' + songId + ".png"))
        plt.clf()
        yTestSum = [i + j for i, j in zip(yTestSum, yTest)]
        yPredictSum = [i + j for i, j in zip(yPredictSum, yPredict)]
    rmseSum = np.sqrt(mean_squared_error(yTestSum, yPredictSum))
    nvar = normalizedVariation(yTestSum, yPredictSum)
    plt.figure(figsize=(6, 4))
    yptag = plt.plot(yPredictSum, 'bo', yPredictSum, 'b-')
    yttag = plt.plot(yTestSum, 'ro', yTestSum, 'r-')
    plt.legend([yptag[1], yttag[1]], ['predict', 'test'])
    plt.xlabel('test days')
    plt.ylabel('counts')
    plt.title('artist sum:' + artistId + '\n' + 'RMSE:' + str(rmseSum) + '-nvar:' + str(nvar))
    plt.savefig(os.path.join(savePath, 'artist' + artistId + ".png"))
    plt.clf()
    artistWeight = np.sqrt(np.sum(artist.getTotalTrace()[0, :]))
    artistF.append(artistWeight * nvar)

print artistF
print np.sum(artistF)
