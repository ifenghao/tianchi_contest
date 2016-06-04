__author__ = 'zfh'
# coding:utf-8
import preprocess as pp
from sklearn import svm, grid_search, cross_validation
from scipy.stats import uniform
import numpy as np
from copy import copy


def train(array, embedDim, interval):
    XTrain, yTrain = pp.makeTrainset(array, embedDim, interval, 1)
    kfold = cross_validation.KFold(len(XTrain), n_folds=5, shuffle=False)
    params = {'C': uniform(1, 99),
              'gamma': uniform(0.01, 0.29),
              'kernel': ['rbf', 'poly']}
    bestModels = []
    for i in range(len(yTrain[0])):
        svr = svm.SVR()
        clf = grid_search.RandomizedSearchCV(svr, param_distributions=params, n_iter=30, cv=kfold,
                                             scoring='mean_squared_error', n_jobs=1, verbose=0)
        clf.fit(XTrain, yTrain[:, i])
        bestModels.append(clf.best_estimator_)

    for i in range(1, 12):
        XTrain, yTrain = pp.makeTrainset(array, embedDim, interval, i)  # 模型的预测天数递增
        XPredict = pp.makeXPredict(array, embedDim, interval, i)  # 待预测的输入递增
        subyPredict = []
        for j in range(len(yTrain[0])):
            bestModels[j].fit(XTrain, yTrain[:, j])
            subyPredict.append(bestModels[j].predict(XPredict))
        array = np.hstack((array, np.array(copy(subyPredict))))  # 将一个模型的预测值作为已知数据，训练下一个模型
    yPredict = array[0, -65:-5]  # 一共可以预测66天，取其中对应的数据
    return yPredict
