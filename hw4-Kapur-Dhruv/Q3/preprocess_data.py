## Data and Visual Analytics - Homework 4
## Georgia Institute of Technology
## Applying ML algorithms on the seizure dataset.

import numpy as np
import pandas as pd
import time

from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import StandardScaler, normalize
from sklearn.svm import SVC

######################################### Reading and Splitting the Data ###############################################

# Read in all the data.
data = pd.read_csv('seizure_dataset.csv')

# Separate out the x_data and y_data.
x_data = data.loc[:, data.columns != "y"]
y_data = data.loc[:, "y"]

# The random state to use while splitting the data.
random_state = 100 # DO NOT CHANGE

# XXX
# TODO: Split 70% of the data into training and 30% into test sets. Call them x_train, x_test, y_train and y_test.
# Use the train_test_split method in sklearn with the parameter 'shuffle' set to true and the 'random_state' set to 100.
# XXX
x_train, x_test, y_train, y_test = train_test_split(x_data, y_data, train_size=0.7, random_state=100,shuffle=True)

# ###################################### Without Pre-Processing Data ##################################################
# XXX
# TODO: Fit the SVM Classifier (with the tuned parameters)  on the x_train and y_train data.
# XXX 

SVM=SVC(C=10, kernel='rbf', degree=3, gamma='auto', coef0=0.0, shrinking=True, probability=False, tol=0.001, cache_size=200, 
        class_weight=None, verbose=False, max_iter=-1, decision_function_shape='ovr', random_state=None)

SVM.fit(x_train,y_train)
y_pred = SVM.predict(x_test)


# XXX
# TODO: Predict the y values for x_test and report the test accuracy using the accuracy_score method.
# XXX
Accuracy = accuracy_score(y_test,y_pred)

# ###################################### With Data Pre-Processing ##################################################
# XXX
# TODO: Standardize or normalize x_train and x_test using either StandardScalar or normalize().
# Call the processed data x_train_p and x_test_p.
# XXX
scaler = StandardScaler()
scaler.fit(x_train)
scaler.fit(x_test)
x_train_p = scaler.transform(x_train)
x_test_p =  scaler.transform(x_test)
StandardScaler(copy=True, with_mean=True, with_std=True)
 

# XXX
# TODO: Fit the SVM Classifier (with the tuned parameters) on the x_train_p and y_train data.
# XXX
SVM.fit(x_train_p,y_train)

# XXX
# TODO: Predict the y values for x_test_p and report the test accuracy using the accuracy_score method.
# XXX
y_pred1 = SVM.predict(x_test_p)
Accuracy1 = accuracy_score(y_test,y_pred1)



