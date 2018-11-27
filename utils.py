import pandas as pd
import sqlite3

from config import Config

# Open the connection
conn = sqlite3.connect(Config.DB_PATH)
cur = conn.cursor()


def table(years, c=cur):
    '''

    :param years: list of years you want to take data from
    :param c: cursor to the database
    :return: dataframe with columns['Team_1_1', 'Team_2_1', 'Team_1_points_1', 'Team_2_points_1', 'OT_1', 'Team_1_2',
                                    'Team_2_2', 'Team_1_points_2', 'Team_2_points_2', 'OT_2', 'Season']
    '''
    result = []
    for year in years:
        cur.execute(f"SELECT A.Team_1, A.Team_2, A.Team_1_points, A.Team_2_points, A.OT, " \
                    f"B.Team_1, B.Team_2, B.Team_1_points, B.Team_2_points, B.OT, B.SEASON " \
                    f"FROM Scores AS A " \
                    f"INNER JOIN " \
                    f"Scores AS B " \
                    f"ON (A.Team_1 = B.Team_2 AND A.Team_2 = B.Team_1) " \
                    f"WHERE A.Season = '{year}' AND B.Season = '{year}' " \
                    f"AND A.Neutral = 0 AND B.Neutral = 0 " \
                    f"AND A.Type = 'REG' AND B.Type = 'REG'")

        result.extend(c.fetchall())

    # Write all of them in a dataframe
    df = pd.DataFrame(data=result,
                      columns=['Team_1_1', 'Team_2_1', 'Team_1_points_1', 'Team_2_points_1', 'OT_1', 'Team_1_2',
                               'Team_2_2', 'Team_1_points_2', 'Team_2_points_2', 'OT_2', 'Season'])

    # Add column point differential and set it to zero where the game went to overtime
    df['Pts_diff_home_1'] = df['Team_1_points_1'] - df['Team_2_points_1']
    df['Pts_diff_home_1'][df['OT_1'] == True] = 0
    df['Pts_diff_home_2'] = df['Team_1_points_2'] - df['Team_2_points_2']

    return df
