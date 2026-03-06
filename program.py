import xgboost as xgb
from features.URL_stats import features
from features.dynamic_stats import features1, connection, whois_connect, connection_1
import pandas as pd
import tldextract
from colorama import init, Fore, Style
import pickle

shorteners_list = [
    "bit.ly", "bitly.kr", "bl.ink", "buff.ly", "clicky.me", "cutt.ly", 
    "dub.co", "fox.ly", "gg.gg", "han.gl", "is.gd", "kurzelinks.de", 
    "kutt.it", "lstu.fr", "oe.cd", "ow.ly", "rebrandly.com", "reduced.to", 
    "rip.to", "san.aq", "short.io", "shorten-url.com", "shorturl.at", 
    "spoo.me", "switchy.io", "tinu.be", "tinyurl.com", "t.ly", "urlr.me", 
    "v.gd", "vo.la", "yaso.su", "zlnk.com", "sor.bz", "73.nu", "lyn.bz",
    "shlink.io", "yourls.org", "polr.me",
    "git.io", "goo.gl", "me2.do", "cutit.org", "s2r.co", "soo.gd", "hoy.kr", "tr.ee"
    ]


static_model = xgb.XGBClassifier()
static_model.load_model("models/static_model.json")
dynamic_model = xgb.XGBClassifier()
dynamic_model.load_model("models/dynamic_model.json")

model_xgb = xgb.XGBClassifier()
model_xgb.load_model("models/meta_model_1.json")
with open("models/meta_model_lr.pkl", "rb") as f:
    model = pickle.load(f)
whitelist = pd.read_csv("majestic_million.csv", usecols=["Domain"], nrows=100000)
whitelist_domains = set(whitelist['Domain'])


with open("data_collection/spam.txt", "r", encoding="utf-8") as f:
    keywords = f.read()
dd = pd.read_csv("features/top500Domains.csv", usecols=["Root Domain"])
popular_domains = set(dd["Root Domain"])

url = input("Enter URL:")
response, score = connection(url)
if response is None:
    print(Fore.RED +"Invalid URL or website does not exist anymore!" + Style.RESET_ALL)
    exit()
ext = tldextract.extract(url)
root_domain = (ext.domain + "." + ext.suffix).lower()

if ext.subdomain:
       domain = ext.subdomain + "." + ext.domain + "." + ext.suffix
else:
       domain = root_domain

is_whitelist = False
if (domain in whitelist_domains):
        is_whitelist = True
for element in shorteners_list:
      if element in domain:
            is_whitelist = False
            break

if is_whitelist:
        print(Fore.GREEN + "URL is on whitelist: 0% PHISH" + Style.RESET_ALL)
else:

    #static
    static_results = features(url, popular_domains)
    static_data = pd.DataFrame([static_results])
    y_proba = static_model.predict_proba(static_data)[:,1]
    print(f"STATIC: This site is {y_proba[0] * 100:.2f}% phishing")
    #dynamic
    driver = connection_1()
    w,  available = whois_connect(url)
    try:   
        driver.get(url)
    except:
           print("No dynamic and meta result: This website does not exist / cannot reach the host")
           driver.quit()
           exit()
    dynamic_results = features1(url, response, driver, w, score, keywords,  available)
    data = pd.DataFrame([dynamic_results])
    data = data.apply(pd.to_numeric, errors='coerce')
    y_proba2 = dynamic_model.predict_proba(data)[:,1]
    print(f"DYNAMIC: This site is {y_proba2[0] * 100:.2f}% phishing")

    #meta model
    X = pd.DataFrame({
        "static_model": y_proba,
        "dynamic_model": y_proba2
    })
    meta_proba = model.predict_proba(X)[:,1]
    meta_proba_xgb = model_xgb.predict_proba(X)[:,1]
    print(f"META MODEL LR: This site is {meta_proba[0] * 100:.2f}% phishing")
    print(f"META MODEL XGB: This site is {meta_proba_xgb[0] * 100:.2f}% phishing")
    driver.quit()