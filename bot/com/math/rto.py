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

@commands.command(aliases = ['frac', 'ratio'], 
                  help = 'math',
                  brief = 'Reduces the ratio between {x} and {y}',
                  usage = ';]rto {x} {y}',
                  description = '''\
X [NUMBER] - The first number, or numerator
Y [NUMBER] - The second number, or denominator
''')
@commands.check(enbl)
async def rto(ctx, x: int, y: int):
    f = math.gcd(int1, int2)
    await ctx.send(f'```md\n#] {x/f}/{y/f}\n>  FACTOR ] {f}```')

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
