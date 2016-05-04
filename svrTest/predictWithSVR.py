__author__ = 'zfh'
# coding:utf-8

from sklearn import svm, grid_search
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt
import numpy as np
import utils, os
import cPickle

# 生成输入空间
def makeDataset(array, insertDim):
    play = array[0]
    download = array[1]
    collect = array[2]
    users = array[3]
    if not len(play) == len(download) == len(collect):
        raise Exception('length not equal')
    X = []
    y = []
    for i in range(insertDim, len(play)):
        subX = []
        for j in range(insertDim):
            subX.extend([play[i - insertDim + j], download[i - insertDim + j],
                         collect[i - insertDim + j], users[i - insertDim + j]])
        X.append(subX)
        y.append(play[i])
    return X, y


def uniform(song):
    play = song.getPlayTrace()
    download = song.getDownTrace()
    collect = song.getCollectTrace()
    users = song.getUsersTrace()
    playMax = np.max(play)
    if playMax == 0: playMax = 0.001
    play = [i / float(playMax) for i in play]
    downloadMax = np.max(download)
    if downloadMax == 0: downloadMax = 0.001
    download = [i / float(downloadMax) for i in download]
    collectMax = np.max(collect)
    if collectMax == 0: collectMax = 0.001
    collect = [i / float(collectMax) for i in collect]
    usersMax = np.max(users)
    if usersMax == 0: usersMax = 0.001
    users = [i / float(usersMax) for i in users]
    data = [play, download, collect, users]
    return data, playMax


def split(data, trainLength):
    play = data[0]
    download = data[1]
    collect = data[2]
    users = data[3]
    train = [play[:trainLength], download[:trainLength], collect[:trainLength], users[:trainLength]]
    test = [play[trainLength:], download[trainLength:], collect[trainLength:], users[trainLength:]]
    return train, test


def normalizedVariation(yTrue, yPredict):
    normSquare = [((p - t) / t) ** 2 for t, p in zip(yTrue, yPredict)]
    return np.sqrt(np.mean(normSquare))


dim = 3
trainLength = 100
artistsDict = cPickle.load(open(utils.artistsPickleFile, 'r'))
plt.figure(figsize=(6, 4))
for artistId in artistsDict.keys():
    savePath = os.path.join(utils.resultPath, artistId)
    if not os.path.exists(savePath):
        os.makedirs(savePath)
    artistFile = os.path.join(utils.allResultPath, 'result0503', artistId + '.pkl')
    artist = cPickle.load(open(artistFile, 'r'))
    yTestSum = [0 for __ in range(utils.days - trainLength)]
    yPredictSum = [0 for __ in range(utils.days - trainLength)]
    for songId, song in artist.getSongsOwned().items():
        data, factor = uniform(song)  # 归一化
        train, test = split(data, trainLength)
        XTrain, yTrain = makeDataset(array=train, insertDim=dim)
        XTest, yTest = makeDataset(array=test, insertDim=dim)
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
