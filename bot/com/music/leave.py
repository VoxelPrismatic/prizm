#!/usr/bin/env python3
# -*- coding: utf-8 -*

#/// DEPENDENCIES
import typing
import discord                    #python3.7 -m pip install -U discord.py
import logging
from discord.ext import commands
from discord.voice_client import VoiceClient
from discord.ext.commands import Bot, MissingPermissions, has_permissions
from chk.enbl import enbl

##///---------------------///##
##///   BOT DEFINITIONS   ///##
##///---------------------///##

def rand(ll,tt): return random.randint(ll,tt)

##///---------------------///##
##///    BOT  COMMANDS    ///##
##///---------------------///##

@commands.command(aliases = [],
                  help = 'music',
                  brief = 'Leaves the VC',
                  usage = ';]leave',
                  description = '''[NO INPUT FOR THIS COMMAND]''')
@commands.check(enbl)
async def leave(ctx):
    vcC = ctx.voice_client
    try:
        await vcC.disconnect()
    except:
        pass
    await ctx.message.add_reaction('<:wrk:608810652756344851>')

##///---------------------///##
##///     OTHER STUFF     ///##
##///---------------------///##
def setup(bot):
    print('+COM')
    bot.add_command(leave)
    print('GOOD')

def teardown(bot):
    print('-COM')
    bot.remove_command('leave')
    print('GOOD')

