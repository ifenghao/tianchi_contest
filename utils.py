__author__ = 'zfh'
# coding:utf-8
import time, os
import csv
import numpy as np
import matplotlib.pyplot as plt
from UserClass import User

startTime = int(time.mktime(time.strptime('20150301', '%Y%m%d')))
secondsPerDay = 86400
days = 183
currentPath = os.getcwd()
usersFileName = 'mars_tianchi_user_actions.csv'
usersFile = os.path.join('/home/zhufenghao', 'dataset', usersFileName)
songsFileName = 'mars_tianchi_songs.csv'
songsFile = os.path.join('/home/zhufenghao', 'dataset', songsFileName)

resultPath = os.path.join(currentPath, 'result')
allResultPath = os.path.join('/home/zhufenghao', 'allresults')

usersPickleFileName = 'usersObjectDict.pkl'
usersPickleFile = os.path.join('/home/zhufenghao', 'dataset', usersPickleFileName)

songsPickleFileName = 'songsDict.pkl'
songsPickleFile = os.path.join('/home/zhufenghao', 'dataset', songsPickleFileName)

artistsPickleFileName='artistsDict.pkl'
artistsPickleFile=os.path.join('/home/zhufenghao','dataset',artistsPickleFileName)


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


def date2num(date):
    return (int(time.mktime(time.strptime(date, '%Y%m%d'))) - startTime) // secondsPerDay


def entropy(countList):
    countList = np.array(map(float, countList))  # 转换为浮点型数组
    countList[countList == 0.] = 0.001  # 所有0元素用0.001代替，否则计算熵出错
    p = countList / float(np.sum(countList))
    return -np.sum(p * np.log2(p))


def normalizedVariation(yTrue, yPredict):
    normSquare = [((p - t) / t) ** 2 for t, p in zip(yTrue, yPredict)]
    return np.sqrt(np.mean(normSquare))


def plotArtistSongsTrace(artistId):
    resultFilePath = os.path.join(resultPath, 'artists', artistId)
    if not os.path.exists(resultFilePath):
        print resultFilePath + ' not exist'
        return
    resultFile = os.path.join(resultFilePath, 'statistics.txt')
    with open(resultFile, 'r') as file:
        while True:
            songId = file.readline().strip('\n')
            if not songId:
                break
            issueTime = file.readline().strip('\n')
            initPlay = file.readline().strip('\n')
            language = file.readline().strip('\n')
            play = map(int, file.readline().strip('\n').split(','))
            download = map(int, file.readline().strip('\n').split(','))
            collect = map(int, file.readline().strip('\n').split(','))
            users = map(int, file.readline().strip('\n').split(','))
            p = plt.plot(play, 'bo', play, 'b-')
            d = plt.plot(download, 'ro', download, 'r-')
            c = plt.plot(collect, 'go', collect, 'g-')
            u = plt.plot(users, 'yo', users, 'y-')
            plt.legend([p[1], d[1], c[1], u[1]], ['play', 'download', 'collect', 'users'])
            plt.xlabel('days')
            plt.ylabel('counts')
            plt.title('id:' + songId + '\n' + issueTime + '-' + initPlay + '-' + language)
            plt.savefig(os.path.join(resultFilePath, songId + ".png"))
            plt.clf()


def plotUserSongsRecord(userId):
    resultFilePath = os.path.join(resultPath, 'users')
    if not os.path.exists(resultFilePath):
        print resultFilePath + ' not exist'
        return
    resultFile = os.path.join(resultFilePath, userId + '.txt')
    with open(resultFile, 'r') as file:
        play = []
        download = []
        collect = []
        songsTriedNumber = 0
        playSum = 0
        downloadSum = 0
        collectSum = 0
        while True:
            songId = file.readline().strip('\n')
            if not songId:
                break
            if songId.find('sum:') != -1:
                songsTriedNumber = map(int, file.readline().strip('\n').split(','))
                playSum = map(int, file.readline().strip('\n').split(','))
                downloadSum = map(int, file.readline().strip('\n').split(','))
                collectSum = map(int, file.readline().strip('\n').split(','))
            else:
                play.append(map(int, file.readline().strip('\n').split(',')))
                download.append(map(int, file.readline().strip('\n').split(',')))
                collect.append(map(int, file.readline().strip('\n').split(',')))
        p = plt.plot(play, 'bo', play, 'b-')
        d = plt.plot(download, 'ro', download, 'r-')
        c = plt.plot(collect, 'go', collect, 'g-')
        plt.legend([p[1], d[1], c[1]], ['play', 'download', 'collect'])
        plt.xlabel('songs')
        plt.ylabel('counts')
        plt.title('songs:' + str(songsTriedNumber) + '\n' + \
                  str(playSum) + '-' + str(downloadSum) + '-' + str(collectSum))
        plt.savefig(os.path.join(resultFilePath, userId + ".png"))
        plt.clf()
