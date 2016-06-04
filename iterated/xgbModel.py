__author__ = 'zfh'
# coding:utf-8

from scipy.stats import randint, uniform
import numpy as np
from copy import copy
import xgboost as xgb
from sklearn import grid_search, cross_validation


def train(XTrain, yTrain, testsize):
    XTrain = np.array(XTrain, dtype=float)
    yTrain = np.array(yTrain, dtype=float)
    params = {'n_estimators': randint(50, 150),
              'max_depth': randint(1, 4),
              'learning_rate': uniform(0.01, 0.19),
              'min_child_weight': [1],
              'max_delta_step': randint(0, 50),
              'subsample': uniform(0.5, 0.5),
              'colsample_bytree': uniform(0.5, 0.5),
              'colsample_bylevel': uniform(0.5, 0.5),
              'scale_pos_weight': [0],
              'gamma': uniform(1, 6)}
    kfold = cross_validation.KFold(len(XTrain), n_folds=4, shuffle=False)
    models = []
    for i in range(len(yTrain[0])):
        xgbr = xgb.XGBRegressor()
        clf = grid_search.RandomizedSearchCV(xgbr, param_distributions=params, n_iter=10, n_jobs=1,
                                             scoring='mean_squared_error', cv=kfold, verbose=0)
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
