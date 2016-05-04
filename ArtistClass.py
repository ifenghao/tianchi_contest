__author__ = 'zfh'
# coding:utf-8
import utils
from SongClass import Song
import os
import matplotlib.pyplot as plt
import numpy as np


class Artist(object):
    def __init__(self, artistId):
        self.__id = artistId
        self.__gender = 0
        self.__totalMean = [0., 0., 0., 0.]  # p,d,c,u平均值
        self.__songsOwned = {}  # 歌曲字典 key=歌曲ID:value=歌曲类

    def makeSongsOwned(self, songsList, songsDict):
        if songsList == None:
            print 'empty songs list ' + self.__id
            return
        songs = {}
        for row in songsList:
            songId = row[0]
            newSong = Song(songId, row)
            songWithUsersList = songsDict.get(songId, None)
            newSong.makeTrace(songWithUsersList)
            songs[songId] = newSong
            self.__totalMean = [i + j for i, j in zip(self.__totalMean, newSong.getMean())]
        self.__gender = songsList[0][5]
        self.__songsOwned = songs
        self.__totalMean = [float(i) / len(self.__songsOwned) for i in self.__totalMean]
        return

    def determinePopularSongs(self):
        count = 0
        for songId, song in self.__songsOwned.items():
            song.makePopular(self.__totalMean)
            if song.getPopular():
                count += 1
        print 'popular songs ' + str(count) + '/' + str(len(self.__songsOwned))

    def combineUnpopularSongs(self):
        playTrace = [0 for __ in range(utils.days)]
        downloadTrace = [0 for __ in range(utils.days)]
        collectTrace = [0 for __ in range(utils.days)]
        userTrace = [0 for __ in range(utils.days)]
        totalSongs = len(self.__songsOwned)
        combineSongs = 0
        for songId, song in self.__songsOwned.items():
            if not song.getPopular():
                playTrace = [i + j for i, j in zip(playTrace, song.getPlayTrace())]
                downloadTrace = [i + j for i, j in zip(downloadTrace, song.getDownTrace())]
                collectTrace = [i + j for i, j in zip(collectTrace, song.getCollectTrace())]
                userTrace = [i + j for i, j in zip(userTrace, song.getUsersTrace())]
                self.__songsOwned.popitem()
                combineSongs += 1
        print 'combine:' + str(combineSongs) + '/' + str(totalSongs)
        unpopularSongsGroup = Song('unpopularSongsGroup', [0, 0, 0, 0, 0])
        unpopularSongsGroup.setPopular(False)
        unpopularSongsGroup.setTrace([playTrace, downloadTrace, collectTrace, userTrace])
        self.__songsOwned['unpopularSongsGroup'] = unpopularSongsGroup

    def plotSongsOwned(self):
        savePath = os.path.join(utils.resultPath, self.__id)
        if os.path.exists(savePath):
            os.makedirs(savePath)
        for songId, song in self.__songsOwned.items():
            plt.figure(figsize=(6, 4))
            song.plotTrace()
            plt.savefig(os.path.join(savePath, songId + "--.png"))
            plt.close()

    def getSongsOwned(self):
        return self.__songsOwned
