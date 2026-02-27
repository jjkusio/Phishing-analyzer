from URL_stats import features
from dynamic_stats import features1, connection, connection_1, whois_connect
import pandas as pd
import sqlite3


def sql(columns):
    conn = sqlite3.connect("data1.db")
    c = conn.cursor()
    columns_sql = ", ".join([f'"{col}" TEXT' for col in columns])
    sql_ = f"""
    CREATE TABLE IF NOT EXISTS results (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    url TEXT,
    {columns_sql}
    )
    """
    c.execute(sql_)
    conn.commit()
    return c, conn

with open("spam.txt", "r", encoding="utf-8") as f:
        keywords = f.read()

data = pd.read_csv("top-1m.csv", header=None, usecols=[1], nrows=19000)
data = data.drop_duplicates()
data[1] = "https://" + data[1]
dd = pd.read_csv("top500Domains.csv", usecols=["Root Domain"])
popular_domains = set(dd["Root Domain"])

def final_function(url, driver):
        response, score = connection(url)
        w,  available = whois_connect(url)
        f_dynamic = features1(url, response, driver, w, score, keywords, available) 
        f_url = features(url, popular_domains)
    
        final = f_url | f_dynamic
        return final 

