__author__ = 'zfh'
# coding:utf-8
class Action(object):

    def __init__(self,num):
        self.num=num
        self.play=0
        self.download=0
        self.collect=0
        self.users=set()

    def increasePlay(self):
        self.play+=1

    def increaseDownload(self):
        self.download+=1

    def increaseCollect(self):
        self.collect+=1

    def addUser(self,user_id):
        self.users.add(user_id)
