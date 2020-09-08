########################
# Fitting
########################
import sklearn
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.svm import SVR
import pandas as pd
import numpy as np

class SmartChargingFitting():
    def __init__(self, baseline_profiles_file, controlled_profiles_file):
        self.num_runs = 4
        self.which_test_sample = 0 # less than num test samples

        self.baseline_profiles = np.load(baseline_profiles_file)
        self.controlled_profiles = np.load(controlled_profiles_file)


    def fitting_linear_regression(self):
        # Split data into train and test sets
        X_train, X_test, y_train, y_test = train_test_split(np.transpose(self.baseline_profiles), np.transpose(self.controlled_profiles), test_size=0.2, random_state=42)

        # Define and fit classifier
        clf = LinearRegression()
        clf.fit(X_train, y_train)

        # Score on test set
        clf.score(X_test, y_test)
        # Pretty good R^2 value with the linear regression model

        y_predicted = clf.predict(X_test)
        print('Prediction: \n', y_predicted)

        # plt.figure()
        # plt.plot(0.25*np.arange(0, 96), y_test[self.which_test_sample, :], label="real control")
        # plt.plot(0.25*np.arange(0, 96), y_predicted[self.which_test_sample, :], label="predicted control")
        # plt.title("Example of predicted control for a workplace at Santa Clara county (one day)")
        # plt.xlabel('Hour')
        # plt.xlim([0, 24])
        # plt.legend()
        # plt.show()

    def fitting_decision_tree_regression(self):
        # Split data into train and test sets
        X_train, X_test, y_train, y_test = train_test_split(np.transpose(self.baseline_profiles), np.transpose(self.controlled_profiles), test_size=0.2, random_state=42)

        # Define and fit classifier
        clf = DecisionTreeRegressor()
        clf.fit(X_train, y_train)

        # Score on test set
        clf.score(X_test, y_test)
        # Pretty good R^2 value with the linear regression model

        # Split data into train and test sets
        X_train, X_test, y_train, y_test = train_test_split(np.transpose(self.baseline_profiles), np.transpose(self.controlled_profiles), test_size=0.2, random_state=42)

        # Define and fit classifier
        clf = RandomForestRegressor()
        clf.fit(X_train, y_train)

        # Score on test set
        clf.score(X_test, y_test)
        # Pretty good R^2 value with the linear regression model

        # Predict on test set and inspect sample
        y_predicted = clf.predict(X_test)
        print('Prediction:\n', y_predicted)


    def run(self):
        self.fitting_linear_regression()
        self.fitting_decision_tree_regression()
