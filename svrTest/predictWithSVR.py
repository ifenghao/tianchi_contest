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
    play = play / float(playMax)
    downloadMax = np.max(download)
    download = download / float(downloadMax)
    collectMax = np.max(collect)
    collect = collect / float(collectMax)
    usersMax = np.max(users)
    users = users / float(usersMax)
    data = [play, download, collect, users]
    return data, playMax


def split(data, percent):
    play = data[0]
    download = data[1]
    collect = data[2]
    users = data[3]
    total = len(play)
    trainLength = int(total * percent)
    train = [play[:trainLength], download[:trainLength], collect[:trainLength], users[:trainLength]]
    test = [play[trainLength:], download[trainLength:], collect[trainLength:], users[trainLength:]]
    return train, test


def normalizedVariation(yTrue, yPredict):
    normSquare = [((p - t) / t) ** 2 for t, p in zip(yTrue, yPredict)]
    return np.sqrt(np.mean(normSquare))


dim = 5
artistsDict = cPickle.load(open(utils.artistsPickleFile, 'r'))
for artistId in artistsDict.keys():
    savePath = os.path.join(utils.resultPath, artistId)
    if not os.path.exists(savePath):
        os.makedirs(savePath)
    artistFile = os.path.join(utils.allResultPath, 'result0503', artistId + '.pkl')
    artist = cPickle.load(open(artistFile, 'r'))
    for songId, song in artist.getSongsOwned().items():
        data, factor = uniform(song)
        train, test = split(data, 0.5)
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
        rmse = np.sqrt(mean_squared_error(yTest, yPredict))
        nvar = normalizedVariation(yTest, yPredict)
        plt.figure(figsize=(6, 4))
        yptag = plt.plot(yPredict, 'bo', yPredict, 'b-')
        yttag = plt.plot(yTest, 'ro', yTest, 'r-')
        plt.legend([yptag[1], yttag[1]], ['predict', 'test'])
        plt.xlabel('test days')
        plt.ylabel('counts')
        plt.title('song id:' + songId + '\n' + \
                  'RMSE:' + str(rmse) + '-' + 'NVAR' + str(nvar))
        plt.savefig(os.path.join(savePath, songId + ".png"))
        plt.clf()
        plt.close()
