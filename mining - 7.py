from sklearn.linear_model import Ridge
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split
import pandas as pd

# df = pd.read_csv("METABRIC_RNA_Mutation.csv")  # Adapt the path
# df_D = pd.concat([df["age_at_diagnosis"], df.iloc[:, 31:520]], axis=1)
# D = df_D.to_numpy()
# y = df["overall_survival_months"].to_numpy()


def RidgeRegression(x_data, y_data, x_test, a):
    ridgeReg = Ridge(alpha=a)
    ridgeReg.fit(x_data, y_data)
    return ridgeReg.predict(x_test)


def MeanSquareError(test, pred):
    mse = mean_squared_error(test, pred)
    return mse


df = pd.read_csv("METABRIC_RNA_Mutation.csv")
df_D = pd.concat([df["age_at_diagnosis"], df.iloc[:, 31:520]], axis=1)

# X and y values
X = df_D.to_numpy()
y = df["overall_survival_months"].to_numpy()
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=17)

for alpha in [10 ** (-10), 1, 2]:
    prediction = RidgeRegression(X_train, y_train, X_test, alpha)
    print(MeanSquareError(y_test, prediction))
