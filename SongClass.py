__author__ = 'zfh'
# coding:utf-8
import utils
from DayActionClass import DayAction
import os


class Song(object):
    def __init__(self, songId, infoList):
        self.__id = songId
        self.__issueTime = infoList[2]
        self.__initPlay = infoList[3]
        self.__language = infoList[4]
        self.__dailyTrace = []  # 日活动列表

    def makeDailyTrace(self, songWithUsersList, usersObjectDict):
        trace = [DayAction(i) for i in range(utils.days)]
        if songWithUsersList == None:
            print 'empty song users list ' + self.__id
        else:
            for row in songWithUsersList:
                user = usersObjectDict.get(row[0])  # 查看用户是否活跃
                if user.isActive():
                    dateNum = utils.date2num(row[4])
                    dayAction = trace[dateNum]
                    dayAction.addActiveUser(row[0])
                    if row[3] == '1':
                        dayAction.increasePlay()
                    elif row[3] == '2':
                        dayAction.increaseDownload()
                    elif row[3] == '3':
                        dayAction.increaseCollect()
        self.__dailyTrace = trace
        return

    def getId(self):
        return self.__id

    def getIssueTime(self):
        return self.__issueTime

    def getInitPlay(self):
        return self.__initPlay

    def getLanguage(self):
        return self.__language

    def getDailyTrace(self):
        return self.__dailyTrace
