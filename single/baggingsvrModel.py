__author__ = 'zfh'
# coding:utf-8

from sklearn import svm, ensemble, grid_search, cross_validation
from scipy.stats import randint


def train(XTrain, yTrain, XPredict):
    params = {'n_estimators': randint(1, 100)}
    kfold = cross_validation.KFold(len(XTrain), n_folds=3)
    svr = svm.SVR(kernel='rbf', C=50, gamma=0.1)
    baggingsvr = ensemble.BaggingRegressor(svr)
    clf = grid_search.RandomizedSearchCV(baggingsvr, param_distributions=params, n_iter=10,
                                         scoring='mean_squared_error', cv=kfold, n_jobs=-1)
    clf.fit(XTrain, yTrain)  # 一次性训练模型
    # print clf.best_score_, clf.best_estimator_
    yPredict = clf.predict(XPredict)
    return yPredict, clf.best_params_
