import sqlite3
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_auc_score
from sklearn.metrics import classification_report, confusion_matrix
import xgboost as xgb
import shap
import matplotlib.pyplot as plt

data = pd.read_csv("data_35k.csv")
data = data.drop_duplicates()

static = ["id", "url", "is_phish", "HTTP",
"URL Length",
"Popular tld in URL",
"IP",
"Non-latin characters",
"Entropy",
"@ in url",
"Suspicious characters",
"Digits",
"Subdomains",
"Sus domains",
"Number of phishing words",
"Levenshtein Distance",
"Free Hosting",
"URL is shortened"]

X_train = data.drop(columns=static)
y_train = data["is_phish"]

model = xgb.XGBClassifier(
    learning_rate = 0.08,
    max_depth = 7,
    n_estimators = 600,
    subsample = 0.7,
    colsample_bytree = 0.8,
    eval_metric = "auc",
    random_state = 42,
)
model.fit(X_train, y_train)
model.save_model("models/dynamic_model.json")
