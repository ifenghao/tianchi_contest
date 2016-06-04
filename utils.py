__author__ = 'zfh'
# coding:utf-8
import time, os
import csv
import numpy as np
import matplotlib.pyplot as plt
from UserClass import User

startTime = int(time.mktime(time.strptime('20150301', '%Y%m%d')))
predictTime = int(time.mktime(time.strptime('20150901', '%Y%m%d')))
secondsPerDay = 86400
days = 183
currentPath = os.getcwd()
usersFileName = 'mars_tianchi_user_actions.csv'
usersFile = os.path.join('/home/zhufenghao', 'dataset', usersFileName)
songsFileName = 'mars_tianchi_songs.csv'
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
