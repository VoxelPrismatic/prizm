#!/usr/bin/env python3
# -*- coding: utf-8 -*

#/// DEPENDENCIES
import discord                    #python3.7 -m pip install -U discord.py
import logging
import random
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
                  brief = 'Flips a virtual coin {x} times!',
                  usage = ';]coin {?count}',
                  description = '''\
COUNT [NUMBER] - How many times the coin should be flipped
''')
@commands.check(enbl)
async def coin(ctx, count: int = 1):
    if num > 5000:
        await ctx.send('```diff\n-] TO PREVENT SPAM, MAX COIN COUNT IS 5000```')
        num = 5000
    st = " ".join(random.choice(["[H]", "[T]"]) for x in range(count))
    heads = st.count("[H]")
    tails = st.count("[T]")
    lit = wrap(st)
    await pages.PageThis(ctx, lit, "COINS", low=f'```md\n#] HEADS ] {heads}\n#] TAILS ] {tails}```')


##///---------------------///##
##///     OTHER STUFF     ///##
##///---------------------///##
def setup(bot):
    print('+COM')
    bot.add_command(coin)
    print('GOOD')

def teardown(bot):
    print('-COM')
    bot.remove_command('coin')
    print('GOOD')

