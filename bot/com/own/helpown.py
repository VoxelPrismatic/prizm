#!/usr/bin/env python3
# -*- coding: utf-8 -*

#/// DEPENDENCIES
import os
import discord                    #python3.7 -m pip install -U discord.py
import logging
import asyncio
from util import pages
from discord.ext import commands
from discord.ext.commands import Bot, MissingPermissions, has_permissions

##///---------------------///##
##///   BOT DEFINITIONS   ///##
##///---------------------///##

def rand(ll,tt): return random.randint(ll,tt)

async def exc(ctx, code: int):
    print('EXCEPTION!')
    if code == 1: await ctx.send('```diff\n-]ERROR 400\n=]BAD REQUEST```')
    elif code == 2: await ctx.send('```diff\n-]ERROR 403\n=]ALL FORBIDDEN```')
    elif code == 3: await ctx.send('```diff\n-]ERROR 404\n=]ALL NOT FOUND```')

##///---------------------///##
##///    BOT  COMMANDS    ///##
##///---------------------///##

@commands.command(aliases=["helpown"])
@commands.is_owner()
async def hlepown(ctx):

    lit = ["""
] ";]hlepown"
> Brings up this message :)
] ";]clrin0"
> An override for ";]clrin"
] ";]clr0"
> An override for ";]clr"
] ";]calc"
> A calculator
] ";]exe"
> Executables""",
            """] ";]pwr"
> Shuts down
] ";]rld"
> Reloads extensions
] ";]ld"
> Loads extensions
] ";]uld"
> Unloads extensions""",
            """] ";]pin0"
> An override for ";]pin"
] ";]unpin0"
> An override for ";]unpin" """]
    await pages.PageThis(ctx, lit)

##///---------------------///##
##///     OTHER STUFF     ///##
##///---------------------///##
def setup(bot):
    print('+COM')
    bot.add_command(hlepown)
    print('GOOD')

def teardown(bot):
    print('-COM')
    bot.remove_command('hlepown')
    print('GOOD')
