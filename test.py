from scrapers import get_mal_user_watchtime, mal_watchtime_average
import pytest


@pytest.mark.asyncio
async def test_get_mal_user_statistics():
    test = await get_mal_user_watchtime(username='crated')
    print(test)


@pytest.mark.asyncio
async def test_save_mal_user_statistics():
    await get_mal_user_watchtime(username='crated', store_data=True)


@pytest.mark.asyncio
async def test_mal_watchtime_average():
    mal_watchtime_average(username='crated', days=3000)
