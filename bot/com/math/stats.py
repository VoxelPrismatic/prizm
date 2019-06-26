#!/usr/bin/env python3
# -*- coding: utf-8 -*

#/// DEPENDENCIES
import discord                    #python3.7 -m pip install -U discord.py
import logging
import statistics
from util import embedify
from discord.ext import commands
from discord.ext.commands import Bot, MissingPermissions, has_permissions
from chk.enbl import enbl

##///---------------------///##
##///    BOT  COMMANDS    ///##
##///---------------------///##

@commands.command()
@commands.check(enbl)
async def stats(ctx, *data: int):
    try: mod = str(statistics.mode(data))
    except: mod = "[NONE]"
    try: await ctx.send(embed=embedify.embedify(desc=f'''```md
#] STATS
>   MAX // {max(data)}
>   MIN // {min(data)}
>   AVG // {statistics.mean(data)}
>   MOD // {mod}
>   MED // {statistics.median(data)}
> RANGE // {max(data)-min(data)}
> STDEV // {statistics.stdev(data)}
> LOMED // {statistics.median_low(data)}
> HIMED // {statistics.median_high(data)}
```'''))
    except: await ctx.send(f'''```md
#] STATS
>   MAX // {max(data)}
>   MIN // {min(data)}
>   AVG // {statistics.mean(data)}
>   MOD // {mod}
>   MED // {statistics.median(data)}
> RANGE // {max(data)-min(data)}
> STDEV // {statistics.stdev(data)}
> LOMED // {statistics.median_low(data)}
> HIMED // {statistics.median_high(data)}
```''')

##///---------------------///##
##///     OTHER STUFF     ///##
##///---------------------///##
def setup(bot):
    print('+COM')
    bot.add_command(stats)
    print('GOOD')

def teardown(bot):
    print('-COM')
    bot.remove_command('stats')
    print('GOOD')

