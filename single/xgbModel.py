__author__ = 'zfh'
# coding:utf-8

from scipy.stats import randint, uniform

import xgboost as xgb
from sklearn import grid_search, cross_validation


def train(XTrain, yTrain, XPredict):
    params = {'n_estimators': randint(20, 200),
              'max_depth': randint(1, 4),
              'learning_rate': uniform(0.01, 0.19),
              'min_child_weight': [1],
              'max_delta_step': randint(0, 50),
              'subsample': uniform(0.5, 0.5),
              'colsample_bytree': uniform(0.5, 0.5),
              'colsample_bylevel': uniform(0.5, 0.5),
              'scale_pos_weight': [0],
              'gamma': uniform(1, 10)}
    kfold = cross_validation.KFold(len(XTrain), n_folds=5, shuffle=False)
    xgbr = xgb.XGBRegressor()
    clf = grid_search.RandomizedSearchCV(xgbr, param_distributions=params, n_iter=50, n_jobs=1,
                                         scoring='mean_absolute_error', cv=kfold, verbose=0)
    clf.fit(XTrain, yTrain)  # 一次性训练模型
    # print clf.best_score_, clf.best_estimator_
    yPredict = clf.predict(XPredict)
    return yPredict
