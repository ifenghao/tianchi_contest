__author__ = 'zfh'
# coding:UTF-8
import os
import utils
import numpy as np
import matplotlib.pyplot as plt


class User(object):
    def __init__(self, userId):
        self.__id = userId
        self.__isActive = True
        self.__songsTried = {}  # 用户尝试过的所有歌曲 key=歌曲ID:value=用户行为(聚类依据)
        self.__actonTrace = np.array([0 for __ in range(utils.days)])  # 用户活动的时间轨迹 每天用户行为求和(判断活跃度依据)

    def makeSongsTried(self, userWithSongsList):
        songs = {}
        for row in userWithSongsList:
            songId = row[1]
            if songId not in songs:
                songs[songId] = [0, 0, 0]  # 分别是播放，下载，收藏
            actionList = songs.get(songId)
            if row[3] == '1':
                actionList[0] += 1
            elif row[3] == '2':
                actionList[1] += 1
            elif row[3] == '3':
                actionList[2] += 1
        self.__songsTried = songs
        for row in userWithSongsList:
            dateNum = utils.date2num(row[4])
            self.__actonTrace[dateNum] += 1
        playSum, downloadSum, collectSum = self.sumAction()
        songsSum = len(self.__songsTried)
        if playSum <= 3 and downloadSum <= 3 and collectSum <= 3 and songsSum <= 3:
            self.__isActive = False  # 过于不活跃的用户
        else:
            entropy = utils.entropy(self.__actonTrace)
            entropyMax = utils.entropy([1 for __ in range(utils.days)])
            percent = entropy / entropyMax
            actionTrace = np.array(self.__actonTrace)
            actionMean = np.mean(actionTrace[np.nonzero(actionTrace)])
            if actionMean <= 3 and percent < 0.2:
                self.__isActive = False
        # if not self.__isActive:
        #     entropy = utils.entropy(self.__actonTrace)
        #     entropyMax = utils.entropy([1 for __ in range(utils.days)])
        #     percent = entropy / entropyMax
        #     actionTrace = np.array(self.__actonTrace)
        #     actionMean = np.mean(actionTrace[np.nonzero(actionTrace)])
        #     savePath = os.path.join(utils.resultPath, 'inactive users')
        #     if os.path.exists(savePath):
        #         os.makedirs(savePath)
        #     plt.figure(figsize=(6, 4))
        #     self.plotSongsTried([entropy, percent, actionMean])
        #     plt.savefig(os.path.join(savePath, self.__id + "songs.png"))
        #     plt.clf()
        #     self.plotSongsTriedTrace([entropy, percent, actionMean])
        #     plt.savefig(os.path.join(savePath, self.__id + "trace.png"))
        #     plt.close()
        return

    def sumAction(self):
        playSum = 0
        downloadSum = 0
        collectSum = 0
        for songId, actionList in self.__songsTried.items():
            playSum += actionList[0]
            downloadSum += actionList[1]
            collectSum += actionList[2]
        return playSum, downloadSum, collectSum

    def plotSongsTried(self, title):
        play = []
        download = []
        collect = []
        for songId, actionList in self.__songsTried.items():
            play.append(actionList[0])
            download.append(actionList[1])
            collect.append(actionList[2])
        plt.figure(figsize=(6, 4))
        p = plt.plot(play, 'bo', play, 'b-')
        d = plt.plot(download, 'ro', download, 'r-')
        c = plt.plot(collect, 'go', collect, 'g-')
        plt.legend([p[1], d[1], c[1]], ['play', 'download', 'collect'])
        plt.xlabel('songs')
        plt.ylabel('counts')
        plt.title('total songs:' + str(len(self.__songsTried)) + '\n' + \
                  str(title[0]) + '-' + str(title[1]) + '-' + str(title[2]) + '-' + str(self.__isActive))

    def plotSongsTriedTrace(self, title):
        plt.figure(figsize=(6, 4))
        plt.plot(self.__actonTrace, 'bo', self.__actonTrace, 'b-')
        plt.xlabel('days')
        plt.ylabel('counts')
        plt.title('user:' + str(self.__id) + '\n' + \
                  str(title[0]) + '-' + str(title[1]) + '-' + str(title[2]) + '-' + str(self.__isActive))

    def isActive(self):
        return self.__isActive
