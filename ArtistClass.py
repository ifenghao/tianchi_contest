__author__ = 'zfh'
# coding:utf-8
import utils
from SongClass import Song
import os
import matplotlib.pyplot as plt


class Artist(object):
    def __init__(self, artistId):
        self.__id = artistId
        self.__gender = 0
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
        self.__gender = songsList[0][5]
        self.__songsOwned = songs
        return

    def conbineUnpopularSongs(self):
        playTrace = [0 for __ in range(utils.days)]
        downloadTrace = [0 for __ in range(utils.days)]
        collectTrace = [0 for __ in range(utils.days)]
        userTrace = [0 for __ in range(utils.days)]
        for songId, song in self.__songsOwned.items():
            if not song.getPopular():
                playTrace = [i + j for i, j in zip(playTrace, song.getPlayTrace())]
                downloadTrace = [i + j for i, j in zip(downloadTrace, song.getDownTrace())]
                collectTrace = [i + j for i, j in zip(collectTrace, song.getCollectTrace())]
                userTrace = [i + j for i, j in zip(userTrace, song.getUsersTrace())]
                self.__songsOwned.popitem()
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
