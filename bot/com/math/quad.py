#!/usr/bin/env python3
# -*- coding: utf-8 -*

#/// DEPENDENCIES
import discord                    #python3.7 -m pip install -U discord.py
import logging
import math
from util import embedify
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

@commands.command(help = 'math',
                  brief = 'Solves the quadratic formula',
                  usage = ';]quad {A} {B} {C}',
                  description = 'A, B, C [FLOATS] - Corrosponds to "Ax^2 + Bx + C"')
@commands.check(enbl)
async def quad(ctx, A: float, B: float, C: float):
    D = B**2 - 4*A*C; K = 1
    for I in range(1,500):
        for J in range(2,1000):
            if not math.remainder(D, J**2):
                D = D/(J**2)
                K = K*J
        if D:
            break
    if D == 1:
        STR = f'{K}'
    elif K == 1:
        STR = f'√{D}'
    else:
        STR = f'{K}√{D}'
    await ctx.send(embed=embedify.embedify(desc=f'''```md
#]QUADRATICS``````
{-B}+-{STR}
------------
{2*A}``````diff
+] [{-B/(2*A)} + {K/(2*A)}√{D}] {(-B+((B**2)-2*A*C)**.5)/(2*A)}
-] [{-B/(2*A)} - {K/(2*A)}√{D}] {(-B-((B**2)-2*A*C)**.5)/(2*A)}```'''))


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

