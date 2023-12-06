from sklearn.metrics import mean_squared_error
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import Ridge, Lasso


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


# for alpha in [10 ** (-10), 1, 2]:
#     prediction = RidgeRegression(X_train, y_train, X_test, alpha)
#     print(MeanSquareError(y_test, prediction))


def LassoRegression(x_data, y_data, x_test, a):
    lasso = Lasso(alpha=a)
    lasso.fit(X_train, y_train)
    return lasso.predict(x_test)


# for alpha in [10 ** (-10), 1, 2]:
#     prediction = LassoRegression(X_train, y_train, X_test, alpha)
#     print(MeanSquareError(y_test, prediction))


def RidgeFeatures(x_train, y_train, alpha):
    ridgeReg = Ridge(alpha=alpha)
    ridgeReg.fit(x_train, y_train)

    # Get the coefficients of the Ridge Regression model
    coefficients = ridgeReg.coef_

    # Count the number of non-zero coefficients, i.e., selected features
    num_selected_features = sum(coeff != 0 for coeff in coefficients)

    return num_selected_features


# print(RidgeFeatures(X_train, y_train, 1))


def LassoFeatures(x_train, y_train, alpha):
    lasso = Lasso(alpha=alpha)
    lasso.fit(X_train, y_train)

    # Get the coefficients of the Ridge Regression model
    coefficients = lasso.coef_

    # Count the number of non-zero coefficients, i.e., selected features
    num_selected_features = sum(coeff != 0 for coeff in coefficients)

    return num_selected_features

    print(LassoFeatures(X_train, y_train, 10 ** (-10)))