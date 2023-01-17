import datetime
import math
from os import getenv

import discord
from discord.ext import commands
from dotenv import load_dotenv
from scrapers import get_mal_user_watchtime, mal_watchtime_average, xkcd_comic

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True

client = commands.Bot(command_prefix='!', intents=intents)


@client.command()
async def wtd(ctx):
    user_one = getenv("WTB_ONE_ALIAS", getenv("WTB_ONE"))
    wt_one = await get_mal_user_watchtime(username=getenv('WTB_ONE'), store_data=True)
    delta_one = mal_watchtime_average(username=getenv('WTB_ONE'), days=60)

    user_two = getenv("WTB_TWO_ALIAS", getenv("WTB_TWO"))
    wt_two = await get_mal_user_watchtime(username=getenv('WTB_TWO'), store_data=True)
    delta_two = mal_watchtime_average(username=getenv('WTB_TWO'), days=60)

    difference = abs(wt_one - wt_two)
    catch_up = datetime.datetime.now() + datetime.timedelta(
        days=abs(wt_one - wt_two) / abs(delta_one - delta_two)) if delta_one - delta_two != 0 else None

    if catch_up is None:
        catch_up_msg = f"{user_one} and {user_two} is watching at the same rate!"
    else:
        if not (wt_one > wt_two and delta_one >= delta_two or wt_two > wt_one and delta_two >= delta_one):
            catch_up_msg = f"At this rate, {user_one if wt_one > wt_two else user_two} " \
                           f"will catch up at {catch_up.strftime('%Y-%m-%d')}"

        else:
            catch_up_msg = f"{user_one if wt_one > wt_two else user_two} lead is growing at " \
                           f"{abs(delta_one - delta_two) * 24:.1f} hours/day, " \
                           f"{user_one if not wt_one > wt_two else user_two} is falling behind!"

    embed = discord.Embed(title="MAL Watch-Time Battler", description=catch_up_msg)
    embed.set_image(url=await xkcd_comic())
    embed.add_field(name="Current Standing",
                    value=f"{user_one}: {wt_one} Days\n{user_two}: {wt_two} Days",
                    inline=True)
    embed.add_field(name="Difference",
                    value=f"{difference:.1f} Days\n~{(difference * 1440 / 24):.0f} Episodes (24 min)",
                    inline=True)
    embed.add_field(name="Net Gain",
                    value=f"Mark: {delta_two * 24:.1f} hours/day\nGofven: {delta_one * 24:.1f} hours/day")

    return await ctx.send(embed=embed)


client.run(token=getenv('DISCORD_TOKEN'))
