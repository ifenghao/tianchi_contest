__author__ = 'zfh'
# coding:utf-8
class DayAction(object):
    def __init__(self, dayNum):
        self.__dayNum = dayNum
        self.__playSum = 0
        self.__downloadSum = 0
        self.__collectSum = 0
        self.__dayActiveUsers = set()# 活跃用户的id

    def increasePlay(self):
        self.__playSum += 1

    def increaseDownload(self):
        self.__downloadSum += 1

    def increaseCollect(self):
        self.__collectSum += 1

    def addActiveUser(self, userId):
        self.__dayActiveUsers.add(userId)

    def getPlaySum(self):
        return self.__playSum

    def getDownloadSum(self):
        return self.__downloadSum

    def getCollectSum(self):
        return self.__collectSum

    def getActiveUsersNumber(self):
        return len(self.__dayActiveUsers)
