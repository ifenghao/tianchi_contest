__author__ = 'zfh'

from sklearn.ensemble import ExtraTreesRegressor
from sklearn import cross_validation, grid_search
from scipy.stats import randint


def train(XTrain, yTrain, XPredict):
    params = {"n_estimators": randint(5, 100),
              "max_depth": [1, 2, 3, 5, 8, 10, None],
              "max_features": randint(1, len(XTrain[0])),
              "min_samples_split": randint(1, 3),
              "min_samples_leaf": randint(1, 3)}
    erf = ExtraTreesRegressor()
    kfold = cross_validation.KFold(len(XTrain), n_folds=5, shuffle=False)
    clf = grid_search.RandomizedSearchCV(erf, param_distributions=params, n_iter=50,
                                         scoring='mean_absolute_error', cv=kfold, n_jobs=-1)
    clf.fit(XTrain, yTrain)
    # print clf.best_score_, clf.best_estimator_
    yPredict = clf.predict(XPredict)
    return yPredict
