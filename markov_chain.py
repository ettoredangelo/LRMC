import numpy as np


def transition_matrix_prob():
    '''

    :return: transition matrix
    '''
    # N = number of games played by i at this moment
    # t_ij = 1/N * [sum(r_x) + sum (1-x)]

    pass


def steady_state_prob(p):
    '''

    :param p: transition matrix
    :return: steady state probability matrix
    '''
    dim = p.shape[0]
    q = (p - np.eye(dim))
    ones = np.ones(dim)
    q = np.c_[q, ones]
    QTQ = np.dot(q, q.T)
    bQT = np.ones(dim)
    return np.linalg.solve(QTQ, bQT)
