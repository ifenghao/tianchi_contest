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
        self.__popular = True
        # 歌曲的时间轨迹
        self.__playTrace = [0 for __ in range(utils.days)]  # 播放轨迹
        self.__downloadTrace = [0 for __ in range(utils.days)]  # 下载轨迹
        self.__collectTrace = [0 for __ in range(utils.days)]  # 收藏轨迹
        self.__usersTrace = [0 for __ in range(utils.days)]  # 用户数量轨迹

    def makeTrace(self, songWithUsersList):
        if songWithUsersList == None:
            print 'empty song users list ' + self.__id
            return
        usersTrace = [set() for __ in range(utils.days)]
        for row in songWithUsersList:
            dateNum = utils.date2num(row[4])
            usersTrace[dateNum].add(row[0])
            if row[3] == '1':
                self.__playTrace[dateNum] += 1
            elif row[3] == '2':
                self.__downloadTrace[dateNum] += 1
            elif row[3] == '3':
                self.__collectTrace[dateNum] += 1
        self.__usersTrace = map(len, usersTrace)
        playSum = np.sum(self.__playTrace)
        downloadSum = np.sum(self.__downloadTrace)
        collectSum = np.sum(self.__collectTrace)
        usersSum = np.sum(self.__usersTrace)
        if (playSum <= 3 and downloadSum <= 3 and collectSum <= 3) or usersSum <= 3:
            self.__popular = False
        else:
            entropy = utils.entropy(self.__usersTrace)
            entropyMax = utils.entropy([1 for __ in range(utils.days)])
            percent = entropy / entropyMax
            usersTraceArray = np.array(self.__usersTrace)
            actionMean = np.mean(usersTraceArray[np.nonzero(usersTraceArray)])
            if actionMean <= 3 and percent < 0.3:
                self.__popular = False
        # if not self.__popular:
        #     entropy = utils.entropy(self.__usersTrace)
        #     entropyMax = utils.entropy([1 for __ in range(utils.days)])
        #     percent = entropy / entropyMax
        #     usersTraceArray = np.array(self.__usersTrace)
        #     actionMean = np.mean(usersTraceArray[np.nonzero(usersTraceArray)])
        #     savePath = os.path.join(utils.resultPath, 'unpopular songs')
        #     if os.path.exists(savePath):
        #         os.makedirs(savePath)
        #     plt.figure(figsize=(6, 4))
        #     self.plotTrace([entropy, percent, actionMean])
        #     plt.savefig(os.path.join(savePath, self.__id + ".png"))
        #     plt.close()
        return

    def plotTrace(self, title):
        p = plt.plot(self.__playTrace, 'bo', self.__playTrace, 'b-')
        d = plt.plot(self.__downloadTrace, 'ro', self.__downloadTrace, 'r-')
        c = plt.plot(self.__collectTrace, 'go', self.__collectTrace, 'g-')
        u = plt.plot(self.__usersTrace, 'yo', self.__usersTrace, 'y-')
        plt.legend([p[1], d[1], c[1], u[1]], ['play', 'download', 'collect', 'users'])
        plt.xlabel('days')
        plt.ylabel('counts')
        plt.title('songId:' + self.__id + '\n' + \
                  str(self.__issueTime) + '-' + str(self.__initPlay) + \
                  '-' + str(self.__language) + '-' + str(self.__popular) + '\n' + \
                  str(title[0]) + '-' + str(title[1]) + '-' + str(title[2]))

    def setTrace(self, trace):
        self.__playTrace = trace[0]
        self.__downloadTrace = trace[1]
        self.__collectTrace = trace[2]
        self.__usersTrace = trace[3]

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

    def getPlayTrace(self):
        return self.__playTrace

    def getDownTrace(self):
        return self.__downloadTrace

    def getCollectTrace(self):
        return self.__collectTrace

    def getUsersTrace(self):
        return self.__usersTrace
