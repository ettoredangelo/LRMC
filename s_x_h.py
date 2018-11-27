import numpy as np
import matplotlib.pyplot as plt

from sklearn.linear_model import LogisticRegression

from utils import home_and_home_data


def model(x):
    return 1 / (1 + np.exp(-x))


def logistic_regression(X, y):
    """
    :param X: array
    :param y: array
    :return:
    """
    clf = LogisticRegression(random_state=0, solver='lbfgs', multi_class='multinomial').fit(X, y)

    print(clf.coef_, clf.intercept_)

    # PLOT

    plt.scatter(X, y, color='black')

    X_test = np.linspace(-70, 70, 300)

    loss = model(X_test * clf.coef_ + clf.intercept_).ravel()
    loss_expected = model(X_test * 0.0292 - 0.6228).ravel()

    plt.plot(X_test, loss, color='red')
    plt.plot(X_test, loss_expected, color='black')

    plt.show()


if __name__ == "__main__":
    df = home_and_home_data([i for i in range(2000, 2004)])

    X = df["pts_diff_home"].values.reshape(-1, 1)
    y = df["W"].values.ravel()

    y = y.astype('int')

    logistic_regression(X, y)
