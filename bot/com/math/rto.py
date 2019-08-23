#!/usr/bin/env python3
# -*- coding: utf-8 -*

#/// DEPENDENCIES
import discord                    #python3.7 -m pip install -U discord.py
import logging
import math
from discord.ext import commands
from discord.ext.commands import Bot, MissingPermissions, has_permissions
from chk.enbl import enbl

##///---------------------///##
##///    BOT  COMMANDS    ///##
##///---------------------///##

@commands.command(aliases=['frac','ratio'],
                  help = 'math',
                  brief = 'Reduces the ratio between {x} and {y}',
                  usage = ';]rto {x} {y}',
                  description = 'X [INT] - The first number\nY [INT] - The second number')
@commands.check(enbl)
async def rto(ctx, int1: int, int2: int):
    factor = math.gcd(int1, int2)
    await ctx.send(f'```] FACT // {factor}\n] INT1 // {int1/factor}\n] INT2 // {int2/factor}```')

##///---------------------///##
##///     OTHER STUFF     ///##
##///---------------------///##
def setup(bot):
    print('+COM')
    bot.add_command(rto)
    print('GOOD')

def teardown(bot):
    print('-COM')
    bot.remove_command('rto')
    print('GOOD')
