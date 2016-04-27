__author__ = 'zfh'
# coding:utf-8
import time, os
import matplotlib.pyplot as plt
from UserClass import User

startTime = int(time.mktime(time.strptime('20150301', '%Y%m%d')))
secondsPerDay = 86400
days = 183
currentPath = os.getcwd()
usersFileName = 'mars_tianchi_user_actions.csv'
usersFile = os.path.join('/home/zfh', 'dataset', usersFileName)
songsFileName = 'mars_tianchi_songs.csv'
songsFile = os.path.join('/home/zfh', 'dataset', songsFileName)

resultPath = os.path.join(currentPath, 'result')


def searchKeyInFile(key, fileName):
    '''
    返回文件中包含键值的所有行所构成的列表
    '''
    import csv

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
    import csv

    dict = {}
    with open(fileName) as file:
        rowReader = csv.reader(file, delimiter=',')
        for row in rowReader:
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
    for userId in usersDict.keys():
        user = User(userId)
        user.makeSongsTried(usersDict)
        user.setActive()
        dict[userId] = user
    return dict


def date2num(date):
    return (int(time.mktime(time.strptime(date, '%Y%m%d'))) - startTime) // secondsPerDay


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
