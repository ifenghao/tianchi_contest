__author__ = 'zfh'
# coding:utf-8

from ArtistClass import Artist
from UserClass import User
import os
import utils
import cPickle
import numpy as np

if not os.path.exists(utils.resultPath):
    os.makedirs(utils.resultPath)

# usersDict = utils.trimFileInCol(0, utils.usersFile)
# usersObjectDict = utils.analyseUsers(usersDict)  # 分析用户活跃程度，包含所有用户
# with open(utils.usersPickleFile, 'w') as file:
#     cPickle.dump(usersObjectDict, file)

# usersObjectDict = cPickle.load(open(utils.usersPickleFile, 'r'))
# utils.plotInactiveUsers(usersObjectDict)

# artistsDict = utils.trimFileInCol(1, utils.songsFile)
# with open(utils.artistsPickleFile, 'w') as file:
#     cPickle.dump(artistsDict, file)
#
# songsDict = utils.trimFileWithActiveUsers(1, utils.usersFile, usersObjectDict)  # 字典中全部是活跃用户的记录
# with open(utils.songsPickleFile, 'w') as file:
#     cPickle.dump(songsDict, file)

artistsDict = cPickle.load(open(utils.artistsPickleFile, 'r'))
songsDict = cPickle.load(open(utils.songsPickleFile, 'r'))
artistsObjectDict = {}
artistsTotalTrace = np.array([[0. for __ in range(utils.days)] for __ in range(4)])
for artistId, songsList in artistsDict.items():
    artist = Artist(artistId)
    artist.makeSongsOwned(songsList, songsDict)
    artist.combineUnpopularSongs()
    artist.makeTotalCumulateEA()
    artistsObjectDict[artistId] = artist
    artistsTotalTrace += artist.getTotalTrace()

for artistId, artist in artistsObjectDict.items():  # 生成每个歌手占所有歌手比例的轨迹
    artist.makePercentInArtists(artistsTotalTrace)

savePath = utils.resultPath
if not os.path.exists(savePath):
    os.makedirs(savePath)
artistFile = os.path.join(savePath, 'artistsObjectDict.pkl')
with open(artistFile, 'w') as file:
    cPickle.dump(artistsObjectDict, file)

# artistFile = os.path.join(utils.resultPath, 'artistsObjectDict.pkl')
# artistsObjectDict = cPickle.load(open(artistFile, 'r'))
# for artistId,artist in artistsObjectDict.items():
#     artist.plotSongsOwned()
