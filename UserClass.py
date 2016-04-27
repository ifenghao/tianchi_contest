__author__ = 'zfh'
# coding:UTF-8
import os
import utils
from UserActionClass import UserAction


class User(object):
    def __init__(self, userId):
        self.__id = userId
        self.__isActive = False
        self.__playSum = 0
        self.__downloadSum = 0
        self.__collectSum = 0
        self.__songsTriedNumber = 0
        self.__songsTried = {}  # 用户尝试过的所有歌曲 key=歌曲ID:value=用户行为

    def makeSongsTried(self, usersDict):
        songs = {}
        userWithSongsList = usersDict.get(self.__id, None)
        if userWithSongsList == None:
            print 'no such user ' + self.__id
        else:
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
        return

    def saveSongsTried(self):
        resultFilePath = os.path.join(utils.resultPath, 'users')
        if not os.path.exists(resultFilePath):
            os.makedirs(resultFilePath)
        resultFile = os.path.join(resultFilePath, self.__id + '.txt')
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

    def setActive(self):
        self.__isActive = True

    def isActive(self):
        return self.__isActive
