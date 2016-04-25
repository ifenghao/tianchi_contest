__author__ = 'zfh'
# coding:utf-8

from ArtistClass import Artist
import utils

artistsDict = utils.trimFileInCol(1, utils.songsFile)
songsDict = utils.trimFileInCol(1, utils.usersFile)
for artistId in artistsDict.keys():
    artist = Artist(artistId)
    artist.makeSongsSet(artistsDict, songsDict)
    artist.saveSongsSet()
    utils.plotSongsTrace(artistId)
