import sqlite3
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_auc_score
from sklearn.metrics import classification_report, confusion_matrix
import xgboost as xgb
from sklearn.linear_model import LogisticRegression

data = pd.read_csv("data_10k.csv")
data = data.drop_duplicates()

static_model = xgb.XGBClassifier()
dynamic_model = xgb.XGBClassifier()
static_model.load_model("static_model.json")
dynamic_model.load_model("dynamic_model.json")

dynamic = ["id", "url", "is_phish", "SSL/Connection", "Response length","Number of forms","Number of password forms","Number of 'text' forms","Number of hidden elements","Title vs domain",
"Text to html ratio","Number of iframe","Number of scripts","Number of suspicious keywords / response length","Domain age in days",
"Domain expires in ? days","Number of images","Number of links in HTML","Number of external links",
"History length (number of redirections)","whois available","domain changed"]

static = ["id", "url", "is_phish", "HTTP","URL Length","Popular tld in URL","IP","Non-latin characters","Entropy",
"@ in url","Suspicious characters","Digits","Subdomains","Sus domains","Number of phishing words","Levenshtein Distance","Free Hosting","URL is shortened"]

static_data = data.drop(columns=dynamic)
dynamic_data = data.drop(columns=static)
y = data["is_phish"]

y_static_proba = static_model.predict_proba(static_data)[:,1]
y_dynamic_proba = dynamic_model.predict_proba(dynamic_data)[:,1]

X_meta = pd.DataFrame({
    "static_model": y_static_proba,
    "dynamic_model": y_dynamic_proba,
})

model = xgb.XGBClassifier(
    n_estimators = 75,
    max_depth = 2,
    learning_rate = 0.1,
    eval_metric = "auc",
    random_state = 42,
    use_label_encoder = False,
    enable_categorical = False
)
model.fit(X_meta, y)

model_lr = LogisticRegression()
model_lr.fit(X_meta, y)

data_test = pd.read_csv("data_test.csv")
data_test = data_test.drop_duplicates()

y_test = data_test["is_phish"]
static_test = data_test.drop(columns=dynamic)
dynamic_test = data_test.drop(columns=static)

test_static_proba = static_model.predict_proba(static_test)[:,1]
test_dynamic_proba=dynamic_model.predict_proba(dynamic_test)[:,1]

X_test = pd.DataFrame({
    "static_model": test_static_proba,
    "dynamic_model": test_dynamic_proba
})

test_proba = model.predict_proba(X_test)[:,1]
test_predict = model.predict(X_test)

print("AUC", roc_auc_score(y_test, test_proba))
print(classification_report(y_test, test_predict))
matrix = confusion_matrix(y_test, test_predict)
print("False positives:",matrix[0][1])
print("False negatives:",matrix[1][0])

model.save_model("meta_model_1.json")