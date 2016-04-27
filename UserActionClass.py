__author__ = 'zfh'
# coding:=UTF-8

class UserAction(object):
    def __init__(self):
        self.__play = 0
        self.__download = 0
        self.__collect = 0

    def increasePlay(self):
        self.__play += 1

    def increaseDownload(self):
        self.__download += 1

    def increaseCollect(self):
        self.__collect += 1

    def getPlay(self):
        return self.__play

    def getDownload(self):
        return self.__download

    def getCollect(self):
        return self.__collect
