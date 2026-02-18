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
        return 3
    return 0

def check_length(url):
    if len(url) > 150:
        return 1
    return 0

def check_domain(url):
    popular_domains = [".pl", ".com", ".eu", ".net", ".org", ".io"]
    for tld in popular_domains:
        if tld in url:
            return 0
    return 1

def check_ip(url):
    x = re.search(r"\b([0-9]{1,3}\.){3}[0-9]{1,3}\b", url)
    if x:
        return 3
    return 0

def check_latin(url):
    for letter in url:
        if (ord(letter) > 126 or ord(letter) < 32):
            return 3
    return 0

def check_whitelist(url, data):
    ext = tldextract.extract(url)
    url = ext.domain + "." + ext.suffix
    if url in data:
        return 0
    return 1

def check_shannon_entropy(url):
    counts = Counter(url)
    frequencies = ((i / len(url)) for i in counts.values())
    result = -sum(f * log(f, 2) for f in frequencies)
    if result > 3.2:
        return 3
    return 0

def check_at(url):
    if "@" in url:
        return 3
    return 0

def check_characters(url):
    count = 0
    suspicious_characters=["?", "-", "_", "&", "*", "=", "%", "^", "#"]
    for letter in url:
        if letter in suspicious_characters:
            count += 1
    if count > 4:
        return 2
    return 0

def check_numbers(url):
    count = 0
    for char in url:
        if char.isdigit():
            count +=1
    if count > 3:
        return 2
    return 0

def check_subdomains(url):
    count = 0
    for char in url:
        if char == ".":
            count +=1
    if count > 3:
        return 2
    return 0

def check_sus_domains(url):
    list = [".ru", ".xyz", ".best", ".bid", ".click", ".info", ".zip", ".top"]
    for domain in list:
        if domain in url:
            return 2
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
    for word in PHISHING_KEYWORDS:
        if word in url:
            return 2
    return 0

def check_fake_domains(url, data):
    ext = tldextract.extract(url)
    url = ext.domain + "." + ext.suffix
    for domain in data:
        if domain in url and check_whitelist(url, safe_domains):
            return 4
    return 0

def check_distance(url, data):
    ext = tldextract.extract(url)
    url = ext.domain
    for domain in data:
        if (nltk.edit_distance(url, domain) == 1):
            return 4
        elif (nltk.edit_distance(url, domain) == 2):
            return 2
        else:
            return 0
    return 0
    

def points_count(url):
    total = 0
    if check_whitelist(url, safe_domains) == False:
        return 0
    check_list = [check_latin, check_at, check_characters, check_distance, check_domain, check_fake_domains, check_http, 
                  check_ip, check_keywords, check_shannon_entropy, check_numbers]
    for func in check_list:
        if func in [check_fake_domains, check_distance]:
            total += func(url, popular_domains)
        else:
            total += func(url)
    return total


url = input("Enter URL link: ")
print("Final score:", points_count(url))
