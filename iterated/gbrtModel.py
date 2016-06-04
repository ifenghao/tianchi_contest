__author__ = 'zfh'
# coding:utf-8

from sklearn.ensemble import GradientBoostingRegressor
from sklearn import cross_validation, grid_search
from scipy.stats import randint, uniform
import numpy as np
from copy import copy


def train(XTrain, yTrain, testsize):
    XTrain = np.array(XTrain, dtype=float)
    yTrain = np.array(yTrain, dtype=float)
    params = {'n_estimators': randint(50, 150),
              'loss': ['ls', 'lad', 'huber'],
              'learning_rate': uniform(0.01, 0.19),
              'subsample': uniform(0.5, 0.5),
              'max_depth': randint(1, 4),
              'min_samples_split': randint(1, 4),
              'min_samples_leaf': randint(1, 4),
              'max_features': randint(1, len(transArray(XTrain)[0]))}
    kfold = cross_validation.KFold(len(XTrain), n_folds=4, shuffle=False)
    models = []
    for i in range(len(yTrain[0])):
        gbrt = GradientBoostingRegressor()
        clf = grid_search.RandomizedSearchCV(gbrt, param_distributions=params, n_iter=10,
                                             scoring='mean_absolute_error', cv=kfold, n_jobs=-1)
        clf.fit(transArray(XTrain), yTrain[:, i])
        models.append(clf.best_estimator_)
    yPredict = []
    XPredict = copy(XTrain[-1])
    for i in range(testsize):
        XPredict = np.delete(XPredict, 0, axis=0)
        XPredict = np.insert(XPredict, len(XPredict), yTrain[-1], axis=0)
        subyPredict = np.array([])
        XTrainTrans = transArray(XTrain)
        XPredictTrans = transRow(XPredict)
        for j in range(len(models)):
            models[j].fit(XTrainTrans, yTrain[:, j])  # 重复训练模型
            newPredict = models[j].predict([XPredictTrans])
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
