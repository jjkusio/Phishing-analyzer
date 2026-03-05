import pandas as pd
import sqlite3

conn = sqlite3.connect("data_last3.db")
db = pd.read_sql("SELECT * FROM results", conn)
df = pd.read_csv("data_new.csv")

combined = pd.concat([db, df], ignore_index=False)
combined.to_csv("new_data.csv", index=False)