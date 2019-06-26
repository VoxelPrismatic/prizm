#!/usr/bin/env python3
# -*- coding: utf-8 -*

#/// DEPENDENCIES
import discord                    #python3.7 -m pip install -U discord.py
import logging
from discord.ext import commands
from discord.ext.commands import Bot, MissingPermissions, has_permissions
from chk.enbl import enbl

##///---------------------///##
##///    BOT  COMMANDS    ///##
##///---------------------///##

@commands.command()
@commands.check(enbl)
async def echo(ctx, *, mCTX):
    try: await ctx.channel.purge(limit=1)
    except: pass
    await ctx.send(content=mCTX)

##///---------------------///##
##///     OTHER STUFF     ///##
##///---------------------///##
def setup(bot):
    print('+COM')
    bot.add_command(echo)
    print('GOOD')

def teardown(bot):
    print('-COM')
    bot.remove_command('echo')
    print('GOOD')

