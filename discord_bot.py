from os import getenv

import discord
from discord.ext import commands
from dotenv import load_dotenv
from scrapers import get_mal_user_watchtime

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True

client = commands.Bot(command_prefix='!', intents=intents)


@client.command()
async def wtd(ctx):
    user_one = getenv("WTB_ONE_ALIAS", getenv("WTB_ONE"))
    wt_one = await get_mal_user_watchtime(username=getenv('WTB_ONE'))

    user_two = getenv("WTB_TWO_ALIAS", getenv("WTB_TWO"))
    wt_two = await get_mal_user_watchtime(username=getenv('WTB_TWO'))

    difference = max(wt_one, wt_two) - min(wt_one, wt_two)

    return await ctx.send(f'Difference between {user_one} and {user_two} is currently {difference:.2f} days')


client.run(token=getenv('DISCORD_TOKEN'))
