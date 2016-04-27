__author__ = 'zfh'
# coding:utf-8

from ArtistClass import Artist
from UserClass import User
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
for userId in usersDict.keys():
    user = User(userId)
    user.makeSongsTried(usersDict)
    user.saveSongsTried()
    utils.plotUserSongsRecord(userId)
