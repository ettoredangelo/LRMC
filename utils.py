import sqlite3

import numpy as np
import pandas as pd

from config import Config


class Model:
    def __init__(self, a, b):
        self.a = a
        self.b = b

        self.h = (- b / a) / 2

    def r_H(self, x):
        x += self.h
        x = x * self.a + self.b
        return 1 / (1 + np.exp(-x))

    def r_R(self, x):
        return 1 - self.r_H(x)


def get_home_and_home_data(years, ot=True):
    """
    :param years: list
    :param ot: boolean, if ot: pts_diff -> 0
    :return: DataFrame columns: "pts_diff_home", "pts_diff_away", "W"
    """
    conn = sqlite3.connect(Config.DB_PATH)
    c = conn.cursor()

    result = []
    for year in years:
        c.execute(f"SELECT A.Team_1, A.Team_2, A.Team_1_points, A.Team_2_points, A.OT, "
                  f"B.Team_1, B.Team_2, B.Team_1_points, B.Team_2_points, B.OT, B.SEASON "
                  f"FROM Scores AS A "
                  f"INNER JOIN "
                  f"Scores AS B "
                  f"ON (A.Team_1 = B.Team_2 AND A.Team_2 = B.Team_1) "
                  f"WHERE A.Season = '{year}' AND B.Season = '{year}' "
                  f"AND A.Neutral = 0 AND B.Neutral = 0 "
                  f"AND A.Type = 'REG' AND B.Type = 'REG'")

        result.extend(c.fetchall())

    c.close()
    conn.close()

    data = pd.DataFrame(data=result,
                        columns=['Team_1_H', 'Team_2_A', 'Team_1_H_points', 'Team_2_A_points', 'OT_1', 'Team_2_H',
                                 'Team_1_A', 'Team_2_H_points', 'Team_1_A_points', 'OT_2', 'Season'])

    df = pd.DataFrame(data=None, index=data.index, columns=["pts_diff_home", "pts_diff_away", "W"])

    df['pts_diff_home'] = data['Team_1_H_points'] - data['Team_2_A_points']
    df['pts_diff_away'] = data['Team_1_A_points'] - data['Team_2_H_points']

    if ot:
        df.loc[data['OT_1'] == 1, 'pts_diff_home'] = 0

    mask = df['pts_diff_away'] > 0

    df.loc[mask, "W"] = 1
    df.loc[~mask, "W"] = 0

    return df


def get_teams(year):
    conn = sqlite3.connect(Config.DB_PATH)
    c = conn.cursor()

    sql = f"SELECT DISTINCT Team_1 FROM Scores WHERE Season = {year} ORDER BY Team_1"

    c.execute(sql)
    r = c.fetchall()

    c.close()
    conn.close()

    teams = [i[0] for i in r]

    return teams


def get_schedule(team, year):
    conn = sqlite3.connect(Config.DB_PATH)
    c = conn.cursor()

    c.execute("SELECT Team_1, Team_2, Team_1_points, Team_2_points From Scores Where Season = ? AND " \
              "(Team_1 = ? OR Team_2 = ?) AND Neutral = 0 AND Type = 'REG'", (year, team, team))

    r = c.fetchall()

    c.close()
    conn.close()

    schedule = pd.DataFrame(data=r, columns=['Team_1', 'Team_2', 'Team_1_points', 'Team_2_points'])

    return schedule


def steady_state_probability(p):
    """
    :param p: transition matrix
    :return: steady state probability
    """
    dim = p.shape[0]

    q = (p - np.eye(dim))
    ones = np.ones(dim)
    q = np.c_[q, ones]

    QTQ = np.dot(q, q.T)
    bQT = np.ones(dim)

    return np.linalg.solve(QTQ, bQT)
