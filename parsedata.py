__author__ = 'zfh'
# coding:utf-8

from ArtistClass import Artist
from UserClass import User
import os
import utils
import cPickle

if os.path.exists(utils.resultPath):
    os.makedirs(utils.resultPath)

usersDict = utils.trimFileInCol(0, utils.usersFile)
usersObjectDict = utils.analyseUsers(usersDict)  # 分析用户活跃程度
with open(utils.usersPickleFile, 'w') as file:
    cPickle.dump(usersObjectDict, file)

artistsDict = utils.trimFileInCol(1, utils.songsFile)
with open(utils.artistsPickleFile, 'w') as file:
    cPickle.dump(artistsDict, file)

songsDict = utils.trimFileWithActiveUsers(1, utils.usersFile, usersObjectDict)  # 全部是活跃用户的记录
with open(utils.songsPickleFile, 'w') as file:
    cPickle.dump(songsDict, file)

# artistsDict = cPickle.load(open(utils.artistsPickleFile, 'r'))
# songsDict = cPickle.load(open(utils.songsPickleFile, 'r'))
for artistId, songsList in artistsDict.items():
    artist = Artist(artistId)
    artist.makeSongsOwned(songsList, songsDict)
    savePath = os.path.join(utils.resultPath, 'artists')
    if not os.path.exists(savePath):
        os.makedirs(savePath)
    artistFile = os.path.join(savePath, artistId + '.pkl')
    with open(artistFile, 'w') as file:
        cPickle.dump(artist, file)

# artistsDict = cPickle.load(open(utils.artistsPickleFile, 'r'))
# for artistId in artistsDict.keys():
#     artistFile = os.path.join(utils.allResultPath, 'result0502', artistId + '.pkl')
#     artist = cPickle.load(open(artistFile, 'r'))
#     artist.plotSongsOwned()
