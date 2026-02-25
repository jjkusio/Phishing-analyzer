from main import final_function, connection_1, data, sql
with open("columns.txt", "r") as f:
    columns = f.read().splitlines()
c, conn = sql(columns)
try: 
    driver = connection_1()
except Exception as s:
    print(s)
    raise
count = 0
failed = 0
for element in data["url"]:
    if count == 75:
        driver.quit()
        count = 0
        try:
            driver = connection_1()
        except Exception as s:
            print(s)
            raise
    try:
        driver.get(element)
    except Exception as s:
        failed +=1
        print(s) 
        try:
            driver.quit()
        except:
            pass
        try: 
            driver = connection_1()
        except:
            print("Restart failed")
            break
        continue
    try:
        result = final_function(element, driver)
        keys = ", ".join([f'"{k}"' for k in result.keys()])
        placeholders = ", ".join(["?"] * len(result))
        values = list(result.values())
        sql = f'INSERT INTO results (url, {keys}) VALUES (?, {placeholders})'
        c.execute(sql, [element] + values)
    except Exception as e:
        print("Error:", e)
    count +=1

print("Failed selenium connections:", failed)
conn.commit()
conn.close()
driver.quit()
