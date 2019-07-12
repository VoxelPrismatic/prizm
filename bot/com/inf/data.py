#!/usr/bin/env python3
# -*- coding: utf-8 -*

#/// DEPENDENCIES
import discord                    #python3.7 -m pip install -U discord.py
import logging
from util import embedify
from discord.ext import commands
from discord.ext.commands import Bot, MissingPermissions, has_permissions
from chk.enbl import enbl

##///---------------------///##
##///    BOT  COMMANDS    ///##
##///---------------------///##

@commands.command()
@commands.check(enbl)
async def data(ctx): await ctx.send(embed=embedify.embedify(desc='''```md
#] HOW YOUR DATA IS USED
-
Data is only stored when talking to the bot directly,
using "]{message}", using commands, or saving server data.
-
Some data is stored forever on the owner's computer
This data only stores your message content, and nothing
more.
-
All guild data will be DELETED forever the moment the bot
leaves the guild, and cannot be recovered. This includes
tags, banned words, mods, command availability, and the prefix.
-
If you do not feel comfortable with this, dont talk to
this bot, or just dont say bad things. I, PRIZ ;]#9244 have
made this bot with a strong database and nobody can break in
except for me XD
-
#] TL;DR // Only messages are stored when using "]{msg}" or "}{msg}"
#] and when you use commands or you create en/disable a command or
#] create a tag, or access server specific data
>  But that data is only used for this bot
>  I, PRIZ ;]#9244, am not selling it```'''))

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

