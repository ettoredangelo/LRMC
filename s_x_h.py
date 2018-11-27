import numpy as np

from sklearn.linear_model import LogisticRegression


def model(x):
    return 1 / (1 + np.exp(-x))


def logistic_regression(X, y):
    """
    :param X: array
    :param y: array
    :return:
    """
    clf = LogisticRegression(random_state=0, solver='lbfgs', multi_class='multinomial').fit(X, y)
