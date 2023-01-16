import aiohttp
import re
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
