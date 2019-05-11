#!/usr/bin/env python3
# -*- coding: utf-8 -*

#/// DEPENDENCIES
import discord                    #python3.7 -m pip install -U discord.py
import logging
import math
from discord.ext import commands
from discord.ext.commands import Bot, MissingPermissions, has_permissions

##///---------------------///##
##///   BOT DEFINITIONS   ///##
##///---------------------///##

def rand(ll,tt): return random.randint(ll,tt)
def embedify(text): return discord.Embed(title="!] PRIZ AI ;] [!", description=text, color=0x069d9d)
async def exc(ctx, code: int):
    print('EXCEPTION!')
    if code == 1: await ctx.send('```diff\n-]ERROR 400\n=]BAD REQUEST```')
    elif code == 2: await ctx.send('```diff\n-]ERROR 403\n=]ALL FORBIDDEN```')
    elif code == 3: await ctx.send('```diff\n-]ERROR 404\n=]ALL NOT FOUND```')

##///---------------------///##
##///    BOT  COMMANDS    ///##
##///---------------------///##

@commands.command()
async def quad(ctx, A: float, B: float, C: float):
    D = B**2 - 4*A*C; K = 1
    for I in range(1,500):
        for J in range(2,1000):
            if not math.remainder(D, J**2):
                D = D/(J**2); K = K*J
        if D:break
    if D == 1: STR = f'{K}'
    elif K == 1: STR = f'√{D}'
    else: STR = f'{K}√{D}'
    try: await ctx.send(embed=embedify(f'''```md
#]QUADRATICS``````
{-B}+-{STR}
------------
{2*A}``````diff
+] [{-B/(2*A)} + {K/(2*A)}√{D}] {(-B+((B**2)-2*A*C)**.5)/(2*A)}
-] [{-B/(2*A)} - {K/(2*A)}√{D}] {(-B-((B**2)-2*A*C)**.5)/(2*A)}```'''))
    except: await ctx.send(f'''```md
#]QUADRATICS``````
{-B}+-{STR}
------------
{2*A}``````diff
+] [{-B/(2*A)} + {K/(2*A)}√{D}] {(-B+((B**2)-2*A*C)**.5)/(2*A)}
-] [{-B/(2*A)} - {K/(2*A)}√{D}] {(-B-((B**2)-2*A*C)**.5)/(2*A)}```''')


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

