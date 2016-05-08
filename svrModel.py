__author__ = 'zfh'
# coding:utf-8

from sklearn import svm, grid_search


def trainSVR(XTrain, yTrain, XPredict):
    svr = svm.SVR()
    para = {'C': [1, 10, 30]}
    clf = grid_search.GridSearchCV(svr, para)
    clf.fit(XTrain, yTrain)  # 一次性训练模型
    yPredict = clf.predict(XPredict)
    return yPredict
