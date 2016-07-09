__author__ = 'zfh'
# coding:utf-8
import time, os
import csv
import numpy as np
import matplotlib.pyplot as plt
from UserClass import User
from SongClass import Song
from sklearn import cluster

startTime = int(time.mktime(time.strptime('20150301', '%Y%m%d')))
predictTime = int(time.mktime(time.strptime('20150901', '%Y%m%d')))
secondsPerDay = 86400
days = 183
currentPath = os.getcwd()
usersFileName = 'p2_mars_tianchi_user_actions.csv'
usersFile = os.path.join('/home/zhufenghao', 'dataset', usersFileName)
songsFileName = 'p2_mars_tianchi_songs.csv'
songsFile = os.path.join('/home/zhufenghao', 'dataset', songsFileName)

resultPath = os.path.join(currentPath, 'result')
allResultPath = os.path.join('/home/zfh', 'allresults')

usersPickleFileName = 'usersObjectDict.pkl'
usersPickleFile = os.path.join('/home/zhufenghao', 'dataset', usersPickleFileName)

songsPickleFileName = 'songsDict.pkl'
songsPickleFile = os.path.join('/home/zhufenghao', 'dataset', songsPickleFileName)

artistsPickleFileName = 'artistsDict.pkl'
artistsPickleFile = os.path.join('/home/zhufenghao', 'dataset', artistsPickleFileName)


def searchKeyInFile(key, fileName):
    '''
    返回文件中包含键值的所有行所构成的列表
    '''
    list = []
    with open(fileName) as file:
        rowReader = csv.reader(file, delimiter=',')
        for row in rowReader:
            if key in row:
                list.append(row)
    return list


def trimFileInCol(col, fileName):
    '''
    按照某关键列整理文件，将包含此关键列的内容到字典中
    key=列元素:value=有关此列的列表
    '''
    dict = {}
    with open(fileName) as file:
        rowReader = csv.reader(file, delimiter=',')
        for row in rowReader:
            if not dict.has_key(row[col]):
                dict[row[col]] = []
            list = dict[row[col]]
            list.append(row)
    return dict


def trimFileWithActiveUsers(col, usersFile, usersObjectDict):
    '''
    按照用户整理文件，将包含此关键列的内容到字典中，将不活跃用户剔除
    key=列元素:value=有关此列的列表
    '''
    dict = {}
    with open(usersFile) as file:
        rowReader = csv.reader(file, delimiter=',')
        for row in rowReader:
            user = usersObjectDict.get(row[0])
            if not user.isActive():
                continue
            if not dict.has_key(row[col]):
                dict[row[col]] = []
            list = dict[row[col]]
            list.append(row)
    return dict


def analyseUsers(usersDict):
    '''
    分析所有用户的行为构建用户字典，判断其活跃与否
    key=用户ID:value=用户对象
    '''
    dict = {}
    for userId, userWithSongsList in usersDict.items():
        user = User(userId)
        user.makeSongsTried(userWithSongsList)
        dict[userId] = user
    return dict


def plotInactiveUsers(usersObjectDict):
    trace = np.zeros(days)
    for userId, userObject in usersObjectDict.items():
        if not userObject.isAcitve():
            trace += userObject.getActionTrace()
    plt.figure(figsize=(6, 4))
    plt.plot(trace, 'b-', trace, 'bo')
    plt.savefig(os.path.join(os.getcwd(), 'inactive users.png'))
    plt.close()


def date2num(date):
    return (int(time.mktime(time.strptime(date, '%Y%m%d'))) - startTime) // secondsPerDay


def num2date(num):
    return time.strftime('%Y%m%d', time.localtime(num * secondsPerDay + predictTime))


def entropy(countList):
    countList = np.array(map(float, countList))  # 转换为浮点型数组
    countList[countList == 0.] = 1e-10  # 所有0元素用1e-10代替，否则计算熵出错
    p = countList / float(np.sum(countList))
    return -np.sum(p * np.log2(p))


def normalizedVariation(yTrue, yPredict):
    normSquare = [((p - t) / t) ** 2 for t, p in zip(yTrue, yPredict)]
    return np.sqrt(np.mean(normSquare))


############################### cluster begin #################################
def clusterSongs(artist):
    clusterSongsList = []
    songsDict = monthSongDict(artist)
    for monthDate, monthSongsList in songsDict.items():
        if len(monthSongsList) == 1:
            clusterSongsList.extend(monthSongsList)
            continue
        clusterIndex, songsList = clusterAlgorithm(monthSongsList)
        clusterSongsList.extend(clusterWithIndex(clusterIndex, songsList))
    if len(clusterSongsList) == 1:
        return clusterSongsList
    clusterSongsList2 = []
    clusterIndex, songsList = clusterAlgorithm(clusterSongsList)
    clusterSongsList2.extend(clusterWithIndex(clusterIndex, songsList))
    return clusterSongsList2


def monthSongDict(artist):  # key=month value=[song]
    songsDict = {}
    if 'unpopularSongsGroup' in artist.getSongsOwned():
        unpopularSongs = artist.getSongsOwned().pop('unpopularSongsGroup')
        songsDict['000000'] = [unpopularSongs]
    for song in artist.getSongsOwned().values():
        issueTime = song.getIssueTime()
        monthDate = ''.join(list(issueTime)[:6])  # 时间取到月份
        if monthDate not in songsDict:
            songsDict[monthDate] = []
        monthSongsList = songsDict.get(monthDate)
        monthSongsList.append(song)
    return songsDict


def clusterAlgorithm(list):
    playArray = []
    songsList = []
    for song in list:
        playTrace = song.getTrace()[0]
        traceLength = len(playTrace)
        if traceLength < days:
            playTrace = np.hstack((np.zeros(days - traceLength), playTrace))
        playArray.append(playTrace)
        songsList.append(song)
    apc = cluster.AffinityPropagation(damping=0.5, max_iter=1000, convergence_iter=50, preference=None,
                                      affinity='euclidean')
    clusterIndex = apc.fit_predict(playArray)
    return clusterIndex, songsList


def clusterWithIndex(clusterIndex, songsList):  # 将歌曲按照索引聚类
    clusterSongsList = []
    clusterDict = {}
    for index, song in zip(clusterIndex, songsList):
        if index not in clusterDict:
            clusterDict[index] = []
        songList = clusterDict.get(index)
        songList.append(song)
    for songList in clusterDict.values():
        clusterSongsList.append(combine(songList))
    return clusterSongsList


def combine(songList):
    traceLength = maxTrace(songList)
    clusterSongsTrace = np.zeros((4, traceLength))
    clusterSongsPercent = np.zeros((4, traceLength))
    clusterSongsCumulateEA = np.zeros(traceLength)
    for song in songList:
        songTrace = song.getTrace()
        percentInSongs = song.getPercentInSongs()
        songCumulateEA = song.getCumulateEA()
        emptyDays = traceLength - songTrace.shape[1]
        clusterSongsTrace += np.hstack((np.zeros((4, emptyDays)), songTrace))
        clusterSongsPercent += np.hstack((np.zeros((4, emptyDays)), percentInSongs))
        clusterSongsCumulateEA += np.hstack((np.zeros(emptyDays), songCumulateEA))
    songId = ''
    initPlay = 0
    for song in songList:
        songId += ' ' + song.getId()
        initPlay += int(song.getInitPlay())
    monthDate = ''.join(list(songList[0].getIssueTime())[:6])
    clusterSong = Song(songId, [0, 0, monthDate, initPlay, -1])
    clusterSong.setTrace(clusterSongsTrace)
    clusterSong.setPercentInSongs(clusterSongsPercent)
    clusterSong.setCumulateEA(clusterSongsCumulateEA)
    clusterSong.makeMean()
    clusterSong.setPopular(True)
    return clusterSong


def maxTrace(songList):
    list = []
    for song in songList:
        list.append(song.getTrace().shape[1])
    return max(list)


############################### cluster end #################################

def findSuddenPoint(songTrace):
    traceLength = songTrace.shape[1]
    actionTrace = np.sum(songTrace[:3, :], axis=0)
    maxPosList = []
    maxIter = 5
    while maxIter > 0:
        maxIter -= 1
        maxActionPoint = max(actionTrace)
        maxPos = np.where(actionTrace == maxActionPoint)[0][0]
        # if len(maxPosList) > 0 and maxPos < max(maxPosList):  # 最大点只向后找
        #     break
        if maxPos < 7 or traceLength - maxPos < 7:  # 当第一个或最后几个点是最大点，要重新寻找最大点
            if maxPos < 7:
                postMaxMean = np.mean(actionTrace[maxPos + 7:])
                actionTrace[0:maxPos + 7] = postMaxMean
            elif traceLength - maxPos < 7:
                preMaxMean = np.mean(actionTrace[:maxPos - 7])
                actionTrace[maxPos - 7:] = preMaxMean
            continue
        preMaxMean = np.mean(actionTrace[:maxPos - 7])
        postMaxMean = np.mean(actionTrace[maxPos + 7:])
        # print maxPos, maxActionPoint, preMaxMean, postMaxMean
        if maxActionPoint > 2.5 * preMaxMean:  # 突变点前提条件
            if traceLength - maxPos > 14:
                if postMaxMean > 2.5 * preMaxMean:
                    maxPosList.append(maxPos)
                    break
                elif postMaxMean > 1.2 * preMaxMean:  # 之后的数量明显提升，说明这是一个突变点
                    maxPosList.append(maxPos)
            if maxPos >= 7 and traceLength - maxPos >= 7:  # 去除这个最大点继续寻找
                actionTrace[maxPos - 7:maxPos + 7] = (preMaxMean + postMaxMean) / 2
            else:
                if maxPos < 7:
                    actionTrace[0:maxPos + 7] = (preMaxMean + postMaxMean) / 2
                elif traceLength - maxPos < 7:
                    actionTrace[maxPos - 7:] = (preMaxMean + postMaxMean) / 2
        else:
            break
    if len(maxPosList) == 0:
        return 0
    else:
        return max(maxPosList) + 5
