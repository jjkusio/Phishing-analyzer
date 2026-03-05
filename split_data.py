import sqlite3
import pandas as pd
from sklearn.model_selection import train_test_split

data = pd.read_csv("new_data.csv")
data = data.drop_duplicates()


df_35, df_temp = train_test_split(
    data,
    train_size=82900,
    stratify=data["is_phish"],
    random_state=42
)
df_10, df_test = train_test_split(
    df_temp,
    train_size=2000,
    stratify=df_temp["is_phish"],
    random_state=42
)

df_35.to_csv("data_35k.csv", index=False)
df_10.to_csv("data_10k.csv", index=False)
df_test.to_csv("data_test.csv", index=False)