import aiohttp
import re
import sqlite3
import datetime
from services import save_user_watchtime


#  Webscrape MAL information
async def get_mal_user_watchtime(*, username: str, is_anime: bool = True, store_data: bool = False) -> float:
    url = f'https://myanimelist.net/profile/{username}'

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            data = await resp.text()

    days = re.findall(r'Days: </span>(\d*\.*\d*)</div>', data)
    days = float(days[not is_anime])

    if store_data:
        save_user_watchtime(username=username, days=days, is_anime=is_anime)

    return days


def mal_watchtime_average(username: str, days: int, is_anime: int = True):
    date = datetime.datetime.now() - datetime.timedelta(days=days)
    date = date.strftime("%Y-%m-%d")
    con = sqlite3.connect("main.db")
    cur = con.cursor()
    cur.execute(f"""SELECT username, ROUND(SUM(delta) / COUNT(*), 2) AS change
                    FROM (SELECT username,
                                 days,
                                 days - LAG(days, 1, days) OVER (PARTITION BY username ORDER BY created_at) AS delta,
                                 is_anime,
                                 created_at
                          FROM mal_watchtime WHERE username="{username}" 
                                             AND created_at >= "{date}" 
                                             AND is_anime = {int(is_anime)})
                    GROUP BY username;""")

    return cur.fetchone()[1]
