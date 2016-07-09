__author__ = 'zfh'
# coding:utf-8
from sklearn.ensemble import ExtraTreesRegressor
from sklearn import cross_validation, grid_search
from scipy.stats import randint
import numpy as np
from copy import copy
import preprocess as pp

def train(array, embedDim, interval):
    XTrain, yTrain = pp.makeTrainset(array, embedDim, interval, 1)
    kfold = cross_validation.KFold(len(XTrain), n_folds=4, shuffle=False)
    params = {"n_estimators": randint(5, 100),
              "max_depth": [1, 2, 3, 5, 8, 10, None],
              "max_features": randint(1, len(XTrain[0])),
              "min_samples_split": randint(1, 3),
              "min_samples_leaf": randint(1, 3)}
    bestModels = []
    for i in range(len(yTrain[0])):
        erf = ExtraTreesRegressor()
        clf = grid_search.RandomizedSearchCV(erf, param_distributions=params, n_iter=10,
                                         scoring='mean_squared_error', cv=kfold, n_jobs=-1)
        clf.fit(XTrain, yTrain[:, i])
        bestModels.append(clf.best_estimator_)

    for i in range(60):
        XTrain, yTrain = pp.makeTrainset(array, embedDim, interval, 1)  # 模型的嵌入维度递增
        XPredict = pp.makeXPredict(array, embedDim, interval, 1)  # 待预测的嵌入维度递增
        subyPredict = []
        for j in range(len(yTrain[0])):
            bestModels[j].fit(XTrain, yTrain[:, j])
            subyPredict.append(bestModels[j].predict(XPredict))
        array = np.hstack((array, np.array(copy(subyPredict))))  # 将一个模型的预测值作为已知数据，训练下一个模型
        embedDim += 1
    yPredict = array[0, -60:]  # 一共可以预测60天，取其中对应的数据
    return yPredict
