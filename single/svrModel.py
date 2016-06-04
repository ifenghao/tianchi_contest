__author__ = 'zfh'
# coding:utf-8

from sklearn import svm, grid_search, cross_validation
from scipy.stats import uniform


def train(XTrain, yTrain, XPredict):
    params = {'C': uniform(1, 999),
              'gamma': uniform(0.01, 0.29),
              'kernel': ['rbf', 'poly']}
    kfold = cross_validation.KFold(len(XTrain), n_folds=3, shuffle=False)
    svr = svm.SVR()
    clf = grid_search.RandomizedSearchCV(svr, param_distributions=params, n_iter=20,
                                         cv=kfold, scoring='mean_squared_error', n_jobs=-1)
    clf.fit(XTrain, yTrain)  # 一次性训练模型
    # print clf.best_score_, clf.best_estimator_
    yPredict = clf.predict(XPredict)
    return yPredict, clf.best_params_
