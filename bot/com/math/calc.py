#!/usr/bin/env python3
# -*- coding: utf-8 -*

#/// DEPENDENCIES
import discord                    #python3.7 -m pip install -U discord.py
import logging, typing
from math import *
from cmath import *
from numpy import *
from numexpr import *
import sympy as sp
from chk.enbl import enbl
from discord.ext import commands
from discord.ext.commands import Bot, MissingPermissions, has_permissions

##///---------------------///##
##///    BOT  COMMANDS    ///##
##///---------------------///##

@commands.command(aliases = [], 
                      help = 'math',
                      brief = 'It is a calculator',
                      usage = ';]calc {eq}',
                      description = '''    EQ [STR] - The thing to solve
    ''')
@commands.check(enbl)
async def calc(ctx, *, eq: str):
    async with ctx.channel.typing():
        await ctx.send(f'''```md
#] {evaluate(str(sp.simplify(eq.replace("^","**")).evalf(16)))}```''')

##///---------------------///##
##///     OTHER STUFF     ///##
##///---------------------///##
def setup(bot):
    print('+COM')
    bot.add_command(calc)
    print('GOOD')

def teardown(bot):
    print('-COM')
    bot.remove_command('calc')
    print('GOOD')