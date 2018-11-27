import pandas as pd
from sklearn.linear_model import LogisticRegression
import matplotlib.pyplot as plt


from utils import table

# point diff at home   won away flag


df = table([i for i in range(2000, 2004)])

df_1 = pd.DataFrame(data=None, index=df.index, columns=["pts_diff", "W"])
i = 0

for index, row in df.iterrows():
    df_1.iloc[index]["pts_diff"] = row["Pts_diff_home_1"]

    if row["Pts_diff_home_2"] > 0:
        df_1["W"].iloc[index] = 0

    else:
        df_1.iloc[index]["W"] = 1

X = df_1["pts_diff"].values.reshape(-1, 1)
y = df_1["W"].values.reshape(-1, 1)

clf = LogisticRegression(random_state=0, solver='lbfgs', multi_class='multinomial').fit(X, y)
print(X)
print(clf.predict_proba(X))
plt.plot(X, clf.predict_proba(X)[:, 0])

plt.show()


