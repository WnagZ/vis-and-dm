from sklearn import datasets
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
import pandas as pd
import numpy as np
#Import Dataset
california = datasets.fetch_california_housing()
#print(california.DESCR)


#Create Polynomial of Degree 1
degree = 1
poly = PolynomialFeatures(degree, include_bias=True)
poly_features = poly.fit_transform(california.data)
feature_names = poly.get_feature_names(california.feature_names)
print(feature_names)

#Fit a Linear Regression
lrm = LinearRegression()
lrm.fit(poly_features, california.target)

#Get Model coefficinets

coefficients = lrm.coef_

print(coefficients)

print(max([ 0.00000000e+00,  4.36693293e-01,  9.43577803e-03, -1.07322041e-01,
  6.45065694e-01, -3.97638942e-06, -3.78654265e-03, -4.21314378e-01,
 -4.34513755e-01]))
# Make the Dataset a Dataframe
df = pd.DataFrame(california.data, columns=california.feature_names)

# Compute the Correlation Matrix
correlation_matrix = df.corr()

pd.set_option('display.max_rows', len(correlation_matrix))
pd.set_option('display.max_columns', len(correlation_matrix))

print(correlation_matrix)
print(max(correlation_matrix))


# Get the feature names and data
feature_names = california.feature_names
data = california.data

# Find the index of 'Longitude' feature
index_to_remove = feature_names.index('Longitude')

# Create a new dataset without 'Longitude'
new_data = np.delete(data, index_to_remove, axis=1)
new_feature_names = np.delete(feature_names, index_to_remove)

new_data = np.delete(california.data, index_to_remove, axis=1)
new_feature_names = np.delete(california.feature_names, index_to_remove)

degree = 1
poly = PolynomialFeatures(degree, include_bias=True)
poly_features = poly.fit_transform(new_data.data)
feature_names = poly.get_feature_names(new_feature_names)
print(feature_names)

#Fit a Linear Regression
lrm2 = LinearRegression()
lrm2.fit(poly_features, california.target)

#Get Model coefficinets

coefficients2 = lrm2.coef_

print(coefficients2)

print(max([0.00000000e+00,  5.27127446e-01,  1.65018937e-02, -1.97311232e-01,
  9.36218091e-01,  1.65072351e-05, -4.78546779e-03, -3.07104601e-02]))