__author__ = 'zfh'
# coding:UTF-8
import os
import utils
import matplotlib.pyplot as plt
from UserActionClass import UserAction


class User(object):
    def __init__(self, userId):
        self.__id = userId
        self.__isActive = True
        self.__activeDegree = 0
        self.__playSum = 0
        self.__downloadSum = 0
        self.__collectSum = 0
        self.__songsTriedNumber = 0
        self.__songsTried = {}  # 用户尝试过的所有歌曲 key=歌曲ID:value=用户行为(聚类依据)
        self.__songsTriedTrace = []  # 用户尝试歌曲的时间轨迹 每天用户行为(判断活跃度依据)

    def makeSongsTried(self, usersDict):
        songs = {}
        userWithSongsList = usersDict.get(self.__id, None)
        for row in userWithSongsList:
            songId = row[1]
            if songId not in songs:
                songs[songId] = UserAction()
            userAction = songs.get(songId)
            if row[3] == '1':
                userAction.increasePlay()
                self.__playSum += 1
            elif row[3] == '2':
                userAction.increaseDownload()
                self.__downloadSum += 1
            elif row[3] == '3':
                userAction.increaseCollect()
                self.__collectSum += 1
        self.__songsTriedNumber = len(songs)
        self.__songsTried = songs
        if self.__songsTriedNumber <= 3 and self.__playSum <= 3 and \
                        self.__downloadSum <= 3 and self.__collectSum <= 3:
            self.__isActive = False  # 过于不活跃的用户
            return
        trace = [UserAction() for i in range(utils.days)]
        for row in userWithSongsList:
                dateNum = utils.date2num(row[4])
                userAction = trace[dateNum]
                if row[3] == '1':
                    userAction.increasePlay()
                elif row[3] == '2':
                    userAction.increaseDownload()
                elif row[3] == '3':
                    userAction.increaseCollect()
        self.__songsTriedTrace = trace
        return

    def saveSongsTried(self):
        if not self.__isActive:
            return
        resultFilePath = os.path.join(utils.resultPath, 'users')
        if not os.path.exists(resultFilePath):
            os.makedirs(resultFilePath)
        resultFile = os.path.join(resultFilePath, 'songs ' + self.__id + '.txt')
        with open(resultFile, 'w') as file:
            for songId, userAction in self.__songsTried.items():
                file.write(songId + '\n')
                file.write(str(userAction.getPlay()) + '\n')
                file.write(str(userAction.getDownload()) + '\n')
                file.write(str(userAction.getCollect()) + '\n')
            file.write('sum:' + '\n')
            file.write(str(self.__songsTriedNumber) + '\n')
            file.write(str(self.__playSum) + '\n')
            file.write(str(self.__downloadSum) + '\n')
            file.write(str(self.__collectSum) + '\n')

    def plotUserSongsRecord(self):
        resultFilePath = os.path.join(utils.resultPath, 'users')
        if not os.path.exists(resultFilePath):
            os.makedirs(resultFilePath)
        play = []
        download = []
        collect = []
        for songId, userAction in self.__songsTried.items():
            play.append(userAction.getPlay())
            download.append(userAction.getDownload())
            collect.append(userAction.getCollect())
        plt.figure(figsize=(6, 4))
        p = plt.plot(play, 'bo', play, 'b-')
        d = plt.plot(download, 'ro', download, 'r-')
        c = plt.plot(collect, 'go', collect, 'g-')
        plt.legend([p[1], d[1], c[1]], ['play', 'download', 'collect'])
        plt.xlabel('songs')
        plt.ylabel('counts')
        plt.title('songs:' + str(self.__songsTriedNumber) + '\n' + \
                  str(self.__playSum) + '-' + str(self.__downloadSum) + '-' + str(self.__collectSum))
        plt.savefig(os.path.join(resultFilePath, 'songs ' + self.__id + ".png"))
        plt.clf()

    def saveSongsTriedTrace(self):
        if not self.__isActive:
            return
        resultFilePath = os.path.join(utils.resultPath, 'users')
        if not os.path.exists(resultFilePath):
            os.makedirs(resultFilePath)
        resultFile = os.path.join(resultFilePath, 'trace ' + self.__id + '.txt')
        with open(resultFile, 'w') as file:
            for userAction in self.__songsTriedTrace:
                file.write(str(userAction.getPlay()) + '\n')
                file.write(str(userAction.getDownload()) + '\n')
                file.write(str(userAction.getCollect()) + '\n')

    def plotUserSongsTriedTrace(self):
        resultFilePath = os.path.join(utils.resultPath, 'users')
        if not os.path.exists(resultFilePath):
            os.makedirs(resultFilePath)
        play = []
        download = []
        collect = []
        for userAction in self.__songsTriedTrace:
            play.append(userAction.getPlay())
            download.append(userAction.getDownload())
            collect.append(userAction.getCollect())
        plt.figure(figsize=(6, 4))
        p = plt.plot(play, 'bo', play, 'b-')
        d = plt.plot(download, 'ro', download, 'r-')
        c = plt.plot(collect, 'go', collect, 'g-')
        plt.legend([p[1], d[1], c[1]], ['play', 'download', 'collect'])
        plt.xlabel('days')
        plt.ylabel('counts')
        plt.title('user:' + str(self.__id))
        plt.savefig(os.path.join(resultFilePath, 'trace ' + self.__id + ".png"))
        plt.clf()

    def isActive(self):
        return self.__isActive
