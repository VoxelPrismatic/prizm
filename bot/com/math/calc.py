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
from discord.ext.commands import Bot
from util.parse_eq import parse_eq

##///---------------------///##
##///    BOT  COMMANDS    ///##
##///---------------------///##

@commands.command(
    aliases = [], 
    help = 'math',
    brief = 'It is a calculator',
    usage = ';]calc {eq}',
    description = '''\
EQ [TEXT] - The thing to solve
'''
)
@commands.check(enbl)
async def calc(ctx, *, eq: str):
    async with ctx.channel.typing():
        pass
    eq = parse_eq(eq)
    try:
        num = round(float(evaluate(eq)), 16)
        if str(num).endswith(".0"):
            num = int(num)
    except ValueError:
        await ctx.send("```diff\n-] BAD VALUE```")
    except SyntaxError:
        await ctx.send("```diff\n-] SYNTAX ERROR```")
    except ZeroDivisionError:
        await ctx.send("```diff\n-] DIV/0 ERROR```")
    except NameError:
        await ctx.send("```diff\n-] UNDEFINED```")
    else:
        await ctx.send(f'```md\n#] {num}```')

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