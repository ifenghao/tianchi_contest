__author__ = 'zfh'
# coding:utf-8
from scipy.stats import randint, uniform

import xgboost as xgb
from sklearn import grid_search, cross_validation
import numpy as np


def train(XTrain, yTrain, XPredict):
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
    xgbr = xgb.XGBRegressor()
    clf = grid_search.RandomizedSearchCV(xgbr, param_distributions=params, n_iter=5, n_jobs=1,
                                         scoring='mean_squared_error', cv=kfold, verbose=0)
    yPredict = []
    for i in range(yTrain.shape[1]):
        clf.fit(XTrain, yTrain[:, i])  # 训练distance个模型
        yPredict.extend(clf.predict(XPredict))
    return np.array(yPredict)
