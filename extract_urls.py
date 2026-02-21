from main import final_function, connection_1
import sqlite3


with open("list.txt", "r") as f:
    data = f.read().splitlines()

first_result = final_function(data[0], driver)
columns = list(first_result.keys())

conn = sqlite3.connect("data.db")
c = conn.cursor()

columns_sql = ", ".join([f'"{col}" TEXT' for col in columns])
sql= f"""
CREATE TABLE IF NOT EXISTS results (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    url TEXT,
    {columns_sql}
)
"""
c.execute(sql)
conn.commit()

for element in data:
    try:
        result = final_function(element)
        keys = ", ".join([f'"{k}"' for k in result.keys()])
        placeholders = ", ".join(["?"] * len(result))
        values = list(result.values())
        sql = f'INSERT INTO results (url, {keys}) VALUES (?, {placeholders})'
        c.execute(sql, [element] + values)
    except Exception as e:
        print("Error:", e)
conn.commit()
conn.close()
