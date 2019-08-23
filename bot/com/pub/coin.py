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

##///---------------------///##
##///   BOT DEFINITIONS   ///##
##///---------------------///##

def rand(ll,tt): return random.randint(ll,tt)

##///---------------------///##
##///    BOT  COMMANDS    ///##
##///---------------------///##

@commands.command(help = 'fun',
                  brief = 'Flips a virtual coin {x} times!',
                  usage = ';]coin {?num}',
                  description = 'NUM [INT] - How many times the coin should be flipped')
@commands.check(enbl)
async def coin(ctx, num: int = 1):
    lit = []
    tcnt = 0
    y = 0
    hcnt = 0
    outp = ""
    if num > 5000:
        await ctx.send('```]To prevent spam, MAX = 5000```')
        num = 5000
    for x in range(num):
        if rand(0,1):
            tcnt+=1
            outp +="[T] "
        else:
            hcnt+=1
            outp += "[H] "
        if y == 200:
            lit.append(str(outp))
            outp = ""
            y = 0
        else:
            y+=1
    if y != 0:
        lit.append(str(outp))
    await pages.PageThis(ctx, lit, "COINS", low=f'```]HEAD // {hcnt}\n]TAIL // {tcnt}```')


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

