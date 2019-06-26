#!/usr/bin/env python3
# -*- coding: utf-8 -*

#/// DEPENDENCIES
import typing
import discord                    #python3.7 -m pip install -U discord.py
import logging
from dyn import refresh
from discord.ext import commands
from discord.ext.commands import Bot, MissingPermissions, has_permissions

##///---------------------///##
##///   BOT DEFINITIONS   ///##
##///---------------------///##

async def exc(ctx, code: int):
    print('EXCEPTION!')
    if code == 1: await ctx.send('```diff\n-]ERROR 400\n=]BAD REQUEST```')
    elif code == 2: await ctx.send('```diff\n-]ERROR 403\n=]ALL FORBIDDEN```')
    elif code == 3: await ctx.send('```diff\n-]ERROR 404\n=]ALL NOT FOUND```')

def lext(name, bot): bot.load_extension(name); print(f'>Lext {name}')
def rext(name, bot): bot.reload_extension(name); print(f'>Rext {name}')
def uext(name, bot): bot.unload_extension(name); print(f'>Uext {name}')

##///---------------------///##
##///    BOT  COMMANDS    ///##
##///---------------------///##

@commands.command()
@commands.is_owner()
async def fld(ctx, typ):
    allext, lodtxt = refresh.refresh()
    for ext in range(len(allext)):
        for com in allext[ext]:
            try:
                if typ == "l": lext(f"{lodtxt[ext]}{com}", ctx.bot)
                if typ == "r": rext(f"{lodtxt[ext]}{com}", ctx.bot)
                if typ == "u": uext(f"{lodtxt[ext]}{com}", ctx.bot)
            except: pass
    await ctx.message.add_reaction('\N{OK HAND SIGN}')

##///---------------------///##
##///     OTHER STUFF     ///##
##///---------------------///##
def setup(bot):
    print('+COM')
    bot.add_command(fld)
    print('GOOD')

def teardown(bot):
    print('-COM')
    bot.remove_command('fld')
    print('GOOD')