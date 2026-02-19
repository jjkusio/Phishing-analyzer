import re
import pandas as pd
import tldextract
from collections import Counter
from math import log

df = pd.read_csv("top-1m.csv", usecols=[1], header=None)
safe_domains = set(df[1])

def check_http(url):
    if url.startswith("http:"):
        return True
    return False

def check_length(url):
    if len(url) > 150:
        return True
    return False

def check_domain(url):
    popular_domains = [".pl", ".com", ".eu", ".net", ".org", ".io"]
    for tld in popular_domains:
        if tld in url:
            return False
    return True

def check_ip(url):
    x = re.search(r"\b([0-9]{1,3}\.){3}[0-9]{1,3}\b", url)
    if x:
        return True
    return False

def check_latin(url):
    for letter in url:
        if (ord(letter) > 126 or ord(letter) < 32):
            return True
    return False

def check_whitelist(url, data):
    ext = tldextract.extract(url)
    url = ext.domain + "." + ext.suffix
    if url in data:
        return False
    return True

def check_shannon_entropy(url):
    counts = Counter(url)
    frequencies = ((i / len(url)) for i in counts.values())
    result = -sum(f * log(f, 2) for f in frequencies)
    if result > 3.2:
        return True
    return False

def check_at(url):
    if "@" in url:
        return True
    return False

def check_characters(url):
    count = 0
    suspicious_characters=["?", "-", "_", "&", "*", "=", "%", "^", "#"]
    for letter in url:
        if letter in suspicious_characters:
            count += 1
    if count > 4:
        return True
    return False

def check_numbers(url):
    count = 0
    for char in url:
        if char.isdigit():
            count +=1
    if count > 3:
        return True
    return False

def check_subdomains(url):
    count = 0
    for char in url:
        if char == ".":
            count +=1
    if count > 3:
        return True
    return False

def check_sus_domains(url):
    list = [".ru", ".xyz", ".best", ".bid", ".click", ".info", ".zip", ".top"]
    for domain in list:
        if domain in url:
            return True
    return False

def group1(url):
    points = 0
    if check_ip(url): points +=3
    if check_numbers(url): points +=2
    if check_subdomains(url): points +=2
    if points > 5:
        points = 5
    return points


def group2(url):
    points = 0
    if check_length(url): points+=1
    if check_domain(url): points+=1
    if check_latin(url): points+=2
    if check_characters(url): points+=2
    if check_at(url): points+=3
    if check_shannon_entropy(url): points+=3
    if check_sus_domains(url): points+=3
    if check_http(url): points += 2
    if points > 12:
        points = 12
    return points

def points_count(url):
    if check_whitelist(url, safe_domains) == False:
        return 0
    total = group1(url) + group2(url)
    return total


url = input("Enter URL link: ")
print("Final score:", points_count(url))
