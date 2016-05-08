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
        # 歌曲的时间轨迹
        self.__trace = np.array([[0 for __ in range(utils.days)] for __ in range(4)])  # 播放,下载,收藏,用户数量轨迹
        self.__percentInSongs = np.array([[0 for __ in range(utils.days)] for __ in range(4)], dtype=np.float)
        self.__mean = np.array([0, 0, 0, 0], dtype=np.float)  # 歌曲的p,d,c,u平均值

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
        self.__mean = np.mean(self.__trace, axis=1)
        return

    def makePopular(self, artistMean):
        threshold = 2
        actionMean = np.sum(self.__mean[:3])
        usersMean = self.__mean[3]
        play = self.__trace[0]
        noPlayDays = len(play[play == 0])
        if actionMean > threshold and usersMean > threshold and noPlayDays < utils.days / 3:
            if actionMean > np.sum(artistMean[:3]) and usersMean > artistMean[3]:
                self.__popular = True
            else:
                traceArray = np.array(self.__trace)
                actionArray = np.sum(traceArray[:3, :], axis=0)
                usersArray = traceArray[3, :]
                actionNonzeroMean = np.mean(actionArray[np.nonzero(actionArray)])
                usersNonzeroMean = np.mean(usersArray[np.nonzero(usersArray)])
                if actionNonzeroMean > threshold * 2 and usersNonzeroMean > threshold * 2:
                    self.__popular = True
        if self.__popular:
            savePath = os.path.join(utils.resultPath, 'popular songs')
            if not os.path.exists(savePath):
                os.makedirs(savePath)
            plt.figure(figsize=(8, 8))
            self.plotTrace([actionMean, usersMean, noPlayDays])
            plt.savefig(os.path.join(savePath, self.__id + ".png"))
            plt.close()
        return

    def makePercentInSongs(self, allSongs):
        thisSong = np.array(self.__trace, dtype=np.float)
        allSongs = np.array(allSongs, dtype=np.float)
        self.__percentInSongs = thisSong / allSongs
        self.__percentInSongs[self.__percentInSongs == np.nan] = 0
        self.__percentInSongs[self.__percentInSongs == np.inf] = 0

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
                  str(title[0]) + '-' + str(title[1]) + '-' + str(title[2]))

    def setTrace(self, trace):
        self.__trace = trace

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

    def getTrace(self):
        return self.__trace

    def getMean(self):
        return self.__mean

    def getPercentInSongs(self):
        return self.__percentInSongs
