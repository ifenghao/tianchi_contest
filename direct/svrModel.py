__author__ = 'zfh'
# coding:utf-8

from sklearn import svm, grid_search, cross_validation
from scipy.stats import uniform
import numpy as np


def train(XTrain, yTrain, XPredict):
    XTrain = np.array(XTrain, dtype=float)
    yTrain = np.array(yTrain, dtype=float)
    params = {'C': uniform(1, 999),
              'gamma': uniform(0.01, 0.29),
              'kernel': ['rbf', 'poly']}
    kfold = cross_validation.KFold(len(XTrain), n_folds=4, shuffle=False)
    svr = svm.SVR()
    clf = grid_search.RandomizedSearchCV(svr, param_distributions=params, n_iter=20,
                                         cv=kfold, scoring='mean_squared_error', n_jobs=-1)
    yPredict = []
    for i in range(yTrain.shape[1]):
        clf.fit(XTrain, yTrain[:, i])  # 训练distance个模型
        yPredict.extend(clf.predict(XPredict))
    return np.array(yPredict)
