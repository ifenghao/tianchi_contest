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
        self.__totalTrace = np.zeros((4, utils.days))  # 播放,下载,收藏,用户数量轨迹
        self.__percentInArtists = np.zeros((4, utils.days))
        self.__totalCumulateEA = np.zeros(utils.days)
        self.__totalMean = np.zeros(4)  # p,d,c,u平均值

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
            newSong.makeMean()
            newSong.makeCumulateEA()
            songs[songId] = newSong
            songTrace = newSong.getTrace()
            emptyDays = utils.days - songTrace.shape[1]
            totalTrace += np.hstack((np.zeros((4, emptyDays)), songTrace))
        self.__gender = songsList[0][5]
        self.__songsOwned = songs
        self.__totalTrace = totalTrace
        self.__totalMean = np.mean(totalTrace, axis=1)
        count = 0
        for songId, song in self.__songsOwned.items():  # 生成每首歌占本歌手总歌曲比例的轨迹
            song.makePercentInSongs(self.__totalTrace)
            song.makePopular(self.__totalMean)
            if song.getPopular():
                count += 1
        print 'popular songs ' + str(count) + '/' + str(len(self.__songsOwned))

    def combineUnpopularSongs(self):
        unpopularSongsTrace = np.zeros((4, utils.days))
        unpopularSongsCumulateEA = np.zeros(utils.days)
        totalSongs = len(self.__songsOwned)
        combineSongs = 0
        for songId, song in self.__songsOwned.items():
            if not song.getPopular():
                songTrace = song.getTrace()
                songCumulateEA = song.getCumulateEA()
                emptyDays = utils.days - songTrace.shape[1]
                unpopularSongsTrace += np.hstack((np.zeros((4, emptyDays)), songTrace))
                unpopularSongsCumulateEA += np.hstack((np.zeros(emptyDays), songCumulateEA))
                self.__songsOwned.pop(songId)
                combineSongs += 1
        print 'combine:' + str(combineSongs) + '/' + str(totalSongs)
        unpopularSongs = Song('unpopularSongsGroup', [0, 0, 0, 0, 0])
        unpopularSongs.setTrace(unpopularSongsTrace)
        unpopularSongs.setCumulateEA(unpopularSongsCumulateEA)
        unpopularSongs.makeMean()
        unpopularSongs.makePercentInSongs(self.__totalTrace)
        unpopularSongs.setPopular(False)
        self.__songsOwned['unpopularSongsGroup'] = unpopularSongs

    def makePercentInArtists(self, allArtists):
        thisArtist = np.array(self.__totalTrace, dtype=np.float)
        allArtists = np.array(allArtists, dtype=np.float)
        self.__percentInArtists = thisArtist / allArtists
        self.__percentInArtists[np.isnan(self.__percentInArtists)] = 0
        self.__percentInArtists[np.isinf(self.__percentInArtists)] = 0

    def makeTotalCumulateEA(self):
        for songId, song in self.__songsOwned.items():
            songCumulateEA = song.getCumulateEA()
            emptyDays = utils.days - songCumulateEA.shape[0]
            self.__totalCumulateEA += np.hstack(((np.zeros(emptyDays), songCumulateEA)))

    def plotSongsOwned(self):
        savePath = os.path.join(utils.resultPath, self.__id)
        if not os.path.exists(savePath):
            os.makedirs(savePath)
        for songId, song in self.__songsOwned.items():
            plt.figure(figsize=(6, 4))
            song.plotTrace([0,0,0])
            plt.savefig(os.path.join(savePath, songId + "--.png"))
            plt.close()

    def getSongsOwned(self):
        return self.__songsOwned

    def getTotalTrace(self):
        return self.__totalTrace

    def getTotalCumulateEA(self):
        return self.__totalCumulateEA

    def getPercentInArtists(self):
        return self.__percentInArtists
