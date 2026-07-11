from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import xgboost as xgb
from features.URL_stats import features
from features.dynamic_stats import features1, connection, whois_connect, connection_1
import pandas as pd
import tldextract
import pickle
import re
import socket
import ipaddress
import urllib3

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


app = FastAPI()
class Url(BaseModel):
    url: str

@app.post("/v1/analyze")
def info(url: Url):
    valid = False
    is_whitelist = False
    static = None
    Dynamic = None
    Meta_X = None
    Meta_Lr = None
    url = url.url
<<<<<<< HEAD
    if not url.startswith(("http://", "https://")):
        raise HTTPException(status_code=403, detail="Server refused to answer")
=======
>>>>>>> 23a8abd (new docker test)
    ip = re.search(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})',url)
    if ip:
        raise HTTPException(status_code=403, detail="Server refused to answer")
    def extracting(url):
        domena = tldextract.extract(url)
        if domena.subdomain:
            urel = domena.subdomain + "." + domena.domain + "." + domena.suffix
        else:
            urel = domena.domain + "." + domena.suffix
        return urel

    urel = extracting(url)
    try:
        ip_from_url = socket.gethostbyname(urel)
<<<<<<< HEAD
    except socket.gaierror:
=======
    except:
>>>>>>> 23a8abd (new docker test)
        raise HTTPException(status_code=400, detail="Cannot resolve a hostname")
    def safety_check(url):
        is_private = ipaddress.IPv4Address(url).is_private
        is_loopback = ipaddress.IPv4Address(url).is_loopback
        return is_private, is_loopback

    private, loopback = safety_check(ip_from_url)
    if private or loopback:
        raise HTTPException(status_code=403, detail="Server refused to answer")

    url = url.replace("www.","", 1)
    response, score = connection(url)
    if response:
        if len(response.history) > 0:
            urel = response.url
            urel = extracting(urel)
            try:
                ip_from_url = socket.gethostbyname(urel)
<<<<<<< HEAD
            except socket.gaierror:
=======
            except:
>>>>>>> 23a8abd (new docker test)
                raise HTTPException(status_code=400, detail="Cannot resolve a hostname")
            priv, loop = safety_check(ip_from_url)
            if priv or loop:
                raise HTTPException(status_code=403, detail="Server refused to answer")

    ext = tldextract.extract(url)
    root_domain = (ext.domain + "." + ext.suffix).lower()

    if ext.subdomain:
       full_domain = ext.subdomain + "." + ext.domain + "." + ext.suffix
       full_domain1 = ext.subdomain + "." + ext.domain
    else:
        full_domain = root_domain
        full_domain1 = ext.domain
    domain = full_domain.lower().removeprefix("www.")
    domain1 = full_domain1.lower().removeprefix("www.")

    if (domain in whitelist_domains or domain1 in whitelist_domains):
        is_whitelist = True
    for element in shorteners_list:
        if element in domain:
                is_whitelist = False
                break
    if is_whitelist:
        return {
        "Valid": valid,
        "Whitelist": is_whitelist,
        "Static": static,
        "Dynamic": Dynamic,
        "Meta_XGB": Meta_X,
        "Meta_LR": Meta_Lr
        }
    #static
    static_results = features(url, popular_domains)
    static_data = pd.DataFrame([static_results])
    y_proba = static_model.predict_proba(static_data)[:,1]
    #dynamic
    driver = connection_1()
    w,  available = whois_connect(url)
<<<<<<< HEAD
    try:
        try:   
            driver.get(url)
        except:
            raise HTTPException(status_code = 504, detail="Gateway Timeout")
        try:
                valid = True
                dynamic_results = features1(url, response, driver, w, score, keywords,  available)
                data = pd.DataFrame([dynamic_results])
                data = data.apply(pd.to_numeric, errors='coerce')
                y_proba2 = dynamic_model.predict_proba(data)[:,1]
                #meta model
                X = pd.DataFrame({
                    "static_model": y_proba,
                    "dynamic_model": y_proba2
                })
                meta_proba = model.predict_proba(X)[:,1]
                meta_proba_xgb = model_xgb.predict_proba(X)[:,1]
        except:
                raise HTTPException(status_code = 500, detail="Internal Server Error")
    finally:
        driver.quit()
=======
    try:   
        driver.get(url)
    except:
        driver.quit()
        raise HTTPException(status_code = 504, detail="Gateway Timeout")
    valid = True
    dynamic_results = features1(url, response, driver, w, score, keywords,  available)
    data = pd.DataFrame([dynamic_results])
    data = data.apply(pd.to_numeric, errors='coerce')
    y_proba2 = dynamic_model.predict_proba(data)[:,1]


    #meta model
    X = pd.DataFrame({
        "static_model": y_proba,
        "dynamic_model": y_proba2
    })
    meta_proba = model.predict_proba(X)[:,1]
    meta_proba_xgb = model_xgb.predict_proba(X)[:,1]
    driver.quit()
>>>>>>> 23a8abd (new docker test)
    static = y_proba
    Dynamic = y_proba2
    Meta_X = meta_proba_xgb
    Meta_Lr = meta_proba
    return {
    "Valid": valid,
    "Whitelist": is_whitelist,
    "Static": f"{static[0] * 100:.2f}%",
    "Dynamic": f"{Dynamic[0] * 100:.2f}%",
    "Meta_XGB": f"{Meta_X[0] * 100:.2f}%",
    "Meta_LR": f"{Meta_Lr[0] * 100:.2f}%"
    }
@app.get("/healthz")
def health():
    return {"Status": "OK"}