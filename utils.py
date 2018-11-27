import sqlite3

import pandas as pd

from config import Config

connection = sqlite3.connect(Config.DB_PATH)


def home_and_home_data(years, conn=connection):
    """
    :param years: list
    :param conn: connection to the database
    :return: DataFrame columns: ["pts_diff_home", "pts_diff_away", "W"]
    """
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
                        columns=['Team_1_H', 'Team_2_A', 'Team_1_H_points', 'Team_2_A_points', 'OT_1', 'Team_1_A',
                                 'Team_2_H', 'Team_2_H_points', 'Team_1_A_points', 'OT_2', 'Season'])

    df = pd.DataFrame(data=None, index=data.index, columns=["pts_diff_home", "pts_diff_away", "W"])

    df['pts_diff_home'] = data['Team_1_H_points'] - data['Team_2_A_points']
    df['pts_diff_home'][data['OT_1'] == 1] = 0
    df['pts_diff_away'] = data['Team_1_A_points'] - data['Team_2_H_points']

    mask = df['pts_diff_away'] > 0

    df["W"][mask] = 1
    df["W"][~mask] = 0

    return df
