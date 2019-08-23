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

@commands.command(aliases=['reduce','radical'],
                  help = 'math',
                  brief = 'Radical Reducers',
                  usage = ';]rad {D} {X}',
                  description = 'D [INT] - Discriminator, aka X\u221A>>D<<\nX [INT] - The radical, aka "square root" is 2 and "cube root" is 3')
@commands.check(enbl)
async def rad(ctx, D: int, X: int = 2):
    K = 1
    for I in range(1,500):
        for J in range(2,int(D**(X**-1))):
            if not math.remainder(D, J**X):
                D = D/(J**X)
                K = K*J
            if J>(D**(X**-1)):
                break
        if D == 1: break
    if D == 1:
        await ctx.send(f'```]ANS // {K}```')
    elif K == 1:
        await ctx.send(f'```]ANS // \u221A{D}```')
    else:
        await ctx.send(f'```]ANS // {K}\u221A{D}```')

##///---------------------///##
##///     OTHER STUFF     ///##
##///---------------------///##
def setup(bot):
    print('+COM')
    bot.add_command(rad)
    print('GOOD')

def teardown(bot):
    print('-COM')
    bot.remove_command('rad')
    print('GOOD')
