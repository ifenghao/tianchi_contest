__author__ = 'zfh'
# coding:utf-8
from sklearn.ensemble import ExtraTreesRegressor
from sklearn import cross_validation, grid_search
from scipy.stats import randint
import numpy as np


def train(XTrain, yTrain, XPredict):
    XTrain = np.array(XTrain, dtype=float)
    yTrain = np.array(yTrain, dtype=float)
    params = {"n_estimators": randint(50, 150),
              "max_depth": [1, 3, 5, None],
              "max_features": randint(1, len(XTrain[0])),
              "min_samples_split": randint(1, 4),
              "min_samples_leaf": randint(1, 4)}
    erf = ExtraTreesRegressor()
    kfold = cross_validation.KFold(len(XTrain), n_folds=4, shuffle=False)
    clf = grid_search.RandomizedSearchCV(erf, param_distributions=params, n_iter=5,
                                         scoring='mean_squared_error', cv=kfold, n_jobs=-1)
    yPredict = []
    for i in range(yTrain.shape[1]):
        clf.fit(XTrain, yTrain[:, i])  # 训练distance个模型
        yPredict.extend(clf.predict(XPredict))
    return np.array(yPredict)
