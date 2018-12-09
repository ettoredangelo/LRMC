import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression

from utils import Model, get_home_and_home_data, get_teams, get_schedule, steady_state_probability


def LRMC(year):
    data = get_home_and_home_data([i for i in range(1993, 2017)])

    X = data["pts_diff_home"].values.reshape(-1, 1)
    y = data["W"].values.ravel()

    y = y.astype('int')

    clf = LogisticRegression(random_state=0, solver='lbfgs', multi_class='multinomial').fit(X, y)

    a = float(clf.coef_)
    b = float(clf.intercept_)

    m = Model(a, b)

    teams = get_teams(year)

    transition_matrix = pd.DataFrame(data=None, index=teams, columns=teams)

    for team_i in teams:
        schedule = get_schedule(team_i, year)

        N = schedule.shape[0]

        for team_j in schedule.Team_1.unique():
            if team_i != team_j:
                t_i_j = 0

                mask = (schedule['Team_1'] == team_j) | (schedule['Team_2'] == team_j)
                games = schedule[mask]

                for _, row in games.iterrows():
                    x = row['pts_diff']

                    if row['Team_1'] == team_i:
                        t_i_j += 1 - m.r_R(x)

                    else:
                        t_i_j += 1 - m.r_H(x)

                t_i_j /= N

                transition_matrix.loc[team_i, team_j] = t_i_j

            else:
                t_i_i = 0

                for _, row in schedule.iterrows():
                    x = row['pts_diff']

                    if row['Team_1'] == team_i:
                        t_i_i += m.r_R(x)

                    else:
                        t_i_i += m.r_H(x)

                t_i_i /= N

                transition_matrix.loc[team_i, team_i] = t_i_i

        print(team_i)

    transition_matrix = transition_matrix.fillna(0).astype(np.float)

    pi = steady_state_probability(transition_matrix.values)
    data = np.column_stack((teams, pi))

    LRMC_ranking = pd.DataFrame(data=data, columns=['Team', 'pi'])

    LRMC_ranking.loc[:, 'pi'] = pd.to_numeric(LRMC_ranking['pi'])
    LRMC_ranking.sort_values(by='pi', ascending=False, inplace=True)

    LRMC_ranking['Rk'] = np.arange(1, LRMC_ranking.shape[0] + 1)
    LRMC_ranking.set_index('Rk', inplace=True)

    return LRMC_ranking
