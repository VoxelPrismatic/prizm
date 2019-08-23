#!/usr/bin/env python3
# -*- coding: utf-8 -*

#/// DEPENDENCIES
import discord                    #python3.7 -m pip install -U discord.py
import logging
from discord.ext import commands
from discord.ext.commands import Bot, MissingPermissions, has_permissions

##///---------------------///##
##///    BOT  COMMANDS    ///##
##///---------------------///##

@commands.command()
@commands.is_owner()
async def clr0(ctx, arg: int):
    await ctx.channel.purge(limit=arg+1)

##///---------------------///##
##///     OTHER STUFF     ///##
##///---------------------///##
def setup(bot):
    print('+COM')
    bot.add_command(clr0)
    print('GOOD')

def teardown(bot):
    print('-COM')
    bot.remove_command('clr0')
    print('GOOD')
