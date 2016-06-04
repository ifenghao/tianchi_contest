__author__ = 'zfh'
# coding:utf-8

from sklearn import svm, grid_search, cross_validation
from scipy.stats import uniform
import numpy as np
from copy import copy


def train(XTrain, yTrain, testsize):
    XTrain = np.array(XTrain, dtype=float)
    yTrain = np.array(yTrain, dtype=float)
    params = {'C': uniform(1, 99),
              'gamma': uniform(0.01, 0.29),
              'kernel': ['rbf', 'poly']}
    kfold = cross_validation.KFold(len(XTrain), n_folds=4, shuffle=False)
    models = []
    for i in range(len(yTrain[0])):
        svr = svm.SVR()
        clf = grid_search.RandomizedSearchCV(svr, param_distributions=params, n_iter=30, cv=kfold,
                                             scoring='mean_squared_error', n_jobs=-1,verbose=1)
        clf.fit(transArray(XTrain), yTrain[:, i])
        models.append(clf.best_estimator_)
    yPredict = []
    XPredict = copy(XTrain[-1])
    for i in range(testsize):
        XPredict = np.delete(XPredict, 0, axis=0)
        XPredict = np.insert(XPredict, len(XPredict), yTrain[-1], axis=0)
        subyPredict = np.array([])
        for j in range(len(models)):
            models[j].fit(transArray(XTrain), yTrain[:, j])  # 重复训练模型
            newPredict = models[j].predict([transRow(XPredict)])
            subyPredict = np.hstack((subyPredict, newPredict))
        XTrain = np.delete(XTrain, 0, axis=0)
        XTrain = np.insert(XTrain, len(XTrain), copy(XPredict), axis=0)
        yTrain = np.delete(yTrain, 0, axis=0)
        yTrain = np.insert(yTrain, len(yTrain), copy(subyPredict), axis=0)
        yPredict.append(copy(subyPredict[0]))
    return np.array(yPredict)


def transArray(array):
    result = []
    for row in array:
        catRow = np.array([])
        for item in row:
            catRow = np.hstack((catRow, item))
        result.append(catRow)
    return np.array(result)


def transRow(row):
    result = []
    for item in row:
        result.extend(item)
    return np.array(result)

# def train(XTrain, yTrain, testsize):
#     XTrain = np.array(XTrain, dtype=float)
#     yTrain = np.array(yTrain, dtype=float)
#     params = {'C': uniform(1, 99),
#               'gamma': uniform(0.01, 0.29),
#               'kernel': ['rbf', 'poly']}
#     kfold = cross_validation.KFold(len(XTrain), n_folds=4, shuffle=False)
#     models = []
#     for i in range(len(yTrain[0])):
#         svr = svm.SVR()
#         clf = grid_search.RandomizedSearchCV(svr, param_distributions=params, n_iter=10,
#                                              cv=kfold, scoring='mean_squared_error', n_jobs=-1,verbose=2)
#         models.append(clf)
#     yPredict = []
#     XPredict = copy(XTrain[-1])
#     for i in range(testsize):
#         XPredict = np.delete(XPredict, 0, axis=0)
#         XPredict = np.insert(XPredict, len(XPredict), yTrain[-1], axis=0)
#         subyPredict = np.array([])
#         XTrainTrans = transArray(XTrain)
#         XPredictTrans = transRow(XPredict)
#         for j in range(len(models)):
#             models[j].fit(XTrainTrans, yTrain[:, j])  # 重复训练模型
#             newPredict = models[j].predict([XPredictTrans])
#             subyPredict = np.hstack((subyPredict, newPredict))
#         XTrain = np.delete(XTrain, 0, axis=0)
#         XTrain = np.insert(XTrain, len(XTrain), copy(XPredict), axis=0)
#         yTrain = np.delete(yTrain, 0, axis=0)
#         yTrain = np.insert(yTrain, len(yTrain), copy(subyPredict), axis=0)
#         yPredict.append(copy(subyPredict[0]))
#     return np.array(yPredict)


# import preprocess
#
# x = np.arange(50)
# z = np.vstack((x, x + 100, x + 200))
# X, y = preprocess.makeTrainset(z, 3, 0)
# print train(X, y, 10)
