from fastapi import FastAPI, HTTPException, Request
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
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
import logging

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
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)
static_model = xgb.XGBClassifier()
try:
    static_model.load_model("models/static_model.json")
    logger.info("Static model loaded")
except Exception:
    logger.critical("Failed to load static model", exc_info=True)
    raise
dynamic_model = xgb.XGBClassifier()
try:    
    dynamic_model.load_model("models/dynamic_model.json")
    logger.info("Dynamic model loaded")
except Exception:
    logger.critical("Failed to load dynamic model", exc_info=True)
    raise

model_xgb = xgb.XGBClassifier()
try:
    model_xgb.load_model("models/meta_model_1.json")
    logger.info("XGB model loaded")
except Exception:
    logger.critical("Failed to load XGB model", exc_info=True)
    raise
try:
    with open("models/meta_model_lr.pkl", "rb") as f:
        model = pickle.load(f)
    logger.info("LR model loaded")
except Exception:
    logger.critical("Failed to load LR model", exc_info=True)
    raise


try:
    whitelist = pd.read_csv("majestic_million.csv", usecols=["Domain"], nrows=100000)
    whitelist_domains = set(whitelist["Domain"])
    logger.info("Loaded whitelist")
except Exception:
    logger.critical("Failed to load whitelist", exc_info=True)
    raise

try:
    with open("data_collection/spam.txt", "r", encoding="utf-8") as f:
        keywords = f.read()
    logger.info("Loaded spam.txt")
except Exception:
    logger.critical("Failed to load spam.txt", exc_info=True)
    raise

try:
    dd = pd.read_csv("features/top500Domains.csv", usecols=["Root Domain"])
    popular_domains = set(dd["Root Domain"])
    logger.info("Loaded top500.csv")
except Exception:
    logger.critical("Failed to load top500.csv", exc_info=True)
    raise


app = FastAPI()
class Url(BaseModel):
    url: str

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
@app.post("/v1/analyze")
@limiter.limit("10/minute")
def info(url: Url, request: Request):
    valid = False
    is_whitelist = False
    static = None
    Dynamic = None
    Meta_X = None
    Meta_Lr = None

    url = url.url

    if not url.startswith(("http://", "https://")):
        raise HTTPException(status_code=403, detail="Server refused to answer")

    def extracting(url):
        domena = tldextract.extract(url)
        if domena.subdomain:
            urel = domena.subdomain + "." + domena.domain + "." + domena.suffix
        else:
            urel = domena.domain + "." + domena.suffix
        return urel
    
    urel = extracting(url)
    ip = re.search(r"(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})", urel)
    if ip:
        raise HTTPException(status_code=403, detail="Server refused to answer")

    try:
        ip_from_url = socket.gethostbyname(urel)
    except socket.gaierror:
        raise HTTPException(status_code=400, detail="Cannot resolve a hostname")

    def safety_check(url):
        is_private = ipaddress.IPv4Address(url).is_private
        is_loopback = ipaddress.IPv4Address(url).is_loopback
        return is_private, is_loopback

    private, loopback = safety_check(ip_from_url)

    if private or loopback:
        logger.warning(f"{url} is loopback/private address")
        raise HTTPException(status_code=403, detail="Server refused to answer")

    ext = tldextract.extract(url)
    root_domain = (ext.domain + "." + ext.suffix).lower()
    if root_domain in whitelist_domains:
        if not ext.subdomain or ext.subdomain == "www":
            is_whitelist = True
    if root_domain in shorteners_list:
        is_whitelist = False


    if is_whitelist:
        logger.info(f"{url} is on whitelist, no further analysis...")
        return {
            "Valid": True,
            "Whitelist": is_whitelist,
            "Static": static,
            "Dynamic": Dynamic,
            "Meta_XGB": Meta_X,
            "Meta_LR": Meta_Lr,
        }


    response, score = connection(url)
    if response:
        if len(response.history) > 0:
            urel = response.url
            urel = extracting(urel)
            try:
                ip_from_url = socket.gethostbyname(urel)
            except socket.gaierror:
                raise HTTPException(status_code=400, detail="Cannot resolve a hostname")

            priv, loop = safety_check(ip_from_url)

            if priv or loop:
                logger.warning(f"{url} redirected to loopback/private address")
                raise HTTPException(status_code=403, detail="Server refused to answer")



    # static
    static_results = features(url, popular_domains)
    static_data = pd.DataFrame([static_results])
    y_proba = static_model.predict_proba(static_data)[:, 1]

    # dynamic
    driver = connection_1()
    
    try:
        try:
            driver.get(url)
            w, available = whois_connect(url)
        except Exception as s:
            logger.error(f"Failed to load {url} on driver", exc_info=True)
            raise HTTPException(status_code=504, detail="Gateway Timeout")

        try:
            valid = True
            dynamic_results = features1(
                url, response, driver, w, score, keywords, available
            )
            data = pd.DataFrame([dynamic_results])
            data = data.apply(pd.to_numeric, errors="coerce")
            y_proba2 = dynamic_model.predict_proba(data)[:, 1]

            # meta model
            X = pd.DataFrame(
                {
                    "static_model": y_proba,
                    "dynamic_model": y_proba2,
                }
            )

            meta_proba = model.predict_proba(X)[:, 1]
            meta_proba_xgb = model_xgb.predict_proba(X)[:, 1]

        except Exception as s:
            logger.error(f"Analysis failed for {url}", exc_info=True)
            raise HTTPException(status_code=500, detail="Internal Server Error")

    finally:
        driver.quit()

    static = y_proba
    Dynamic = y_proba2
    Meta_X = meta_proba_xgb
    Meta_Lr = meta_proba
    logger.info(f"Analysis on {url} completed...")
    return {
        "Valid": valid,
        "Whitelist": is_whitelist,
        "Static": f"{static[0] * 100:.2f}%",
        "Dynamic": f"{Dynamic[0] * 100:.2f}%",
        "Meta_XGB": f"{Meta_X[0] * 100:.2f}%",
        "Meta_LR": f"{Meta_Lr[0] * 100:.2f}%",
    }



@app.get("/healthz")
def health():
    return {"Status": "OK"}