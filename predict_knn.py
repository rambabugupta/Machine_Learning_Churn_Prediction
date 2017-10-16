from __future__ import division
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.cross_validation import KFold
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier as RF
from sklearn.neighbors import KNeighborsClassifier as KNN



df = pd.read_csv('merged.csv')
col_names = df.columns.tolist()
is_returnable = df['is_returning_customer']
y = is_returnable
to_drop = ['customer_id','is_returning_customer'    ]
final_df = df.drop(to_drop,axis=1)


features = final_df.columns

print 'features list:-'
print features

X = final_df.as_matrix().astype(np.float)

scaler = StandardScaler()
X = scaler.fit_transform(X)


def predict_result(X,y, classification_methon, **kwargs):
    kf = KFold(len(y),n_folds=5,shuffle=False)
    y_prediction = y.copy()
    for train_index, test_index in kf:
        X_train, X_test = X[train_index], X[test_index]
        y_train = y[train_index]
        classification = classification_methon(**kwargs)
        classification.fit(X_train,y_train)
        y_prediction[test_index] = classification.predict(X_test)
    return y_prediction

def check_accuracy(y_true,y_prediction):
    return np.mean(y_true == y_prediction)


print 'KNN accuracy'
y_prediction = predict_result(X,y,KNN);
print "%.3f" % check_accuracy(y, y_prediction)

df_csv = pd.read_csv('merged.csv')
df_csv['predict_result'] = y_prediction
df_csv.to_csv('predict_knn.csv')



#CONFUSION METRICS
from sklearn.metrics import confusion_matrix
import pylab as pl
y = np.array(y)
class_names = np.unique(y)
confusion_matrices = confusion_matrix(y,y_prediction)
print confusion_matrices
pl.matshow(confusion_matrices)
pl.title('KNN')
pl.colorbar()
pl.show()