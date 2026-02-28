import sqlite3
import pandas as pd

conn1 = sqlite3.connect("data1.db")
conn2 = sqlite3.connect("data2.db")

df1 = pd.read_sql("SELECT * FROM results", conn1)
df2= pd.read_sql("SELECT * FROM results", conn2)

df_merge = pd.concat([df1, df2], ignore_index=True)

conn_out = sqlite3.connect("data.db")
df_merge.to_sql("results", conn_out, if_exists="replace", index=False)