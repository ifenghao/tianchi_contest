__author__ = 'zfh'
# coding:utf-8

from ArtistClass import Artist
from UserClass import User
import os
import utils

# artistsDict = utils.trimFileInCol(1, utils.songsFile)
# songsDict = utils.trimFileInCol(1, utils.usersFile)
# usersDict = utils.trimFileInCol(0, utils.usersFile)
# usersObjectDict = utils.analyseUsers(usersDict)# 分析用户活跃程度
# for artistId in artistsDict.keys():
#     artist = Artist(artistId)
#     artist.makeSongsOwned(artistsDict, songsDict)
#     artist.saveSongsOwned()
#     utils.plotArtistSongsTrace(artistId)

usersDict = utils.trimFileInCol(0, utils.usersFile)
resultFilePath = os.path.join(utils.resultPath, 'users')
if not os.path.exists(resultFilePath):
    os.makedirs(resultFilePath)
songsResultFile = os.path.join(resultFilePath, 'songs.txt')
traceResultFile = os.path.join(resultFilePath, 'trace.txt')
inactiveUserCount=0
with open(songsResultFile, 'w') as songsFile:
    with open(traceResultFile, 'w') as traceFile:
        for userId in usersDict.keys():
            user = User(userId)
            user.makeSongsTried(usersDict)
            if user.isActive():
                user.saveSongsTried(songsFile)
                user.saveSongsTriedTrace(traceFile)
            else:
                usersDict.pop(userId)
                inactiveUserCount+=1
print 'inactive user number: '+inactiveUserCount
