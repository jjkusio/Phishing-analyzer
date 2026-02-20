import re
import pandas as pd
import tldextract
from collections import Counter
from math import log
import nltk

df = pd.read_csv("top-1m.csv", usecols=[1], header=None)
safe_domains = set(df[1])

dd = pd.read_csv("top500Domains.csv", usecols=["Root Domain"])
popular_domains = set(dd["Root Domain"])

def check_http(url):
    if url.startswith("http:"):
        return 1
    return 0

def check_length(url):
    return len(url)
       

def check_tld(url):
    ext = tldextract.extract(url)
    url = "." + ext.suffix
    popular_domains = [".pl", ".com", ".eu", ".net", ".org", ".io"]
    for tld in popular_domains:
        if tld in url:
            return 1
    return 0

def check_ip(url):
    x = re.search(r"\b([0-9]{1,3}\.){3}[0-9]{1,3}\b", url)
    if x:
        return 1
    return 0

def check_latin(url):
    for letter in url:
        if (ord(letter) > 126 or ord(letter) < 32):
            return 1
    return 0

def check_whitelist(url, data):
    ext = tldextract.extract(url)
    if ext.subdomain !="":
        url = ext.subdomain + "." + ext.domain + "." + ext.suffix
    else:
        url = ext.domain + "." + ext.suffix
    if url in data:
        return 1
    return 0

def check_shannon_entropy(url):
    ext = tldextract.extract(url)
    url = ext.domain +"." + ext.suffix
    counts = Counter(url)
    frequencies = ((i / len(url)) for i in counts.values())
    result = -sum(f * log(f, 2) for f in frequencies)
    return result

def check_at(url):
    if "@" in url:
        return 1
    return 0

def check_characters(url):
    ext = tldextract.extract(url)
    url = ext.domain + "." + ext.suffix
    count = 0
    suspicious_characters=["?", "-", "_", "&", "*", "=", "%", "^", "#"]
    for letter in url:
        if letter in suspicious_characters:
            count += 1
    return count

def check_numbers(url):
    ext = tldextract.extract(url)
    url = ext.domain + "." + ext.suffix
    count = 0
    for char in url:
        if char.isdigit():
            count +=1
    return count

def check_subdomains(url):
    count = -1
    for char in url:
        if char == ".":
            count +=1
    return count

def check_sus_domains(url):
    list = [".ru", ".xyz", ".best", ".bid", ".click", ".info", ".zip", ".top", ".weebly"]
    for domain in list:
        if domain in url:
            return 1
    return 0

def check_keywords(url):
    PHISHING_KEYWORDS = [
    "login", "logon", "signin", "sign-in", "auth", "authenticate",
    "authentication", "verify", "verification", "validate",
    "validation", "confirm", "secure", "security", "account",
    "password", "passcode", "credential", "credentials",
    "reset", "recovery", "recover", "restore", "unlock",
    "reactivate", "update", "upgrade",
    "urgent", "alert", "warning", "suspended", "suspension",
    "blocked", "locked", "limited", "expire", "expired",
    "compromised", "breach", "unusual", "activity",
    "bank", "banking", "billing", "payment", "invoice",
    "transaction", "refund", "wallet", "card", "credit",
    "debit", "paypal", "stripe",
    "securelogin", "accountverify", "updateaccount",
    "confirmaccount", "verifyaccount", "resetpassword",
    "webscr", "ebayisapi", "wp-admin", "admin", "support"
]
    count = 0
    for word in PHISHING_KEYWORDS:
        if word in url:
            count +=1
    return count

def check_fake_domains(url, data):
    ext = tldextract.extract(url)
    url = ext.domain + "." + ext.suffix
    for domain in data:
        if domain in url and not check_whitelist(url, safe_domains):
            return 1
    return 0

def check_distance(url, data):
    lista = []
    ext = tldextract.extract(url)
    url = ext.domain
    for domain in data:
        dist = nltk.edit_distance(url, domain)
        lista.append(dist)
    dist1 = min(lista)
    return dist1

def is_free_hosting(url):
    free_hosts = [
        "weebly.com", "wixsite.com", "wordpress.com", "github.io", "freehostia.com",
        "000webhostapp.com", "bravesites.com", "jimdosite.com", "webnode.com",
        "vercel.app", "netlify.app", "herokuapp.com", "firebaseapp.com", 
        "web.app", "pages.dev", "glitch.me", "onrender.com", "azurewebsites.net",
        "forms.gle", "typeform.com", "jotform.com", "survey-smiles.com",
        "s3.amazonaws.com", "storage.googleapis.com", "sharepoint.com", "blob.core.windows.net",
        ]
    for host in free_hosts:
        if host in url:
            return 1
    return 0

def is_shortened(url):
    ext = tldextract.extract(url)
    url = ext.domain + "." + ext.suffix
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
    for element in shorteners_list:
        if element in url:
            return 1
    return 0
    
    
def features(url, safe, pop):
    features = {"HTTP": check_http(url),
    "URL Length": check_length(url),
    "Popular tld in URL": check_tld(url),
    "IP": check_ip(url),
    "Non-latin characters": check_latin(url),
    "URL IN WHITELIST": check_whitelist(url, safe),
    "Entropy": check_shannon_entropy(url),
    "@ in url": check_at(url),
    "Suspicious characters": check_characters(url),
    "Digits": check_numbers(url),
    "Subdomains": check_subdomains(url),
    "Sus domains": check_sus_domains(url),
    "Number of phishing words": check_keywords(url),
    "Popular domain and not in whitelist": check_fake_domains(url, safe),
    "Levenshtein Distance": check_distance(url,pop),
    "Free Hosting": is_free_hosting(url),
    "URL is shortened": is_shortened(url)
    }
    return features
