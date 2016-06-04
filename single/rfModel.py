__author__ = 'zfh'

from sklearn.ensemble import RandomForestRegressor
from sklearn import cross_validation, grid_search
from scipy.stats import randint


def train(XTrain, yTrain, XPredict):
    params = {"n_estimators": randint(5, 100),
              "max_depth": [1, 2, 3, 5, 10, None],
              "max_features": randint(1, len(XTrain[0])),
              "min_samples_split": randint(1, 3),
              "min_samples_leaf": randint(1, 3)}
    rf = RandomForestRegressor()
    kfold = cross_validation.KFold(len(XTrain), n_folds=3, shuffle=False)
    clf = grid_search.RandomizedSearchCV(rf, param_distributions=params, n_iter=30,
                                         scoring='mean_squared_error', cv=kfold, n_jobs=-1)
    clf.fit(XTrain, yTrain)
    # print clf.best_score_, clf.best_estimator_
    yPredict = clf.predict(XPredict)
    return yPredict, clf.best_params_
