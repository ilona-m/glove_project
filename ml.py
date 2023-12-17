### This file reads the gesture files, builds the ML model and evaluates different charasteristics.

import os
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import confusion_matrix, classification_report

# Reading the gesture files and saving them to a list:

directory = 'datasets/' 
file_list = [f for f in os.listdir(directory) if f.endswith('.csv')]
file_list.sort()

# Adding the files to a dataframe for easier handling:

data = []
labels = []

i = 0
for filename in file_list:
    df = pd.read_csv(os.path.join(directory, filename), header=None)
    data.append(df.values)
    labels.append(i)
    i += 1

flat_data = []
for d in data:
    for line in d:
        flat_data.append(line)
data = pd.DataFrame(flat_data)

# Labeling the data:

repeated_labels = []
for label in labels:
    for i in range(50000):
        repeated_labels.append(label)
labels = pd.Series(repeated_labels)

# Dividing the data into training and testing sets:

X_train, X_test, y_train, y_test = train_test_split(data, labels, test_size=0.2, random_state=42)

# Creating the random forest classifier and fitting the data (training the model):

clf = RandomForestClassifier(n_estimators=100, max_depth=10)
clf.fit(X_train, y_train)

# Testing accuracies of different things:

predictions = clf.predict(X_test)
accuracy = accuracy_score(y_test, predictions)
print(f"Validation accuracy: {accuracy}")

#combined = pd.read_csv("testsets1/concatted")
#com_predictions = clf.predict(combined)
#indexes = [0,8,2,6,4,7,5,3,9,1]
#times = [2000,2000,2000,2000,2000,2000,2000,2000,2000,2000]
#classes = np.repeat(indexes, times)
#com_accuracy = accuracy_score(classes, com_predictions)
#print(f"Accuracy of one test subject: {com_accuracy}")

# Exporting the model:

import pickle
final_model = [] 

final_model.append(clf)

with open('model', 'wb') as file:
    pickle.dump(final_model, file)

# Saving a picture of a decision tree:

from sklearn import tree
import matplotlib.pyplot as plt
fig, axes = plt.subplots(nrows = 1,ncols = 1,figsize = (4,4), dpi=800)
tree.plot_tree(clf.estimators_[0], feature_names = ['s' + str(k) for k in range(1,8)], class_names=file_list, filled = True)
fig.savefig('tree.png')

# Printing a confusion Matrix:

conf_matrix = confusion_matrix(y_test, predictions)
print("\nConfusion Matrix:")
print(conf_matrix)

# Printing a classification report
class_report = classification_report(y_test, predictions)
print("\nClassification Report:")
print(class_report)