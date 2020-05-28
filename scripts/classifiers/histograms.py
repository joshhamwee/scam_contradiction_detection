import json
import os
import argparse
import random
import re
import csv
import numpy as np
from sklearn import preprocessing
from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import ShuffleSplit
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import plot_confusion_matrix

import matplotlib.pyplot as plt
import pandas as pd
from sklearn import metrics


in_data = pd.read_csv("data_json/data.csv", header=0)

in_data = in_data.dropna()

in_data = in_data.sample(frac=1).reset_index(drop=True)

feature_cols = ['text_age','text_gender','image_age','image_gender','demographic_age','demographic_gender','demographic_ethnicity','image_demographic_gender','text_image_age']
X = in_data[feature_cols]
y = in_data[['labels']]

min_max_scaler = preprocessing.MinMaxScaler()
X = min_max_scaler.fit_transform(X)


array_real = []
array_scam = []

for i in range(len(y)):
    if y['labels'][i] == 0:
        array_real.append(X[i][7])
    if y['labels'][i] == 1:
        array_scam.append(X[i][7])

print("Mean real: ", np.mean(array_real))
print("Mean scam: ", np.mean(array_scam))

count_real = 0
count_scam = 0
for i in range(len(array_real)):
    if array_real[i] > 0.05:
        count_real += 1

for i in range(len(array_scam)):

    if array_scam[i] > 0.05:
        count_scam += 1

print("Proportion > 0 real: ", count_real/len(array_real))
print("Proportion > 0 scam: ", count_scam/len(array_scam))

plt.hist(array_real,bins=30,color='teal')
plt.axvline(np.mean(array_real), color='k', linestyle='dashed', linewidth=1)
min_ylim, max_ylim = plt.ylim()
plt.text(np.mean(array_real)*1.1, max_ylim*0.9, 'Mean: {:.2f}'.format(np.mean(array_real)))
plt.xlabel("image_imag2_gender value of inconsistency")
plt.ylabel("Frequency of inconsistency value")
plt.title("Real Users")
plt.show()

plt.hist(array_scam,bins=30,color='teal')
plt.axvline(np.mean(array_scam), color='k', linestyle='dashed', linewidth=1)
min_ylim, max_ylim = plt.ylim()
plt.text(np.mean(array_scam)*1.1, max_ylim*0.9, 'Mean: {:.2f}'.format(np.mean(array_scam)))
plt.xlabel("image_imag2_gender value of inconsistency")
plt.ylabel("Frequency of inconsistency value")
plt.title("Scam Users")
plt.show()
