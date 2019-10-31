#!/usr/bin/env python3
# -*- coding: utf-8 -*

#/// DEPENDENCIES
import discord                    #python3.7 -m pip install -U discord.py
import logging
from random import randint as rand
from util import pages
from discord.ext import commands
from discord.ext.commands import Bot, MissingPermissions, has_permissions
from chk.enbl import enbl
from util.ez import wrap

##///---------------------///##
##///    BOT  COMMANDS    ///##
##///---------------------///##

@commands.command(aliases = [],
                  help = 'fun',
                  brief = 'Prints rng from {min} to {max}, {count} times!',
                  usage = ';]rng {min} {max} {?count}',
                  description = '''\
MIN   [NUMBER] - Minimum number
MAX   [NUMBER] - Maximum number
COUNT [NUMBER] - Number of numbers
''')
@commands.check(enbl)
async def rng(ctx, min: int, max: int, count: int = 1):
    lit = []
    if num > 2000:
        await ctx.send('```diff\n-] TO PREVENT SPAM, MAXIMUM NUMBERS IS 2000```')
        num = 2000
    lit = wrap(" ".join(str(rand(min, max)) for x in range(count)))
    await pages.PageThis(ctx, lit, "RNG", low=f'''```md
#] RNG BETWEEN {min} AND {max}
COUNT ] {len(ttl)}
  AVG ] {sum(ttl)/len(ttl):.4f}
RANGE ] {max(ttl)-min(ttl)}```''')


##///---------------------///##
##///     OTHER STUFF     ///##
##///---------------------///##
def setup(bot):
    print('+COM')
    bot.add_command(rng)
    print('GOOD')

def teardown(bot):
    print('-COM')
    bot.remove_command('rng')
    print('GOOD')

