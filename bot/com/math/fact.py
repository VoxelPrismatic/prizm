#!/usr/bin/env python3
# -*- coding: utf-8 -*

#/// DEPENDENCIES
import discord                    #python3.7 -m pip install -U discord.py
import logging
import math
import typing
import asyncio
from util import pages
from discord.ext import commands
from discord.ext.commands import Bot, MissingPermissions, has_permissions
from chk.enbl import enbl

##///---------------------///##
##///    BOT  COMMANDS    ///##
##///---------------------///##

@commands.command(aliases=["factorial"])
@commands.check(enbl)
async def fact(ctx, num: int):
    if num > 100000: return await ctx.send('```Do you really need that big of a number?```')
    async with ctx.channel.typing(): string = str(math.factorial(num))
    lit = []
    for strt in range(0, len(string), 2000): lit.append(string[strt:strt+2000])
    await pages.PageThis(ctx, lit, "FACTORIAL")

##///---------------------///##
##///     OTHER STUFF     ///##
##///---------------------///##
def setup(bot):
    print('+COM')
    bot.add_command(fact)
    print('GOOD')

def teardown(bot):
    print('-COM')
    bot.remove_command('fact')
    print('GOOD')
