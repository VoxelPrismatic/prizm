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
##///   BOT DEFINITIONS   ///##
##///---------------------///##

def rand(ll,tt):
    return random.randint(ll,tt)

##///---------------------///##
##///    BOT  COMMANDS    ///##
##///---------------------///##

@commands.command(help = 'fun',
                  brief = 'Spams {x} chars!',
                  usage = ';]spam {?x}',
                  description = 'X [INT] - How many chars to spam DEFAULT: 10')
@commands.check(enbl)
async def spam(ctx, num: int = 10):
    if num > 10000: num = 10000
    send = ""
    data = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcsdefghgijklmnopqrstuvwxyz1234567890!@#$%^&*()-_=+[]{}\"\'<,>./?\\|`~"
    for x in range(num):
        send += data[rand(0,len(data)-1)]
        if len(send) == 2000:
            await ctx.send(send)
            send = ""
    if len(send) > 0: await ctx.send(send)

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
