__author__ = 'zfh'
# coding:utf-8
import utils
import os
import numpy as np
import matplotlib.pyplot as plt


class Song(object):
    def __init__(self, songId, infoList):
        self.__id = songId
        self.__issueTime = infoList[2]
        self.__initPlay = infoList[3]
        self.__language = infoList[4]
        self.__popular = False
        self.__emptyDays = 0
        # 歌曲的时间轨迹，仅保留发行后的时间轨迹，发行前的空余将剔除
        self.__trace = np.zeros((4, utils.days))  # 播放,下载,收藏,用户数量轨迹
        self.__percentInSongs = np.zeros((4, utils.days))
        self.__cumulateEA = np.zeros(utils.days)
        self.__mean = np.zeros(4)  # 歌曲的p,d,c,u平均值

    def makeTrace(self, songWithUsersList):
        if songWithUsersList == None:
            print 'empty song users list ' + self.__id
            return
        usersTrace = [set() for __ in range(utils.days)]
        for row in songWithUsersList:
            dateNum = utils.date2num(row[4])
            usersTrace[dateNum].add(row[0])
            if row[3] == '1':
                self.__trace[0][dateNum] += 1
            elif row[3] == '2':
                self.__trace[1][dateNum] += 1
            elif row[3] == '3':
                self.__trace[2][dateNum] += 1
        self.__trace[3] = map(len, usersTrace)
        issueTimeNum = utils.date2num(self.__issueTime)
        if issueTimeNum > 0:
            users = np.array(self.__trace[3])
            self.__emptyDays = np.where(users != 0)[0][0]  # 第一天有用户活动
            self.__trace = self.__trace[:, self.__emptyDays:]

    def makeMean(self):
        self.__mean = np.mean(self.__trace, axis=1)

    def makePopular(self, artistMean):
        threshold = 1
        actionMean = np.sum(self.__mean[:3])
        usersMean = self.__mean[3]
        if actionMean >= threshold and usersMean >= threshold / 2:
            if actionMean >= np.sum(artistMean[:3]) and usersMean >= artistMean[3]:
                self.__popular = True
            else:
                traceArray = np.array(self.__trace)
                actionArray = np.sum(traceArray[:3, :], axis=0)
                usersArray = traceArray[3, :]
                actionNonzeroMean = np.mean(actionArray[np.nonzero(actionArray)])
                usersNonzeroMean = np.mean(usersArray[np.nonzero(usersArray)])
                if actionNonzeroMean >= threshold * 2 and usersNonzeroMean >= threshold:
                    self.__popular = True
                    # if self.__popular:
                    #     savePath = os.path.join(utils.resultPath, 'popular songs')
                    #     if not os.path.exists(savePath):
                    #         os.makedirs(savePath)
                    #     plt.figure(figsize=(8, 8))
                    #     self.plotTrace([actionMean, usersMean, np.sum(artistMean[:3]), artistMean[3]])
                    #     plt.savefig(os.path.join(savePath, self.__id + ".png"))
                    #     plt.close()

    def makePercentInSongs(self, allSongs):
        thisSong = np.array(self.__trace, dtype=np.float)
        allSongs = np.array(allSongs, dtype=np.float)
        self.__percentInSongs = thisSong / allSongs[:, self.__emptyDays:]
        self.__percentInSongs[np.isnan(self.__percentInSongs)] = 0
        self.__percentInSongs[np.isinf(self.__percentInSongs)] = 0

    def makeCumulateEA(self):
        cumulateEA = []
        play = np.array(self.__trace[0])
        initPlay = float(self.__initPlay)
        issueTimeNum = utils.date2num(self.__issueTime)
        cumulateList = []
        w = []
        if issueTimeNum < 0:  # 发行时间在之前
            cumulateList = [initPlay / np.abs(issueTimeNum)] + cumulateList  # 已发行平均播放作第一个元素
            w.append(1)
        for i in range(len(play)):
            cumulateList = [play[i]] + cumulateList
            w.append(2.0 / (1 + len(cumulateList)))
            cumulateEA.append(np.average(cumulateList, weights=w))
        self.__cumulateEA = np.array(cumulateEA)

    def plotTrace(self, title):
        p = plt.plot(self.__trace[0], 'bo', self.__trace[0], 'b-')
        d = plt.plot(self.__trace[1], 'ro', self.__trace[1], 'r-')
        c = plt.plot(self.__trace[2], 'go', self.__trace[2], 'g-')
        u = plt.plot(self.__trace[3], 'yo', self.__trace[3], 'y-')
        plt.legend([p[1], d[1], c[1], u[1]], ['play', 'download', 'collect', 'users'])
        plt.xlabel('days')
        plt.ylabel('counts')
        plt.title('songId:' + self.__id + '\n' + \
                  str(self.__issueTime) + '-' + str(self.__initPlay) + \
                  '-' + str(self.__language) + '-' + str(self.__popular) + '\n' + \
                  str(title[0]) + '-' + str(title[1]) + '-' + str(title[2]) + '-' + str(title[3]))

    def setTrace(self, trace):
        self.__trace = trace
        self.__emptyDays = utils.days - trace.shape[1]

    def setCumulateEA(self, cumulateEA):
        self.__cumulateEA = cumulateEA

    def setPercentInSongs(self, percentInSongs):
        self.__percentInSongs = percentInSongs

    def setPopular(self, bool):
        self.__popular = bool

    def getId(self):
        return self.__id

    def getIssueTime(self):
        return self.__issueTime

    def getInitPlay(self):
        return self.__initPlay

    def getLanguage(self):
        return self.__language

    def getPopular(self):
        return self.__popular

    def getEmptyDays(self):
        return self.__emptyDays

    def getTrace(self):
        return self.__trace

    def getMean(self):
        return self.__mean

    def getPercentInSongs(self):
        return self.__percentInSongs

    def getCumulateEA(self):
        return self.__cumulateEA
