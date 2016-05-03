__author__ = 'zfh'
# coding:utf-8

from sklearn import svm,grid_search
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt
import numpy as np
import utils, os

# 生成输入空间
def makeDataset(fourRowList, insertDim):
    play = fourRowList[0]
    download = fourRowList[1]
    collect = fourRowList[2]
    users = fourRowList[3]
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


def getDataFromTxt(artistId):
    statisticsFile = os.path.join(utils.allResultPath, artistId, 'statistics.txt')
    songsDict = {}
    with open(statisticsFile, 'r') as file:
        while True:
            songId = file.readline().strip('\n')
            if songId == 'sum':
                break
            issueTime = file.readline().strip('\n')
            initPlay = file.readline().strip('\n')
            language = file.readline().strip('\n')
            play = map(int, file.readline().strip('\n').split(','))
            download = map(int, file.readline().strip('\n').split(','))
            collect = map(int, file.readline().strip('\n').split(','))
            users = map(int, file.readline().strip('\n').split(','))
            songsDict[songId] = [play, download, collect, users]
    return songsDict


def splitDataset(fourRowList):
    play = fourRowList[0]
    download = fourRowList[1]
    collect = fourRowList[2]
    users = fourRowList[3]
    train = [play[:100], download[:100], collect[:100], users[:100]]
    test = [play[100:], download[100:], collect[100:], users[100:]]
    return train, test

dim = 3
artistsDict = utils.trimFileInCol(1, utils.songsFile)
for artistId in artistsDict.keys():
    resultPath = os.path.join(utils.resultPath, artistId)
    if not os.path.exists(resultPath):
        os.makedirs(resultPath)
    songsDict = getDataFromTxt(artistId)
    for songId, fourRowList in songsDict.items():
        train, test = splitDataset(fourRowList)
        XTrain, yTrain = makeDataset(fourRowList=train, insertDim=dim)
        XTest, yTest = makeDataset(fourRowList=test, insertDim=dim)
        svr = svm.SVR()
        para={'C':range(1,50,5)}
        clf=grid_search.GridSearchCV(svr,para)
        # clf.fit(XTrain, yTrain)
        yPredict=[]
        for XSub,ySub in zip(XTest,yTest):
            clf.fit(XTrain, yTrain)
            yPredict.extend(clf.predict([XSub]))
            XTrain.pop(0)
            XTrain.append(XSub)
            yTrain.pop(0)
            yTrain.append(ySub)
        rmse = np.sqrt(mean_squared_error(yTest,yPredict))
        plt.figure(figsize=(6, 4))
        yptag = plt.plot(yPredict, 'bo', yPredict, 'b-')
        yttag = plt.plot(yTest, 'ro', yTest, 'r-')
        plt.legend([yptag[1], yttag[1]], ['predict', 'test'])
        plt.xlabel('test days')
        plt.ylabel('counts')
        plt.title('song id:' + songId + '\n' + \
                  'RMSE:' + str(rmse))
        plt.savefig(os.path.join(resultPath, songId + ".png"))
        plt.clf()
        plt.close()