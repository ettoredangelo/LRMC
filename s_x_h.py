import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression
import matplotlib.pyplot as plt


from utils import table

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
a = [i[0] for i in X]
print(clf.predict_proba(X)[:, 1])
plt.plot(a, clf.predict_proba(X)[:, 1])

# and plot the result
plt.figure(1, figsize=(4, 3))
plt.clf()
plt.scatter(X.ravel(), y, color='black', zorder=20)
X_test = np.linspace(-70, 70, 300)


def model(x):
    return 1 / (1 + np.exp(-x))


loss = model(X_test * clf.coef_ + clf.intercept_).ravel()
plt.plot(X_test, loss, color='red', linewidth=3)

plt.show()

print(clf.coef_, clf.intercept_)


