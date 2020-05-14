import csv
import numpy as np
from sklearn import preprocessing
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import plot_confusion_matrix
import matplotlib.pyplot as plt
import pandas as pd
from sklearn import metrics


in_data = pd.read_csv("data_json/data.csv", header=0)

in_data = in_data.dropna()

in_data = in_data.sample(frac=1).reset_index(drop=True)
print(in_data)

feature_cols = ['text_age','text_gender','image_age','image_gender','demographic_age','demographic_gender','demographic_ethnicity']
X = in_data[feature_cols]
y = in_data[['labels']]
print(y)



X_train,X_test,y_train,y_test=train_test_split(X,y,test_size=0.20,random_state=0)


model = LogisticRegression()

# fit the model with data
model.fit(X_train,y_train)

y_pred = model.predict(X_test)

cnf_matrix = metrics.confusion_matrix(y_test, y_pred)
print(cnf_matrix)

plot_confusion_matrix(model, X_test, y_test)  # doctest: +SKIP
plt.show()
