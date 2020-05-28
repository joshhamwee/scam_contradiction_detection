from sklearn.ensemble import VotingClassifier
import csv
import numpy as np
from sklearn import preprocessing
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn import svm
from sklearn.metrics import plot_confusion_matrix
from sklearn.metrics import precision_recall_fscore_support
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
import matplotlib.pyplot as plt
import pandas as pd
from sklearn import metrics


in_data = pd.read_csv("data_json/data.csv", header=0)

in_data = in_data.dropna()

in_data = in_data.sample(frac=1).reset_index(drop=True)


feature_cols = ['text_age','text_gender','image_age','image_gender','demographic_age','demographic_gender','demographic_ethnicity','image_demographic_gender','text_image_age']
# feature_cols = ['text_age','text_gender','image_age','image_gender','demographic_age','demographic_gender','demographic_ethnicity']

X = in_data[feature_cols]
y = in_data[['labels']]

X = np.array(X)
y = np.array(y)

min_max_scaler = preprocessing.MinMaxScaler()
X = min_max_scaler.fit_transform(X)

average_cnf_matrix = [0,0,0,0]

real_precision = 0
scam_precision = 0

real_recall = 0
scam_recall = 0

real_f1 = 0
scam_f1 = 0

features_imp_average = np.zeros(len(feature_cols))



for i in range(0,10):

    X_train,X_test,y_train,y_test=train_test_split(X,y,test_size=0.20)

    #Create a all classifier Classifier
    classifiers = []
    classifiers.append(('RF', RandomForestClassifier()))
    classifiers.append(('DT', DecisionTreeClassifier(criterion="entropy",min_samples_split=3,max_features=5,min_samples_leaf=5)))
    # classifiers.append(('KNN', KNeighborsClassifier(n_neighbors=5)))
    classifiers.append(('NB', GaussianNB()))

    model = VotingClassifier(estimators = classifiers, voting ='hard')
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    # Train the model using the training sets

    scores = precision_recall_fscore_support(y_test,y_pred)
    print(scores)
    scores[0][0]

    real_precision += scores[0][0]
    scam_precision += scores[0][1]

    real_recall += scores[1][0]
    scam_recall += scores[1][1]

    real_f1 += scores[2][0]
    scam_f1 += scores[2][1]

    cnf_matrix = metrics.confusion_matrix(y_test, y_pred)
    average_cnf_matrix[0] += cnf_matrix[0][0]
    average_cnf_matrix[1] += cnf_matrix[0][1]
    average_cnf_matrix[2] += cnf_matrix[1][0]
    average_cnf_matrix[3] += cnf_matrix[1][1]


average_cnf_matrix = np.divide(average_cnf_matrix,10)
print("Confusion matrix:", average_cnf_matrix)
print("real_precision",real_precision/10)
print("scam_precision",scam_precision/10)
print("real_recall",real_recall/10)
print("scam_recall",scam_recall/10)
print("real_f1",real_f1/10)
print("scam_f1",scam_f1/10)

print("average precision",(real_precision+scam_precision)/20)
print("average recall",(real_recall+scam_recall)/20)
print("average f1",(real_f1+scam_f1)/20)
