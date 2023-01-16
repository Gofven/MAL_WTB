from scrapers import get_mal_user_watchtime
import pytest


@pytest.mark.asyncio
async def test_get_mal_user_statistics():
    test = await get_mal_user_watchtime(username='crated')
    print(test)


@pytest.mark.asyncio
async def test_save_mal_user_statistics():
    await get_mal_user_watchtime(username='crated', store_data=True)
