__author__ = 'zfh'

from sklearn.ensemble import GradientBoostingRegressor
from sklearn import cross_validation, grid_search
from scipy.stats import randint, uniform


def train(XTrain, yTrain, XPredict):
    params = {'n_estimators': randint(20, 200),
              'loss': ['ls', 'lad', 'huber'],
              'learning_rate': uniform(0.01, 0.19),
              'subsample': uniform(0.5, 0.5),
              'max_depth': randint(1, 5),
              'min_samples_split': randint(1, 3),
              'min_samples_leaf': randint(1, 3),
              'max_features': randint(1, len(XTrain[0]))}
    gbrt = GradientBoostingRegressor()
    kfold = cross_validation.KFold(len(XTrain), n_folds=5, shuffle=False)
    clf = grid_search.RandomizedSearchCV(gbrt, param_distributions=params, n_iter=50,
                                         scoring='mean_absolute_error', cv=kfold, n_jobs=-1)
    clf.fit(XTrain, yTrain)
    # print clf.best_score_, clf.best_estimator_
    yPredict = clf.predict(XPredict)
    return yPredict
