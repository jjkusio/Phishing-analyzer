import sqlite3
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_auc_score
from sklearn.metrics import classification_report, confusion_matrix
import xgboost as xgb

conn = sqlite3.connect("data.db")
data = pd.read_sql("SELECT * FROM results", conn)
data = data.drop_duplicates()

X = data.drop(columns=["id", "url", "is_phish"])
y = data["is_phish"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

model = xgb.XGBClassifier(
    learning_rate = 0.08,
    max_depth = 7,
    n_estimators = 600,
    subsample = 0.8,
    colsample_bytree = 0.8,
    eval_metric = "auc",
    random_state = 42,
)
model.fit(X_train, y_train)
y_predict = model.predict(X_test)
y_proba = model.predict_proba(X_test)[:,1]

print("AUC", roc_auc_score(y_test, y_proba))
print(classification_report(y_test, y_predict))
matrix = confusion_matrix(y_test, y_predict)
print("False positives:", matrix[0][1])
print("False negatives:", matrix[1][0])

model.save_model("model.json")