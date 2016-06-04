__author__ = 'zfh'
# coding:utf-8
import preprocess as pp
from sklearn import svm, grid_search, cross_validation
from scipy.stats import uniform
import numpy as np
from copy import copy


def train(array, embedDim, interval):
    distance=7
    for i in range(9):
        XTrain, yTrain = pp.makeTrainset(array, embedDim, interval, distance)  # 模型的预测天数
        XPredict = pp.makeXPredict(array, embedDim, interval, distance)
        params = {'C': uniform(1, 99),
                  'gamma': uniform(0.01, 0.29),
                  'kernel': ['rbf', 'poly']}
        kfold = cross_validation.KFold(len(XTrain), n_folds=5, shuffle=False)
        subyPredict = []
        for j in range(len(yTrain[0])):
            svr = svm.SVR()
            clf = grid_search.RandomizedSearchCV(svr, param_distributions=params, n_iter=10, cv=kfold,
                                                 scoring='mean_squared_error', n_jobs=1, verbose=0)
            clf.fit(XTrain, yTrain[:, j])
            subyPredict.append(clf.predict(XPredict))
        array = np.hstack((array, np.array(copy(subyPredict))))  # 将一个模型的预测值作为已知数据，训练下一个模型
        embedDim += distance
    yPredict = array[0, -62:-2]  # 一共可以预测63天，取其中对应的数据
    return yPredict
