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
        self.__songsOwned = {}  # 歌曲字典 key=歌曲ID:value=歌曲类
        # 所有歌曲总和的时间轨迹
        self.__totalTrace = np.array([[0 for __ in range(utils.days)] for __ in range(4)])  # 播放,下载,收藏,用户数量轨迹
        self.__percentInArtists = np.array([[0 for __ in range(utils.days)] for __ in range(4)], dtype=np.float)
        self.__totalMean = np.array([0, 0, 0, 0], dtype=np.float)  # p,d,c,u平均值

    def makeSongsOwned(self, songsList, songsDict):
        if songsList == None:
            print 'empty songs list ' + self.__id
            return
        songs = {}
        totalTrace = np.array(self.__totalTrace)
        for row in songsList:  # 生成每首歌的轨迹
            songId = row[0]
            newSong = Song(songId, row)
            songWithUsersList = songsDict.get(songId, None)
            newSong.makeTrace(songWithUsersList)
            songs[songId] = newSong
            totalTrace += newSong.getTrace()
        for songId, song in songs.items():  # 生成每首歌占本歌手总歌曲比例的轨迹
            song.makePercentInSongs(totalTrace)
        self.__gender = songsList[0][5]
        self.__songsOwned = songs
        self.__totalTrace = totalTrace
        self.__totalMean = np.mean(self.__totalTrace, axis=1)
        return

    def determinePopularSongs(self):
        count = 0
        for songId, song in self.__songsOwned.items():
            song.makePopular(self.__totalMean)
            if song.getPopular():
                count += 1
        print 'popular songs ' + str(count) + '/' + str(len(self.__songsOwned))

    def combineUnpopularSongs(self):
        unpopularSongsTrace = np.array([[0 for __ in range(utils.days)] for __ in range(4)])
        totalSongs = len(self.__songsOwned)
        combineSongs = 0
        for songId, song in self.__songsOwned.items():
            if not song.getPopular():
                unpopularSongsTrace += song.getTrace()
                self.__songsOwned.pop(songId)
                combineSongs += 1
        print 'combine:' + str(combineSongs) + '/' + str(totalSongs)
        unpopularSongs = Song('unpopularSongsGroup', [0, 0, 0, 0, 0])
        unpopularSongs.setPopular(False)
        unpopularSongs.setTrace(unpopularSongsTrace)
        self.__songsOwned['unpopularSongsGroup'] = unpopularSongs

    def makePercentInArtists(self, allArtists):
        thisArtist = np.array(self.__totalTrace, dtype=np.float)
        allArtists = np.array(allArtists, dtype=np.float)
        self.__percentInArtists = thisArtist / allArtists
        self.__percentInArtists[self.__percentInArtists == np.nan] = 0
        self.__percentInArtists[self.__percentInArtists == np.inf] = 0

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

    def getTotalTrace(self):
        return self.__totalTrace

    def getPercentInArtists(self):
        return self.__percentInArtists
