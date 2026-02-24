import requests
from selenium import webdriver
from selenium_stealth import stealth
from selenium.webdriver.chrome.options import Options
import whois
from datetime import datetime, timezone
import time
import tldextract
from selenium.webdriver.common.by import By
import nltk


def connection(url):
    response = None
    try:
        response = requests.get(url, timeout=3, allow_redirects=True)
    except requests.exceptions.SSLError:
        return response, 1
    except requests.exceptions.RequestException:
        return response, 0.5
    return response, 0
    
def response_length(response):
    if response == -1:
        return None
    return len(response.text)

def history_length(response):
    if response == -1:
        return None
    return len(response.history)

def domain_change(response, url):
    if response == -1:
        return None
    try:
        ext1 = tldextract.extract(response.url)
        ext2 = tldextract.extract(url)
        if (ext1.domain + "." + ext1.suffix != ext2.domain +"." + ext2.suffix):
            return 1
        else:
            return 0
    except:
        return 0

        
def forms(driver):
    try:
        forms = driver.find_elements("tag name", "form")
        return len(forms)
    except:
        return 0

def links(driver):
    try:
        links = driver.find_elements(By.TAG_NAME, 'a')
        return len(links)
    except:
        return 0
    
def external_links(driver, url):
    ext2 = tldextract.extract(url)
    ext2 = ext2.domain + "." + ext2.suffix
    count = 0
    try:
        links = driver.find_elements(By.TAG_NAME, 'a')
        for link in links:
            link_data = link.get_attribute('href')
            if link_data is None or link_data.lower().startswith("http") == False:
                continue
            ext1 = tldextract.extract(link_data)
            ext1 = ext1.domain + "." + ext1.suffix
            if ext1 != ext2:    
                count+=1
        return count
    except:
        return 0

def password_forms(driver):
    try:
        passwords = driver.find_elements("xpath", "//input[@type='password']")
        return len(passwords)
    except:
        return 0

def text_forms(driver):
    try:
        texts = driver.find_elements("xpath", "//input[@type='text']")
        return len(texts)
    except:
        return 0
    
def hidden(driver):
    try:
        hidden = driver.find_elements("xpath", "//input[@type='hidden']")
        return len(hidden)
    except:
        return 0
    
def img(driver):
    try:
        images = driver.find_elements("tag name", "img")
        return len(images)
    except:
        return 0
    
def iframe(driver):
    try:
        iframe = driver.find_elements("tag name", "iframe")
        return len(iframe)
    except:
        return 0
    
def title_vs_domain(driver, url):
    try:
        ext = tldextract.extract(url)
        domain = ext.domain
        title = driver.title
        distance = nltk.distance(title, domain)
        return distance
    except:
        return None

    
def suspicious_keywords(driver, keywords, response):
    if response == None:
        return None
    length = len(response.text)
    keywords = keywords.lower().splitlines()
    page_text = driver.page_source.lower()
    found = 0
    for word in keywords:
        if word in page_text:
            found += 1
    if length > 0:
        return (found / length) * 1000
    else:
        return 0

def whois_connect(url):
    available = 1
    w = None
    ext = tldextract.extract(url)
    url = ext.domain + "." + ext.suffix
    try:
        w = whois.whois(url)
    except Exception as s:
        available = 0
        print(s)
        w = None
    return w, available


def connection_1():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    driver = webdriver.Chrome(options=options)
    driver.set_page_load_timeout(5)
    stealth(driver,
    languages=["en-US", "en"],
    vendor="Google Inc.",
    platform="Win32",
    webgl_vendor="Intel Inc.",
    renderer="Intel Iris OpenGL Engine",
    fix_hairline=True,
     )
    time.sleep(0.8)
    return driver

    

def domain_days(w):
    if w == None:
        return None
    try:
        if isinstance(w.creation_date, list):
            creation_date = w.creation_date[0]
        else:
            creation_date = w.creation_date
        date = creation_date.date()
        now = datetime.now(timezone.utc).date()
        delta = now - date
        days = delta.days
        return days
    except:
        return None

def expiration_time(w):
    if w == None:
        return None
    try:
        if isinstance(w.expiration_date, list):
            expiration_date = w.expiration_date[0]
        else:
            expiration_date = w.expiration_date
        date = expiration_date.date()
        now = datetime.now(timezone.utc).date()
        delta = date - now
        days = delta.days
        return days
    except:
        return None

def features1(url, response, driver, w, score, keywords,  available):
    features = {"SSL/Connection": score,
    "Response length": response_length(response),
    "Suspicious server": server(response),
    "Number of forms": forms(driver),
    "Number of password forms": password_forms(driver),
    "Number of 'text' forms": text_forms(driver),
    "Number of hidden elements": hidden(driver),
    "Number of iframe": iframe(driver),
    "Number of suspicious keywords / response length": suspicious_keywords(driver, keywords, response),
    "Domain age in days": domain_days(w),
    "Domain expires in ? days": expiration_time(w),
    "Number of images": img(driver),
    "Number of links in HTML": links(driver),
    "Number of external links": external_links(driver, url),
    "History length (number of redirections)": history_length(response),
    "whois available":  available,
    "domain changed": domain_change(response, url),
    "is_phish": 1
    }
    return features
