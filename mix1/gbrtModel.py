__author__ = 'zfh'
# coding:utf-8
from sklearn.ensemble import GradientBoostingRegressor
from sklearn import cross_validation, grid_search
from scipy.stats import randint, uniform
import numpy as np
from copy import copy
import preprocess as pp


def train(array, embedDim, interval):
    XTrain, yTrain = pp.makeTrainset(array, embedDim, interval, 1)
    kfold = cross_validation.KFold(len(XTrain), n_folds=5, shuffle=False)
    params = {'n_estimators': randint(20, 200),
              'loss': ['ls', 'lad', 'huber'],
              'learning_rate': uniform(0.01, 0.19),
              'subsample': uniform(0.5, 0.5),
              'max_depth': randint(1, 5),
              'min_samples_split': randint(1, 3),
              'min_samples_leaf': randint(1, 3),
              'max_features': randint(1, len(XTrain[0]))}
    bestModels = []
    for i in range(len(yTrain[0])):
        gbrt = GradientBoostingRegressor()
        clf = grid_search.RandomizedSearchCV(gbrt, param_distributions=params, n_iter=20,
                                             scoring='mean_squared_error', cv=kfold, n_jobs=-1)
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
