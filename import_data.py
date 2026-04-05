import pandas as pd
import sqlite3

conn = sqlite3.connect('movies.db')

df = pd.read_csv('movies.csv')

df.columns = [
    "Title",
    "Year",
    "IMDb",
    "Duration",
    "Genres",
    "Synopsis",
    "Cast",
    "Director",
    "Providers",
    "Link"
]

df.to_sql('movies', conn, if_exists='replace', index=False)

conn.close()

print("Data imported successfully into movies.db")