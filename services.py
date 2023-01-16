import sqlite3
from datetime import datetime


#  Store MAL information
def save_user_watchtime(username: str, days: float, is_anime: bool):
    con = sqlite3.connect("main.db")  # Creates the file if it doesn't exist
    cur = con.cursor()

    cur.execute("""CREATE TABLE IF NOT EXISTS mal_watchtime (
                   username TEXT NOT NULL,
                   days REAL NOT NULL,
                   is_anime BOOL NOT NULL,
                   created_at TEXT NOT NULL,
                   UNIQUE (username, is_anime, created_at) ON CONFLICT REPLACE)""")

    created_at = datetime.now().strftime("%Y-%m-%d")
    cur.execute(f"""INSERT OR REPLACE INTO mal_watchtime VALUES (?, ?, ?, ?)""",
                (username, days, is_anime, created_at))
    con.commit()
    return
