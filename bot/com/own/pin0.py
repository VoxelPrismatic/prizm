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
async def pin0(ctx, mID: discord.Message):
    await mID.pin()

@commands.command()
@commands.is_owner()
async def unpin0(ctx, mID: discord.Message):
    await mID.unpin()
    await ctx.send('`]UNPINNED`')

##///---------------------///##
##///     OTHER STUFF     ///##
##///---------------------///##
def setup(bot):
    print('+COM')
    bot.add_command(pin0)
    bot.add_command(unpin0)
    print('GOOD')

def teardown(bot):
    print('-COM')
    bot.remove_command('pin0')
    bot.remove_command('unpin0')
    print('GOOD')
