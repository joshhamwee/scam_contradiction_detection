
import csv
import numpy as np
from sklearn import preprocessing
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import plot_confusion_matrix
from sklearn.metrics import precision_recall_fscore_support
import matplotlib.pyplot as plt
import pandas as pd
from sklearn import metrics


in_data = pd.read_csv("data_json/data.csv", header=0)

in_data = in_data.dropna()

in_data = in_data.sample(frac=1).reset_index(drop=True)


# feature_cols = ['text_age','text_gender','image_age','image_gender','demographic_age','demographic_gender','demographic_ethnicity','image_demographic_gender','text_image_age']
feature_cols = ['text_age','text_gender','image_age','image_gender','demographic_age','demographic_gender','demographic_ethnicity']

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

    #Create a Gaussian Classifier
    model = RandomForestClassifier()


    # Train the model using the training sets
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
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

    features_imp_average = np.add(features_imp_average,model.feature_importances_)

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

features_imp_average = np.divide(features_imp_average,10)
for i in range(len(feature_cols)):
    print(feature_cols[i], ": ", features_imp_average[i])


features = ['text_age','text_gender','image_age','image_gender','image2_age','image2_gender','image2_ethnicity']
importances = features_imp_average
indices = np.argsort(importances)

plt.title('Feature Importances of Random Forests Classifier')
plt.barh(range(len(indices)), importances[indices], color='teal', align='center')
plt.yticks(range(len(indices)), [features[i] for i in indices])
plt.xlabel('Relative Importance')
plt.show()
