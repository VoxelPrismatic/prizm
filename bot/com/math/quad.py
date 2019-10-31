#!/usr/bin/env python3
# -*- coding: utf-8 -*

#/// DEPENDENCIES
import discord                    #python3.7 -m pip install -U discord.py
import logging
import math
from numexpr import evaluate as evl
from util import embedify
from sympy.simplify.simplify import nsimplify as nsimp
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

@commands.command(aliases = [], 
                      help = 'math',
                      brief = 'Solves the quadratic formula',
                      usage = ';]quad {A} {B} {C}',
                      description = '''    A, B, C [FLOAT] - Corrosponds to "Ax^2 + Bx + C"
    ''')
@commands.check(enbl)
async def quad(ctx, A: float, B: float, C: float):
    root = str(nsimp(f'sqrt({B**2}-4*{A}*{C})'))
    imaginary, K, D = False, 1, 1
    if '*I' in root:
        root, imaginary = root.replace('*I', ''), True
    if '*' not in root and 'sqrt(' not in root:
        K, D = int(root), 1
    elif '*' not in root and 'sqrt(' in root:
        K, D = 1, float(root.split('sqrt(')[1][:-1])
    else:
        K, D = int(root.split('*')[0]), float(root.split('sqrt(')[1][:-1])
    if imaginary:
        K = K*1j
    sol1 = evl(f"({-B}+{K}*sqrt({D}))/(2*{A})")
    sol2 = evl(f"({-B}-{K}*sqrt({D}))/(2*{A})")
    await ctx.send(embed=embedify.embedify(desc=f'''```md
#]QUADRATICS``````
{-B}+-{K}√{D}
-----------------
{2*A}``````diff
+] [{-B/(2*A)} + {K/(2*A)}√{D}] {sol1}
-] [{-B/(2*A)} - {K/(2*A)}√{D}] {sol2}```'''))


##///---------------------///##
##///     OTHER STUFF     ///##
##///---------------------///##
def setup(bot):
    print('+COM')
    bot.add_command(quad)
    print('GOOD')

def teardown(bot):
    print('-COM')
    bot.remove_command('quad')
    print('GOOD')

