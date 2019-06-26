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
##///   BOT DEFINITIONS   ///##
##///---------------------///##

def embedify(text): return discord.Embed(title="!] PRIZ AI ;] [!", description=text, color=0x00ffff)
async def exc(ctx, code: int):
    print('EXCEPTION!')
    if code == 1: await ctx.send('```diff\n-]ERROR 400\n=]BAD REQUEST```')
    elif code == 2: await ctx.send('```diff\n-]ERROR 403\n=]ALL FORBIDDEN```')
    elif code == 3: await ctx.send('```diff\n-]ERROR 404\n=]ALL NOT FOUND```')

##///---------------------///##
##///    BOT  COMMANDS    ///##
##///---------------------///##

@commands.command(aliases=['reduce','radical'])
@commands.check(enbl)
async def rad(ctx, D: int, X: int = 2):
    K = 1
    for I in range(1,500):
        for J in range(2,int(D**(X**-1))):
            if not math.remainder(D, J**X):
                D = D/(J**X); K = K*J
            if J>(D**(X**-1)): break
        if D == 1: break
    if D == 1: await ctx.send(f'```]ANS // {K}```')
    elif K == 1: await ctx.send(f'```]ANS // \u221A{D}```')
    else: await ctx.send(f'```]ANS // {K}\u221A{D}```')

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
