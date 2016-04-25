__author__ = 'zfh'
# coding:utf-8
import utils
from SongClass import Song
import os


class Artist(object):
    def __init__(self, artistId):
        self.__id = artistId
        self.__gender = 0
        self.__songsSet = set()  # 整理出的每天歌曲的播放，下载，收藏数据

    def makeSongsSet(self, artistsDict, songsDict):
        songs = set()
        songsList = artistsDict.get(self.__id, None)
        if songsList == None:
            print 'no such aritist ' + self.__id
            return
        for row in songsList:
            songId = row[0]
            newSong = Song(songId, row)
            usersList = songsDict.get(songId, None)
            newSong.makeTrace(usersList)
            songs.add(newSong)
        self.__gender = songsList[0][5]
        self.__songsSet = songs
        return

    def saveSongsSet(self):
        resultFilePath = os.path.join(utils.resultPath, self.__id)
        if not os.path.exists(resultFilePath):
            os.makedirs(resultFilePath)
        resultFile = os.path.join(resultFilePath, 'statistics.txt')
        with open(resultFile, 'w') as file:
            playSum = [0 for i in range(utils.days)]
            downloadSum = [0 for i in range(utils.days)]
            collectSum = [0 for i in range(utils.days)]
            usersSum = [0 for i in range(utils.days)]
            for song in self.__songsSet:
                trace = song.getTrace()
                if trace == []:
                    print 'skip song ' + song.getId()
                    continue
                file.write(song.getId() + '\n')
                file.write(song.getIssueTime() + '\n')
                file.write(song.getInitPlay() + '\n')
                file.write(song.getLanguage() + '\n')
                play = [trace[i].play for i in range(utils.days)]
                download = [trace[i].download for i in range(utils.days)]
                collect = [trace[i].collect for i in range(utils.days)]
                users = [len(trace[i].users) for i in range(utils.days)]
                file.write(','.join(map(str, play)) + '\n')
                file.write(','.join(map(str, download)) + '\n')
                file.write(','.join(map(str, collect)) + '\n')
                file.write(','.join(map(str, users)) + '\n')
                playSum = [i + j for i, j in zip(play, playSum)]
                downloadSum = [i + j for i, j in zip(download, downloadSum)]
                collectSum = [i + j for i, j in zip(collect, collectSum)]
                usersSum = [i + j for i, j in zip(users, usersSum)]
            file.write('sum' + '\n')
            file.write('00' + '\n')
            file.write('00' + '\n')
            file.write('00' + '\n')
            file.write(','.join(map(str, playSum)) + '\n')
            file.write(','.join(map(str, downloadSum)) + '\n')
            file.write(','.join(map(str, collectSum)) + '\n')
            file.write(','.join(map(str, usersSum)) + '\n')
