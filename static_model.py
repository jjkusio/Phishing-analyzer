import sqlite3
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_auc_score
from sklearn.metrics import classification_report, confusion_matrix
import xgboost as xgb
import matplotlib.pyplot as plt
import shap


data = pd.read_csv("data_35k.csv")
data = data.drop_duplicates()

dynamic = ["id", "url", "is_phish", "SSL/Connection", "Response length","Number of forms","Number of password forms","Number of 'text' forms","Number of hidden elements","Title vs domain",
"Text to html ratio","Number of iframe","Number of scripts","Number of suspicious keywords / response length","Domain age in days",
"Domain expires in ? days","Number of images","Number of links in HTML","Number of external links",
"History length (number of redirections)","whois available","domain changed", "Free Hosting"]

X_train = data.drop(columns=dynamic )
y_train = data["is_phish"]

model = xgb.XGBClassifier(
    learning_rate = 0.05,
    max_depth = 5,
    n_estimators = 500,
    subsample = 0.8,
    colsample_bytree = 0.4,
    colsample_bylevel=0.7,
    reg_alpha=0.1,   
    reg_lambda=2.0,
    min_child_weight=5,
    eval_metric = "auc",
    random_state = 42,
)
model.fit(X_train, y_train)
model.save_model("static_model.json")