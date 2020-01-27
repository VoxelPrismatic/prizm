#!/usr/bin/env python3
# -*- coding: utf-8 -*

#/// DEPENDENCIES
import typing
import discord                    #python3.7 -m pip install -U discord.py
import logging, re
from discord.ext import commands
from discord.ext.commands import Bot, MissingPermissions, has_permissions
from chk.enbl import enbl
from math import *
from cmath import *
from numpy import *
from numexpr import *
import sympy as sp
from util.parse_eq import parse_eq, unparse_eq

##///---------------------///##
##///    BOT  COMMANDS    ///##
##///---------------------///##

@commands.command(aliases = ['simp', 'simplify', 'sym'],
                      help = 'math',
                      brief = 'Symplify complex equations',
                      usage = ';]simplify {eq}',
                      description = '''\
EQ [TEXT] - The equation to simplify
''')
@commands.check(enbl)
async def simple(ctx, *, eq: str):
    async with ctx.channel.typing():
        a, b, c, d, e, f, g, h, j, k, l, m, n, o, p, q, r, s, t, u, v, w, x,\
        y, z = sp.symbols(' '.join('abcdefghjklmnopqrstuvwxyz'))
        # 'i' is imaginary
        eq = parse_eq(eq)
        simpled = unparse_eq(str(sp.simplify(eq)))
        factored = unparse_eq(str(sp.factor(eq)))
        expanded = unparse_eq(str(sp.expand(eq)))
    await ctx.send(f'''```md
#]  CLEAN ] {simpled}
-
#] FACTOR ] {factored}
-
#] EXPAND ] {expanded}```''')


##///---------------------///##
##///     OTHER STUFF     ///##
##///---------------------///##
def setup(bot):
    print('+COM')
    bot.add_command(simple)
    print('GOOD')

def teardown(bot):
    print('-COM')
    bot.remove_command('simple')
    print('GOOD')
