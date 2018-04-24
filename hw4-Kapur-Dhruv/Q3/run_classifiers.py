# -*- coding: utf-8 -*-
## Data and Visual Analytics - Homework 4
## Georgia Institute of Technology
## Applying ML algorithms to recognize seizure from EEG brain wave signals



import numpy as np
import pandas as pd
import time 

from sklearn.model_selection import cross_val_score, GridSearchCV, cross_validate, train_test_split
from sklearn.metrics import accuracy_score, classification_report
from sklearn.svm import SVC
from sklearn.linear_model import LinearRegression
from sklearn.neural_network import MLPClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import MinMaxScaler,normalize

######################################### Reading and Splitting the Data ###############################################

# Read in all the data.
data = pd.read_csv('seizure_dataset.csv')

# Separate out the x_data and y_data.
x_data = data.loc[:, data.columns != "y"]
y_data = data.loc[:, "y"]

# The random state to use while splitting the data. DO NOT CHANGE.
random_state = 100 # DO NOT CHANGE

# XXX
# TODO: Split each of the features and labels arrays into 70% training set and
#       30% testing set (create 4 new arrays). Call them x_train, x_test, y_train and y_test.
#       Use the train_test_split method in sklearn with the parameter 'shuffle' set to true 
#       and the 'random_state' set to 100.
# XXX

x_train, x_test, y_train, y_test = train_test_split(x_data, y_data, train_size=0.7, random_state=100,shuffle=True)


# ############################################### Linear Regression ###################################################
# XXX
# TODO: Create a LinearRegression classifier and train it.
# XXX
linear=LinearRegression(fit_intercept=True, normalize=False, copy_X=True, n_jobs=1)
linear.fit(x_train,y_train)
y_pred=linear.predict(x_test)
y_tpred = linear.predict(x_train)

# XXX
# TODO: Test its accuracy (on the testing set) using the accuracy_score method.
# Note: Use y_predict.round() to get 1 or 0 as the output.
# XXX
y_pred =y_pred.round()
y_tpred = y_tpred.round()
Accuracy1=accuracy_score(y_test,y_pred)
t_accuracy1 = accuracy_score(y_train,y_tpred)

# ############################################### Multi Layer Perceptron #################################################
# XXX
# TODO: Create an MLPClassifier and train it.
# XXX
MLP=MLPClassifier(hidden_layer_sizes=(100,), activation='relu',solver='adam',alpha=0.0001,batch_size='auto',
                  learning_rate='constant',learning_rate_init=0.001,power_t=0.5,max_iter=200,shuffle=True,
                  random_state=None,tol=0.0001,verbose=False,warm_start=False,momentum=0.9,nesterovs_momentum=True,
                  early_stopping=False,validation_fraction=0.1,beta_1=0.9,beta_2=0.999,epsilon=1e-08)
#MLP = MLPClassifier(solver='adam', alpha=1e-5,hidden_layer_sizes=(15,), random_state=1)
MLP.fit(x_train,y_train)
y_pred1 = MLP.predict(x_test)
y_tpred1 = MLP.predict(x_train)
# XXX
# TODO: Test its accuracy on the test set using the accuracy_score method.
# XXX

Accuracy2 = accuracy_score(y_test,y_pred1)
t_accuracy2 = accuracy_score(y_train,y_tpred1)


# ############################################### Random Forest Classifier ##############################################
# XXX
# TODO: Create a RandomForestClassifier and train it.
# XXX
 
RFC=RandomForestClassifier(n_estimators=10, criterion='gini', max_depth=None, min_samples_split=2, min_samples_leaf=1, 
                           min_weight_fraction_leaf=0.0, max_features='auto', max_leaf_nodes=None, min_impurity_decrease=0.0,
                           min_impurity_split=None, bootstrap=True, oob_score=False, n_jobs=1, random_state=None, 
                           verbose=0, warm_start=False, class_weight=None)
#RFC=RandomForestClassifier(n_estimators=10, max_depth=None,min_samples_split=2, random_state=0)
RFC.fit(x_train,y_train)
y_pred2 = RFC.predict(x_test)
y_tpred2 = RFC.predict(x_train)

# XXX
# TODO: Test its accuracy on the test set using the accuracy_score method.
# XXX
Accuracy3 = accuracy_score(y_test,y_pred2)
t_accuracy3 = accuracy_score(y_train,y_tpred2)
# XXX
# TODO: Tune the hyper-parameters 'n_estimators' and 'max_depth'.
#       Print the best params, using .best_params_, and print the best score, using .best_score_.
# XXX

rfc = RandomForestClassifier() 

# Use a grid over parameters of interest
param_grid = { 
           "n_estimators" : [10, 20, 30],
           "max_depth" : [5, 10, 15]
           }
 
CV_rfc = GridSearchCV(estimator=rfc, param_grid=param_grid, cv= 10)
CV_rfc.fit(x_train, y_train)
print (CV_rfc.best_params_)
print (CV_rfc.best_score_)


# ############################################ Support Vector Machine ###################################################
# XXX
# TODO: Create a SVC classifier and train it.
# XXX
SVM=SVC(C=1.0, kernel='rbf', degree=3, gamma='auto', coef0=0.0, shrinking=True, probability=False, tol=0.001, cache_size=200, 
        class_weight=None, verbose=False, max_iter=-1, decision_function_shape='ovr', random_state=None)

SVM.fit(x_train,y_train)
y_pred3 = SVM.predict(x_test)
y_tpred3 = SVM.predict(x_train)

# XXX
# TODO: Test its accuracy on the test set using the accuracy_score method.
# XXX
Accuracy4 = accuracy_score(y_test,y_pred3)
t_accuracy4 = accuracy_score(y_train,y_tpred3)

# XXX
# TODO: Tune the hyper-parameters 'C' and 'kernel' (use rbf and linear).
#       Print the best params, using .best_params_, and print the best score, using .best_score_.
# XXX

scaler = MinMaxScaler()
MinMaxScaler(copy=True, feature_range=(0, 1))

scaler.fit(x_train)
x_train_p=scaler.transform(x_train)
parameters = {'kernel':[ 'rbf', 'linear'], 'C':[0.1,10,1]}
clf=GridSearchCV(SVC(), parameters, cv=10)

clf.fit(x_train_p,y_train)
print(clf.best_params_)
print(clf.best_score_)


# XXX 
# ########## PART C ######### 
# TODO: Print your CV's highest mean testing accuracy and its corresponding mean training accuracy and mean fit time.
# 		State them in report.txt.
# XXX

parameters = {'kernel':[ 'rbf'], 'C':[10]}

grid = GridSearchCV(SVC(), parameters, cv=10)
grid.fit(x_train_p,y_train)
print(grid.cv_results_)



