#!/usr/bin/env python3
# -*- coding: utf-8 -*

#/// DEPENDENCIES
import discord                    #python3.7 -m pip install -U discord.py
import logging
import random
from discord.ext import commands
from discord.ext.commands import Bot, MissingPermissions, has_permissions
from chk.enbl import enbl

##///---------------------///##
##///    BOT  COMMANDS    ///##
##///---------------------///##

@commands.command(aliases = [],
                  help = 'fun',
                  brief = 'Spams {num} chars!',
                  usage = ';]spam {?num}',
                  description = '''\
NUM [NUMBER] - How many chars to spam
''')
@commands.check(enbl)
async def spam(ctx, num: int = 10):
    num = min(num, 10000)
    data = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcsdefghgijklmnopqrstuvwxyz1234567890!@#$%^&*()-_=+[]{}\"\'<,>./?\\|`~"
    for x in range(int(num/2000)):
        await ctx.send("".join(random.choice(data) for n in range(2000)))
        num -= 2000
    await ctx.send("".join(random.choice(data) for n in range(num)))

##///---------------------///##
##///     OTHER STUFF     ///##
##///---------------------///##
def setup(bot):
    print('+COM')
    bot.add_command(spam)
    print('GOOD')

def teardown(bot):
    print('-COM')
    bot.remove_command('spam')
    print('GOOD')
