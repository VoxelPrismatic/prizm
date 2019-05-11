#!/usr/bin/env python3
# -*- coding: utf-8 -*

#/// DEPENDENCIES
import discord                    #python3.7 -m pip install -U discord.py
import logging
from discord.ext import commands
from discord.ext.commands import Bot, MissingPermissions, has_permissions

##///---------------------///##
##///   BOT DEFINITIONS   ///##
##///---------------------///##

def embedify(text): return discord.Embed(title="!] PRIZ AI ;] [!", description=text, color=0x069d9d)

##///---------------------///##
##///    BOT  COMMANDS    ///##
##///---------------------///##

@commands.command()
async def data(ctx): await ctx.send('''```md
#] HOW YOUR DATA IS USED
Data is only stored when talking to the bot directly,
using "]{message}" or using commands
This data is stored forever on the owner's computer
This data only stores your message content, and nothing
more.
If you do not feel comfortable with this, dont talk to
this bot, or just dont say bad things.
#] TL;DR // Only messages are stored when using "]{msg}"
#] and when you use commands```''')

##///---------------------///##
##///     OTHER STUFF     ///##
##///---------------------///##
def setup(bot):
    print('+COM')
    bot.add_command(data)
    print('GOOD')

def teardown(bot):
    print('-COM')
    bot.remove_command('data')
    print('GOOD')

