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

@commands.command(aliases = [],
                      help = 'math',
                      brief = 'Gives statistics on inputed data',
                      usage = ';]stats {data1} {data2} {...}',
                      description = '''\
DATAx [NUMBER] - A number or a statistic
''')
@commands.check(enbl)
async def stats(ctx, *data: float):
    try:
        mod = str(statistics.mode(data))
    except:
        mod = "[NONE]"
    await ctx.send(embed=embedify.embedify(desc=f'''```md
#] STATS
>   MAX ] {max(data)}
>   MIN ] {min(data)}
>   AVG ] {statistics.mean(data)}
>   MOD ] {mod}
>   MED ] {statistics.median(data)}
> RANGE ] {max(data)-min(data)}
> STDEV ] {statistics.stdev(data)}
> LOMED ] {statistics.median_low(data)}
> HIMED ] {statistics.median_high(data)}
```'''))

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

