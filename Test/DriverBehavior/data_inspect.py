# Import 

import sys
import pandas as pd

sys.path.append('')

from xgboost import XGBClassifier, XGBRFClassifier
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split

# Functions

if __name__ == '__main__':
    df = pd.read_csv('./Data/DriverBehavior/features_14.csv')

    # reduce each target with 1
    df['Target'] = df['Target'] - 1
    
    # split data 50/50  
    X_train, X_test, y_train, y_test = train_test_split(
        df.drop('Target', axis=1), df['Target'], test_size=0.5, random_state=42)


    model = XGBClassifier(verbosity = 2, max_depth = 5, n_estimators = 10, learning_rate = 0.1, eval_metric = accuracy_score)
    # model = XGBRFClassifier()
    model.fit(X_train, y_train, eval_set = [(X_test, y_test)], verbose = True)

    y_pred = model.predict(X_test)
    predictions = [round(value) for value in y_pred]

    # evaluate predictions
    accuracy = accuracy_score(y_test, predictions)
    print("Accuracy: %.2f%%" % (accuracy * 100.0))