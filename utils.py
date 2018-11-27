import pandas as pd
import sqlite3

conn = sqlite3.connect("C:\\Users\\rdangelo\\Desktop\\ncaa_database\\Teams.db")

cur = conn.cursor()

years = [2006, 2007]

result = []
for year in years:
    cur.execute(f"SELECT A.Team_1, A.Team_2, A.Team_1_points, A.Team_2_points, A.OT, " \
                f"B.Team_1, B.Team_2, B.Team_1_points, B.Team_2_points, B.OT " \
                f"FROM Scores AS A " \
                f"INNER JOIN " \
                f"Scores AS B " \
                f"ON (A.Team_1 = B.Team_2 AND A.Team_2 = B.Team_1) " \
                f"WHERE A.Season = '{year}' AND B.Season = '{year}' " \
                f"AND A.Neutral = 0 AND B.Neutral = 0 " \
                f"AND A.Type = 'REG' AND B.Type = 'REG'")

    result.extend(cur.fetchall())

for i in result:
    if 'Air Force' in i:
        print(i)

# # Write all of them in a dataframe
# df = pd.DataFrame(data=result, columns=['Team_1', 'Team_2', 'Team_1_points', 'Team_2_points', 'OT', 'Season'])
#
# # Add column point differential and set it to zero where the game went to overtime
# df['Pts_diff'] = df['Team_1_pts'] - df['Team_2_pts']
# df['Pts_diff'][df['OT'] == True] = 0
#
# # Find all teams that played in the opponents' court
# for i in range(df.shape[0]):
#     for j in range(i, df.shape[0]):
#         if df['Team_1'][i] == df['Team_2'][j] and df['Team_2'][i] == df['Team_1'][j]:
#             pass
#         pass


cur.close()
conn.close()