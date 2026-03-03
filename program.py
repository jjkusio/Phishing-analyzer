import xgboost as xgb
from URL_stats import features
from dynamic_stats import features1, connection, whois_connect, connection_1
import pandas as pd

with open("spam.txt", "r", encoding="utf-8") as f:
        keywords = f.read()
driver = connection_1()
dd = pd.read_csv("top500Domains.csv", usecols=["Root Domain"])
popular_domains = set(dd["Root Domain"])
url = input("Enter URL:")

#static
static_model = xgb.XGBClassifier()
static_model.load_model("static_model.json")
static_results = features(url, popular_domains)
static_data = pd.DataFrame([static_results])
y_predict = static_model.predict(static_data)
y_proba = static_model.predict_proba(static_data)[:,1]
print(f"STATIC: This site is {y_proba[0] * 100:.2f}% phishing")

#dynamic
response, score = connection(url)
w,  available = whois_connect(url)
driver.get(url)
dynamic_results = features1(url, response, driver, w, score, keywords,  available)
results = static_results | dynamic_results
data = pd.DataFrame([results])
data = data.apply(pd.to_numeric, errors='coerce')
dynamic_model = xgb.XGBClassifier()
dynamic_model.load_model("dynamic_model.json")
data = pd.DataFrame([dynamic_results])
data = data.apply(pd.to_numeric, errors='coerce')
y_proba2 = dynamic_model.predict_proba(data)[:,1]
print(f"DYNAMIC: This site is {y_proba2[0] * 100:.2f}% phishing")

#meta model
model = xgb.XGBClassifier()
model.load_model("meta_model_1.json")
X = pd.DataFrame({
    "static_model": y_proba,
    "dynamic_model": y_proba2
})
meta_proba = model.predict_proba(X)[:,1]
print(f"META MODEL: This site is {meta_proba[0] * 100:.2f}% phishing")
print(static_results)
print(dynamic_results) 
