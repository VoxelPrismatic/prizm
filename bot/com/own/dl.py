#!/usr/bin/env python3
# -*- coding: utf-8 -*

#/// DEPENDENCIES
import os
import discord                    #python3.7 -m pip install -U discord.py
import logging
from discord.ext import commands
from discord.ext.commands import Bot, MissingPermissions, has_permissions

##///---------------------///##
##///   BOT DEFINITIONS   ///##
##///---------------------///##

def rand(ll,tt): return random.randint(ll,tt)

##///---------------------///##
##///    BOT  COMMANDS    ///##
##///---------------------///##

@commands.command(aliases=["del"])
@commands.is_owner()
async def dl(ctx, file):
    os.remove(file)
    await ctx.message.add_reaction('\N{OK HAND SIGN}')

##///---------------------///##
##///     OTHER STUFF     ///##
##///---------------------///##
def setup(bot):
    print('+COM')
    bot.add_command(dl)
    print('GOOD')

def teardown(bot):
    print('-COM')
    bot.remove_command('dl')
    print('GOOD')
