__author__ = 'zfh'
# coding:utf-8
import utils
from ActionClass import Action
import os


class Song(object):
    def __init__(self, songId, infoList):
        self.__id = songId
        self.__issueTime = infoList[2]
        self.__initPlay = infoList[3]
        self.__language = infoList[4]
        self.__trace = []  # 列表

    def makeTrace(self, usersList):
        traceList = [Action(i) for i in range(utils.days)]
        for row in usersList:
            dateNum = utils.date2num(row[4])
            action = traceList[dateNum]
            action.addUser(row[0])
            if row[3] == '1':
                action.increasePlay()
            elif row[3] == '2':
                action.increaseDownload()
            elif row[3] == '3':
                action.increaseCollect()
        self.__trace = traceList
        return

    def getId(self):
        return self.__id

    def getIssueTime(self):
        return self.__issueTime

    def getInitPlay(self):
        return self.__initPlay

    def getLanguage(self):
        return self.__language

    def getTrace(self):
        return self.__trace
